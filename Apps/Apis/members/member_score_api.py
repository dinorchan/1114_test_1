import json

from flask import request
from flask_restful import Resource, abort, fields, marshal
from sqlalchemy import and_

from Apps.Apis.api_constant import HTTP_CREATE_OK
from Apps.Apis.member_course_status_def import member_status, small_course_status
from Apps.Apis.members.member_add_score_def import add_member_score
from Apps.Apis.summary_statistics.behavior_api import behavior_fields
from Apps.Models.behavior_score_model import Behavior, MemberBehavior
from Apps.Models.small_course_dapartments_model import SmallCourseDepartments

sc_member_score_fields = {
    "scm_id": fields.Integer,
    "scm_date": fields.String,
    "scm_name": fields.String,
    "scm_phone": fields.String,
    "scm_seat_number": fields.String,
    "scm_firm_or_department": fields.String,
    "scm_job": fields.String,
    "scm_group": fields.String,
    "scm_status": fields.Integer,
    "scm_checkin_time": fields.DateTime,
    "scm_destination": fields.String,
    "scm_license_plate": fields.String,
    "scm_remark": fields.String,
    "scm_course": fields.String,
    "scm_add_score": fields.Float,
    "scm_subtract_score": fields.Float,
}

multi_sc_members_score_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "member_data": fields.Nested(sc_member_score_fields),
    "his(her)_behaviors": fields.List(fields.Nested(behavior_fields)),
}

class AddMemberScoreResource(Resource):

    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        scm_id = data["scm_id"]
        if not scm_id:
            return {"msg": "请输入小课程人员主键(scm_id)"}

        # 获取成员信息
        small_course_member = member_status(scm_id)
        small_course = small_course_status(small_course_member.scm_small_course_id)

        # 给成员打分
        # 获取该成员行为表单信息
        scm_behaviors = data["scm_behaviors"]

        # 获取该成员的部门信息
        member_department = SmallCourseDepartments.query.filter(
            and_(SmallCourseDepartments.scd_small_course_id == small_course.sc_id,
                 SmallCourseDepartments.scd_name == small_course_member.scm_firm_or_department)).first()

        # 将成员的加减分设置为0
        small_course_member.scm_add_score = 0
        small_course_member.scm_subtract_score = 0
        small_course_member.scm_score = 0
        # 将与该成员有关的历史行为数据删除
        existing_member_behaviors = MemberBehavior.query.filter(
            MemberBehavior.mb_member_id == small_course_member.scm_id).all()
        if existing_member_behaviors:
            for existing_member_behavior in existing_member_behaviors:
                if not existing_member_behavior.delete():
                    abort(400, msg="成员原有行为信息删除失败")
        # 该成员不属于任何部门
        if not member_department:
            # 将该成员此次课程的所有行为与行为表对比，打包出一份该成员关于此课程的所有行为表
            member_all_behaviors = add_member_score(small_course_member, scm_behaviors)
            data = {
                "msg": "成员打分保存成功",
                "status": HTTP_CREATE_OK,
                "member_data": small_course_member,
                "his(her)_behaviors": member_all_behaviors,
            }

            return marshal(data, multi_sc_members_score_fields)
        else:
            # 该成员有所属部门，先将其部门数据更新
            member_department.scd_add_score -= small_course_member.scm_add_score
            member_department.scd_subtract_score -= small_course_member.scm_subtract_score
            if not member_department.save():
                abort(400, msg="部门信息变更保存失败")

            # 将该成员此次课程的所有行为与行为表对比，打包出一份该成员关于此课程的所有行为表
            member_all_behaviors = add_member_score(small_course_member, scm_behaviors)
            member_department.scd_add_score += small_course_member.scm_add_score
            member_department.scd_subtract_score += small_course_member.scm_subtract_score
            if not member_department.save():
                abort(400, msg="部门信息变更保存失败")
            data = {
                "msg": "成员打分保存成功",
                "status": HTTP_CREATE_OK,
                "member_data": small_course_member,
                "his(her)_behaviors": member_all_behaviors,
            }

            return marshal(data, multi_sc_members_score_fields)




