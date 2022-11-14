import json

from flask import request
from flask_restful import Resource, marshal, fields
from Apps.Models.behavior_score_model import MemberBehavior, Behavior
from Apps.Models.small_course_member_model import SmallCourseMember


behavior_fields = {
    "id": fields.Integer,
    "b_name": fields.String,
    "b_status": fields.String,
    "b_score": fields.Float,
}

multi_behaviors_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(behavior_fields))
}

member_basic_data_fields = {
    "scm_id": fields.Integer,
    "scm_date": fields.String,
    "scm_course": fields.String,
    "scm_seat_number": fields.String,
    "scm_name": fields.String,
    "scm_job": fields.String,
    "scm_firm_or_department": fields.String,
}

member_personal_data_fields = {
    "member_basic_data": fields.Nested(member_basic_data_fields),
    "member_behaviors_data": fields.Nested(multi_behaviors_fields),
}

multi_members_behavior_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(member_personal_data_fields))
}


# 个人行为汇总查询
class MemberQueryResource(Resource):

    def get(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        started_date = data["started_date"]
        ended_date = data["ended_date"]
        scm_name = data["scm_name"]
        scm_phone = data["scm_phone"]
        # 没有输入人员的电话号码
        if not scm_phone:
            # 没有输入成员的名字
            if not scm_name:
                return {"msg": "请输入成员名字或电话号码"}
            # 只输入成员的名字
            members_in_all_time = SmallCourseMember.query.filter(
                SmallCourseMember.scm_name == scm_name).all()
            if not members_in_all_time:
                return {"msg": "不存在此成员"}
            # 没有限定时间段，返回成员的所有行为信息
            if not (started_date and ended_date):
                all_members_behaviors_list = []
                for member in members_in_all_time:
                    member_behaviors = MemberBehavior.query.filter(
                        MemberBehavior.mb_member_id == member.id).all()
                    # 将特定时段课程该学员的行为信息打包
                    behaviors_list = []
                    for member_behavior in member_behaviors:
                        behavior = Behavior.query.filter(Behavior.id == member_behavior.mb_behavior_id).first()
                        behaviors_list.append(behavior)
                    member_data = {
                        "member_data": marshal(member, member_basic_data_fields),
                        "member_behaviors_data": marshal(behaviors_list, behavior_fields),
                    }
                    all_members_behaviors_list.append(member_data)

                return all_members_behaviors_list
            else:
                # 根据所给时间段查询该成员的所有行为信息
                members = []
                for sc_member in members_in_all_time:
                    if (sc_member.scm_date >= started_date and sc_member.scm_date <= ended_date):
                        members.append(sc_member)
                if not members:
                    return {"msg": "该时间段内没有该成员的行为信息"}
                all_members_behaviors_list = []
                for member in members:
                    member_behaviors = MemberBehavior.query.filter(
                        MemberBehavior.mb_member_id == member.id).all()
                    # 将特定时段课程该学员的行为信息打包
                    behaviors_list = []
                    for member_behavior in member_behaviors:
                        behavior = Behavior.query.filter(Behavior.id == member_behavior.mb_behavior_id).first()
                        behaviors_list.append(behavior)
                    member_data = {
                        "member_data": marshal(member, member_basic_data_fields),
                        "member_behaviors_data": marshal(behaviors_list, behavior_fields),
                    }
                    all_members_behaviors_list.append(member_data)

                return all_members_behaviors_list

        # 输入了成员的电话号码
        else:
            members_in_all_time = SmallCourseMember.filter(
                SmallCourseMember.scm_phone == scm_phone).all()
            if not members_in_all_time:
                return {"msg": "不存在此成员"}
            # 没有输入限定时间段，则返回该成员所有时间段的所有行为信息
            if not (started_date and ended_date):
                all_members_behaviors_list = []
                for member in members_in_all_time:
                    member_behaviors = MemberBehavior.query.filter(
                        MemberBehavior.mb_member_id == member.id).all()
                    # 将特定时段课程该学员的行为信息打包
                    behaviors_list = []
                    for member_behavior in member_behaviors:
                        behavior = Behavior.query.filter(Behavior.id == member_behavior.mb_behavior_id).first()
                        behaviors_list.append(behavior)
                    member_data = {
                        "member_data": marshal(member, member_basic_data_fields),
                        "member_behaviors_data": marshal(behaviors_list, behavior_fields),
                    }
                    all_members_behaviors_list.append(member_data)

                return all_members_behaviors_list
            else:
                # 给出限定时间段，则返回该成员在限定时间段内的所有行为信息
                members = []
                for sc_member in members_in_all_time:
                    if (sc_member.scm_date >= started_date and sc_member.scm_date <= ended_date):
                        members.append(sc_member)
                if not members:
                    return {"msg": "不存在该成员在此时间段内的行为信息"}
                all_members_behaviors_list = []
                for member in members:
                    member_behaviors = MemberBehavior.query.filter(
                        MemberBehavior.mb_member_id == member.id).all()
                    # 将特定时段课程该学员的行为信息打包
                    behaviors_list = []
                    for member_behavior in member_behaviors:
                        behavior = Behavior.query.filter(Behavior.id == member_behavior.mb_behavior_id).first()
                        behaviors_list.append(behavior)
                    member_data = {
                        "member_data": marshal(member, member_basic_data_fields),
                        "member_behaviors_data": marshal(behaviors_list, behavior_fields),
                    }
                    all_members_behaviors_list.append(member_data)

                return all_members_behaviors_list












