import json

from flask import request
from flask_restful import Resource, abort, marshal, fields
from sqlalchemy import and_

from Apps.Apis.api_constant import HTTP_CREATE_OK, HTTP_DELETE_OK
from Apps.Apis.member_course_status_def import small_course_status, member_status, small_course_department_update
from Apps.Models.small_course_dapartments_model import SmallCourseDepartments
from Apps.Models.small_course_member_model import SmallCourseMember


small_course_member_fields = {
    "scm_id": fields.Integer,
    "scm_date": fields.String,
    "scm_course": fields.String,
    "scm_name": fields.String,
    "scm_phone": fields.String,
    "scm_seat_number": fields.String,
    "scm_firm_or_department": fields.String,
    "scm_job": fields.String,
    "scm_group": fields.String,
    "scm_destination": fields.String,
    "scm_license_plate": fields.String,
    "scm_remark": fields.String,
}


class AddMemberResource(Resource):

    # 增加和删除成员
    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        sc_id = data["sc_id"]
        sc_start_time = data["sc_start_time"]
        if not sc_id:
            return {"msg": "请输入完整的信息"}

        small_course = small_course_status(sc_id)

        scm_name = data["scm_name"]
        scm_phone = data["scm_phone"]
        scm_seat_number = data["scm_seat_number"]
        scm_firm_or_department = data["scm_firm_or_department"]
        scm_job = data["scm_job"]
        scm_group = data["scm_group"]
        scm_destination = data["scm_destination"]
        scm_license_plate = data["scm_license_plate"]
        scm_remark = data["scm_remark"]

        if not (scm_phone and scm_name and scm_seat_number):
            return {"msg": "未输入必选信息(手机号+名字+座位号)，成员信息录入失败！"}

        member_phone_state = SmallCourseMember.query.filter(
            and_(SmallCourseMember.scm_small_course_id == small_course.id,
                 SmallCourseMember.scm_phone == scm_phone)).first()
        if member_phone_state:
            return {"msg": "该电话号码已存在"}
        seat_status = SmallCourseMember.query.filter(
            and_(SmallCourseMember.scm_small_course_id == small_course.id,
                 SmallCourseMember.scm_seat_number == scm_seat_number)).first()
        if seat_status:
            return {"msg": "该座位已被使用"}

        # 信息录入
        small_course_member = SmallCourseMember()

        small_course_member.scm_name = scm_name
        small_course_member.scm_phone = scm_phone
        small_course_member.scm_date = small_course.sc_date
        small_course_member.scm_course = small_course.sc_name
        small_course_member.scm_seat_number = scm_seat_number
        small_course_member.scm_firm_or_department = scm_firm_or_department
        small_course_member.scm_job = scm_job
        small_course_member.scm_group = scm_group
        small_course_member.scm_destination = scm_destination
        small_course_member.scm_license_plate = scm_license_plate
        small_course_member.scm_remark = scm_remark
        small_course_member.scm_small_course_id = small_course.sc_id

        # 更新此小课程下的部门信息
        small_course_department_update(small_course, scm_firm_or_department)

        # 信息保存
        if not small_course_member.save():
            abort(400, msg="成员信息保存失败")

        # 小课程录入人数加一
        small_course.sc_member_num += 1
        data = {
            "msg": "成员信息保存成功",
            "status": HTTP_CREATE_OK,
            "data": marshal(small_course_member, small_course_member_fields)
        }

        return data

# 修改成员基础信息
class ModifyMemberResource(Resource):

    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        scm_id = data["scm_id"]
        if not scm_id:
            return {"msg": "请输入完整的信息：小课程人员主键(scm_id)"}
        small_course_member = member_status(scm_id)

        # 将成员电话号码清零
        small_course_member.scm_phone = None

        # 获取修改信息
        new_scm_name = data["new_scm_name"]
        new_scm_phone = data["new_scm_phone"]
        new_scm_firm_or_department = data["new_scm_firm_or_department"]
        new_scm_job = data["new_scm_job"]
        new_scm_group = data["new_scm_group"]
        new_scm_destination = data["new_scm_destination"]
        new_scm_license_plate = data["new_scm_license_plate"]
        new_scm_remark = data["new_scm_remark"]

        member_phone_state = SmallCourseMember.query.filter(
            and_(SmallCourseMember.scm_small_course_id == small_course_member.scm_small_course_id,
                 SmallCourseMember.scm_phone == new_scm_phone)).first()
        if member_phone_state:
            abort(400, msg="该电话号码已存在")

        # 判断该成员前后的部门数据是否相同，不相同则修改其原所属部门的人数
        if small_course_member.scm_firm_or_department != new_scm_firm_or_department:
            before_department = SmallCourseDepartments.query.filter(
                and_(SmallCourseDepartments.scd_small_course_id == small_course_member.scm_small_course_id,
                     SmallCourseDepartments.scd_name == new_scm_firm_or_department))
            before_department.scd_member_num -= 1

        # 更新该成员输入的部门的数据，已存在则人数加一，不存在则创建
        small_course_department_update(small_course_member.scm_small_course_id,
                                       new_scm_firm_or_department)

        small_course_member.scm_name = new_scm_name
        small_course_member.scm_phone = new_scm_phone
        small_course_member.scm_firm_or_department = new_scm_firm_or_department
        small_course_member.scm_job = new_scm_job
        small_course_member.scm_group = new_scm_group
        small_course_member.scm_destination = new_scm_destination
        small_course_member.scm_license_plate = new_scm_license_plate
        small_course_member.scm_remark = new_scm_remark

        # 信息保存
        if not small_course_member.save():
            abort(400, msg="成员信息保存失败")

        data = {
            "msg": "成员信息保存成功",
            "status": HTTP_CREATE_OK,
            "data": marshal(small_course_member, small_course_member_fields)
        }

        return data


# 删除成员信息
class DeleteMemberScoreResource(Resource):

    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        scm_id = data["scm_id"]
        if not scm_id:
            return {"msg": "请输入完整的信息：小课程人员主键(scm_id)"}

        # 获取成员信息
        small_course_member = member_status(scm_id)
        small_course = small_course_status(small_course_member.scm_small_course_id)
        # 获取成员部门信息
        member_department = SmallCourseDepartments.query.filter(
            and_(SmallCourseDepartments.scd_small_course_id == small_course.sc_id,
                 SmallCourseDepartments.scd_name == small_course_member.scm_firm_or_department)).first()
        # 部门人数和出席人数减一，部门加减分同时减去该成员加减分
        member_department.scd_attendance_num -= 1
        member_department.scd_member_num -= 1
        member_department.scd_add_score -= small_course_member.scm_add_score
        member_department.scd_subtract_score -= small_course_member.scm_subtract_score
        # 此小课程人数减一
        small_course.sc_member_num -= 1
        # 如果此小课程中该成员已出席，则小课程出席人数减一
        if small_course_member.scm_status == 1 or small_course_member.scm_status == 2:
            small_course.sc_attendance_num -= 1

        if not small_course_member.delete():
            abort(400, msg="人员信息删除失败")
        if not member_department.save():
            abort(400, msg="该成员所属部门信息修改保存失败")
        if not small_course.save():
            abort(400, msg="小课程信息修改保存失败")

        data = {
            "msg": "人员信息删除成功",
            "status": HTTP_DELETE_OK,
        }

        return data


