import json

from flask import request
from flask_restful import marshal, Resource

from Apps.Apis.api_constant import HTTP_OK
from Apps.Apis.courses.big_course_api import multi_big_courses_fields
from Apps.Apis.courses.small_course_api import multi_small_courses_fields
from Apps.Apis.member_course_status_def import big_course_status
from Apps.Models.big_course_model import BigCourse
from Apps.Models.small_course_model import SmallCourse


# 根据所选时间段查询大课程信息
class DateQueryBigCourseResource(Resource):

    def get(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        started_date = data["started_date"]
        ended_date = data["ended_date"]
        if not (started_date and ended_date):
            return {"msg": "请输入时间区间"}

        all_big_courses = BigCourse.query.all()
        if not all_big_courses:
            return {"msg": "目前没有任何大课程"}
        in_region_bcs = []
        for big_course in all_big_courses:
            if big_course.bc_date >= started_date and big_course.bc_date <= ended_date:
                in_region_bcs.append(big_course)
        if not in_region_bcs:
            return {"msg": "该时间段内没有大课程"}
        data = {
            "msg": "所有大课程如下",
            "status": HTTP_OK,
            "data": in_region_bcs
        }

        return marshal(data, multi_big_courses_fields)


# 根据大课程查询小课程信息
class BCQuerySmallCourseResource(Resource):

    def get(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        bc_id = data["bc_id"]
        if not bc_id:
            return {"msg": "请输入大课程信息(日期+名字)"}
        big_course = big_course_status(bc_id)
        if not big_course:
            return {"msg": "不存在这个大课程"}
        in_region_scs = SmallCourse.query.filter(
            SmallCourse.sc_big_course_id == big_course.id).all()
        if not in_region_scs:
            return {"msg": "该大课程下不存在任何小课程"}
        data = {
            "msg": "获取小课程信息成功",
            "status": HTTP_OK,
            "data": in_region_scs
        }

        return marshal(data, multi_small_courses_fields)