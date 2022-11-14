import json
import time

from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal
from sqlalchemy import and_

from Apps.Apis.api_constant import HTTP_CREATE_OK, HTTP_DELETE_OK
from Apps.Apis.member_course_status_def import big_course_status, small_course_status
from Apps.Models.classroom_model import Classroom
from Apps.Models.small_course_model import SmallCourse

parse_get = reqparse.RequestParser()
parse_get.add_argument("small_course_status", required=True, help="获取小课程信息,请输入操作(future-past-ongoing)")


small_course_fields = {
    "sc_id": fields.Integer,
    "sc_group": fields.String,
    "sc_date": fields.String,
    "sc_name": fields.String,
    "sc_room": fields.String,
    "sc_start_time": fields.String,
    "sc_end_time": fields.String,
    "sc_attendance_num": fields.Integer,
    "sc_member_num": fields.Integer,
    "sc_remark": fields.String,
}

multi_small_courses_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(small_course_fields))
}


# 增加小课程
class AddSmallCourseResource(Resource):

    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        bc_id = data["bc_id"]
        if not bc_id:
            return {"msg": "请输入完整的大课程信息"}

        big_course = big_course_status(bc_id)

        sc_name = data["sc_name"]
        sc_room = data["sc_room"]
        sc_start_time = data["sc_start_time"]
        sc_end_time = data["sc_end_time"]
        sc_remark = data["sc_remark"]
        if not (sc_name and sc_room and sc_end_time and sc_start_time):
            return {"msg": "请输入完整的小课程信息(时间+地点+名字)"}

        # 判断小课程是否存在
        small_course_state = SmallCourse.query.filter(
            and_(SmallCourse.sc_big_course_id == big_course.bc_id,
                 SmallCourse.sc_name == sc_name,
                 SmallCourse.sc_room == sc_room,
                 SmallCourse.sc_start_time == sc_start_time)).first()
        if small_course_state:
            return {"msg": "该小课程已存在"}

        classroom_ok = True
        classrooms = Classroom.query.filter(
            and_(Classroom.c_date == big_course.bc_date,
                 Classroom.c_name == sc_room)).all()
        # 所选教室全天为空
        if not classrooms:
            classroom_ok = True
        else:
            # 将时间字符转化，再进行比较
            chose_start_time = time.strptime(sc_start_time, "%H:%M:%S")
            chose_end_time = time.strptime(sc_end_time, "%H:%M:%S")
            for classroom in classrooms:
                start_time = time.strptime(classroom.c_start_time, "%H:%M:%S")
                end_time = time.strptime(classroom.c_end_time, "%H:%M:%S")

                if not (chose_start_time > end_time or chose_end_time < start_time):
                    classroom_ok = False
                    break

        if not classroom_ok:
            return {"msg": "小课程时间设置存在冲突"}
        small_course = SmallCourse()
        small_course.sc_date = big_course.bc_date
        small_course.sc_group = big_course.bc_name
        small_course.sc_name = sc_name
        small_course.sc_room = sc_room
        small_course.sc_start_time = sc_start_time
        small_course.sc_end_time = sc_end_time
        small_course.sc_remark = sc_remark
        small_course.sc_big_course_id = big_course.bc_id

        if not small_course.save():
            abort(400, msg="小课程存储失败")
        # 储存教室信息
        sc_classroom = Classroom()
        sc_classroom.c_name = sc_room
        sc_classroom.c_date = small_course.sc_date
        sc_classroom.c_start_time = sc_start_time
        sc_classroom.c_end_time = sc_end_time
        sc_classroom.c_small_course_id = small_course.sc_id

        if not sc_classroom.save():
            abort(400, msg="教室信息存储失败")

        data = {
            "msg": "小课程存储成功",
            "status": HTTP_CREATE_OK,
            "data": marshal(small_course, small_course_fields)
        }

        return data


class DeleteSmallCourseResource(Resource):
    # 删除小课程
    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        sc_id = data["sc_id"]
        if not sc_id:
            return {"msg": "请输入完整的小课程信息(其所属大课程信息(日期+名字)+小课程信息(名字+地点+开始时间)"}
        small_course = small_course_status(sc_id)

        if not small_course.delete():
            abort(400, msg="小课程删除失败")
        data = {
            "msg": "小课程删除成功",
            "status": HTTP_DELETE_OK,
        }

        return data


