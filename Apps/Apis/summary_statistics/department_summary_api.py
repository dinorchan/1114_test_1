import json

from flask import request
from flask_restful import Resource, marshal, fields

from Apps.Apis.api_constant import HTTP_OK
from Apps.Models.big_course_model import BigCourse
from Apps.Models.small_course_model import SmallCourse
from Apps.Models.small_course_dapartments_model import SmallCourseDepartments


small_course_department_fields = {
    "scd_id": fields.Integer,
    "scd_name": fields.String,
    "scd_add_score": fields.Float,
    "scd_subtract_score": fields.Float,
    "scd_attendance_num": fields.Float,
}

multi_small_courses_departments_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(small_course_department_fields)),
}


class DepartmentsResource(Resource):

    def get(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        started_date = data["started_date"]
        ended_date = data["ended_date"]
        big_course_id = data["big_course_id"]
        small_course_id = data["small_course_id"]
        # 没有输入限定时间段，返回所有部门信息
        if not (started_date and ended_date):
            all_departments_in_all_time = SmallCourseDepartments.query.all()
            if not all_departments_in_all_time:
                return {"msg": "目前没有任何部门信息"}

            data = {
                "msg": "获取大课程成功",
                "status": HTTP_OK,
                "data": all_departments_in_all_time
            }

            return marshal(data, multi_small_courses_departments_fields)
        else:
            # 没有输入大课程信息，返回该时间段内的所有部门信息
            if not big_course_id:
                departments_in_time = []
                all_bcs = BigCourse.query.all()
                if not all_bcs:
                    return {"msg": "该时间段内没有任何大课程信息，也没有任何部门信息"}
                for bc in all_bcs:
                    scs_in_bc = SmallCourse.query.filter(
                        SmallCourse.sc_big_course_id == bc.id).all()
                    if not scs_in_bc:
                        return {"msg": "该时间段内没有任何小课程信息，也没有任何部门信息"}
                    for sc in scs_in_bc:
                        departments_in_sc = SmallCourseDepartments.query.filter(
                            SmallCourseDepartments.scd_small_course_id == sc.id).all()
                        departments_in_time.append(departments_in_sc)
                    if not departments_in_time:
                        return {"msg": "此时间段内没有任何部门信息"}
                    data = {
                        "msg": "获取小课程下各部门数据成功",
                        "status": HTTP_OK,
                        "data": departments_in_time
                    }

                    return marshal(data, multi_small_courses_departments_fields)
            else:
                # 有大课程信息，没有小课程信息，返回此大课程下所有部门信息
                big_course = BigCourse.query.filter(BigCourse.id == big_course_id).first()
                departments_in_bc = []
                if not small_course_id:
                    scs_in_bc = SmallCourse.query.filter(
                        SmallCourse.sc_big_course_id == big_course.id).all()
                    if not scs_in_bc:
                        return {"msg": "此大课程内没有任何小课程信息，也没有任何部门信息"}
                    for sc in scs_in_bc:
                        departments_in_sc = SmallCourseDepartments.query.filter(
                            SmallCourseDepartments.scd_small_course_id == sc.id).all()
                        departments_in_bc.append(departments_in_sc)
                    if not departments_in_bc:
                        return {"msg": "此大课程内没有任何部门信息"}
                    data = {
                        "msg": "获取小课程下各部门数据成功",
                        "status": HTTP_OK,
                        "data": departments_in_bc
                    }

                    return marshal(data, multi_small_courses_departments_fields)
                else:
                    # 有小课程信息，返回小课程内所有部门信息
                    small_course = SmallCourse.query.filter(
                        SmallCourse.sc_big_course_id == big_course.id).first()
                    departments_in_sc = SmallCourseDepartments.query.filter(
                        SmallCourseDepartments.scd_small_course_id == small_course.id).all()
                    data = {
                        "msg": "获取小课程下各部门数据成功",
                        "status": HTTP_OK,
                        "data": departments_in_sc
                    }

                    return marshal(data, multi_small_courses_departments_fields)






