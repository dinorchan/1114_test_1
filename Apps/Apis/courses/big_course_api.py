import datetime
import json

from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal
from sqlalchemy import and_

from Apps.Apis.api_constant import HTTP_CREATE_OK, HTTP_DELETE_OK, HTTP_OK
from Apps.Apis.member_course_status_def import big_course_status
from Apps.Models.big_course_model import BigCourse

parse_get = reqparse.RequestParser()
parse_get.add_argument("big_course_state", required=True, help="获取大课程信息,请输入操作(future or past)")

big_course_fields = {
    "bc_id": fields.Integer,
    "bc_name": fields.String,
    "bc_date": fields.String,
    "bc_remark": fields.String,
}

multi_big_courses_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(big_course_fields))
}

class AllBigCourseResource(Resource):

    def get(self):
        all_bcs = BigCourse.query.all()
        if not all_bcs:
            return {"msg": "目前没有任何大课程"}
        data = {
            "msg": "大课程获取成功",
            "status": HTTP_CREATE_OK,
            "data": marshal(all_bcs, big_course_fields)
        }

        return data


# 增加大课程
class AddBigCourseResource(Resource):

    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        bc_name = data["bc_name"]
        bc_dates = data["bc_date"]
        if bc_dates and bc_name:
            # 如果输入的大课程有多个日期，则逐步判断和创建
            for bc_date in bc_dates:
                # 判断大课程名是否存在
                big_course_state = BigCourse.query.filter(
                    and_(BigCourse.bc_name == bc_name,
                         BigCourse.bc_date == bc_date)).first()
                if big_course_state:
                    return {"msg": "该大课程已存在"}
                else:
                    big_course = BigCourse()
                    big_course.bc_name = bc_name
                    big_course.bc_date = bc_date

                    # 大课程存储
                    if not big_course.save():
                        abort(400, msg="大课程存储失败")
                    data = {
                        "msg": "大课程存储成功",
                        "status": HTTP_CREATE_OK,
                        "data": marshal(big_course, big_course_fields)
                    }

                    return data
        else:
            return {"msg": "请输入完整的大课程信息(日期和名字)"}


# 删除大课程
class DeleteBigCourseResource(Resource):

    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        bc_id = data["bc_id"]
        if bc_id:
            big_course = big_course_status(bc_id)
            if not big_course.delete():
                abort(400, msg="该大课程名删除失败")
            data = {
                "msg": "该大课程删除成功",
                "status": HTTP_DELETE_OK,
            }

            return data
        else:
            return {"msg": "请输入完整的大课程信息(日期和名字)"}


# 获取已结束和未开始大课程
class FutureBigCoursesResource(Resource):

    def get(self):
        all_big_courses = BigCourse.query.all()
        date_now_str = datetime.date.today()
        if not all_big_courses:
            return {"msg": "目前没有任何大课程"}
        future_big_courses = []
        date_now = datetime.date.strftime(date_now_str, "%Y-%m-%d")
        for bc in all_big_courses:
            if bc.bc_date >= date_now:
                future_big_courses.append(bc)
        data = {
            "msg": "未结束大课程如下",
            "status": HTTP_OK,
            "data": future_big_courses
        }

        return marshal(data, multi_big_courses_fields)


class EndedBigCoursesResource(Resource):

    def get(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        bc_start_date = data["bc_start_date"]
        bc_ended_date = data["bc_ended_date"]
        query = data["query"]

        all_big_courses = BigCourse.query.all()
        date_now_str = datetime.date.today()
        if not all_big_courses:
            return {"msg": "目前没有任何大课程"}

        ended_big_courses = []
        date_now = datetime.date.strftime(date_now_str, "%Y-%m-%d")
        for bc in all_big_courses:
            if bc.bc_date < date_now:
                ended_big_courses.append(bc)

        in_region_bcs = []
        for bc in ended_big_courses:
            if bc.bc_date >= bc_start_date and bc.bc_date <= bc_ended_date:
                in_region_bcs.append(bc)
        if not query:
            return {"msg": "输入query进行查询"}
        data = {
            "msg": "已结束大课程如下",
            "status": HTTP_OK,
            "data": in_region_bcs
        }

        return marshal(data, multi_big_courses_fields)













