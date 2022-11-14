import datetime
import json

from flask import request
from flask_restful import Resource, abort, fields, marshal
from sqlalchemy import and_

from Apps.Apis.api_constant import HTTP_OK
from Apps.Apis.member_course_status_def import small_course_status, member_check_status, member_status
from Apps.Models.small_course_dapartments_model import SmallCourseDepartments


small_course_member_fields = {
    "sc_id": fields.Integer,
    "scm_name": fields.String,
    "scm_phone": fields.String,
    "scm_date": fields.String,
    "scm_course": fields.String,
    "scm_seat_number": fields.String,
    "scm_status": fields.Integer,
    "scm_checkin_time": fields.DateTime,
}

class CheckInMemberResource(Resource):

    # 人员签到
    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        scm_id = data["scm_id"]
        if not scm_id:
            return {"msg": "请输入完整的信息：小课程人员电话主键(scm_id)"}

        # 获取成员信息
        small_course_member = member_status(scm_id)
        # 获取小课程
        small_course = small_course_status(small_course_member.scm_small_course_id)

        # 修改成员签到状态
        member = member_check_status(small_course, small_course_member)
        # 赋予当前时间给成员
        member.scm_checkin_time = datetime.datetime.now()
        # 保存成员信息
        if not member.save():
            abort(400, msg="成员信息修改保存失败")

        # 获取当前小课程下的该成员的部门数据
        in_small_course_department = SmallCourseDepartments.query.filter(
            and_(SmallCourseDepartments.scd_small_course_id == small_course.sc_id,
                 SmallCourseDepartments.scd_name == member.scm_firm_or_department)).first()
        # 如果该成员有部门信息，则根据该成员的签到情况更新其所属部门的信息
        if in_small_course_department:
            # 正常签到和迟到都属于已出勤,所有成员所属部门和该课程出席人数加一
            if member.scm_status == 1 or member.scm_status == 2:
                small_course.sc_attendance_num += 1
                in_small_course_department.scd_attendance_num += 1
                if not in_small_course_department.save():
                    abort(400, msg="部门数据修改保存失败")
        else:
            if member.scm_status == 1 or member.scm_status == 2:
                small_course.sc_attendance_num += 1

        if not small_course.save():
            abort(400, msg="小课程数据修改保存失败")

        data = {
            "status": HTTP_OK,
            "data": marshal(member, small_course_member_fields)
        }

        return data



