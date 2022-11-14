import json

from flask import request
from flask_restful import Resource, marshal

from Apps.Apis.member_course_status_def import big_course_status, small_course_status
from Apps.Apis.summary_statistics.behaviors_summary.member_query_api import member_basic_data_fields, behavior_fields
from Apps.Models.behavior_score_model import MemberBehavior, Behavior
from Apps.Models.big_course_model import BigCourse
from Apps.Models.small_course_member_model import SmallCourseMember
from Apps.Models.small_course_model import SmallCourse


# 课程内所有成员行为汇总查询
class CourseQueryMembersResource(Resource):

    def get(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        started_date = data["started_date"]
        ended_date = data["ended_date"]
        bc_id = data["bc_id"]
        sc_id = data["sc_id"]
        if not (started_date and ended_date):
            return {"msg": "请输入时间区间"}

        # 没有输入大课程名字，返回日期范围内所有成员行为信息
        if not bc_id:
            all_big_courses = BigCourse.query.all()
            if not all_big_courses:
                return {"msg": "目前没有任何大课程"}
            in_region_bcs = []
            for big_course in all_big_courses:
                if big_course.bc_date >= started_date and big_course.bc_date <= ended_date:
                    in_region_bcs.append(big_course)
            if not in_region_bcs:
                return {"msg": "该时间段内没有大课程"}
            for bc in in_region_bcs:
                in_region_scs = SmallCourse.query.filter(SmallCourse.sc_big_course_id == bc.id).all()
                if not in_region_scs:
                    return {"msg": "该时间段内的所有大课程并未创建任何小课程"}
                for sc in in_region_scs:
                    members = SmallCourseMember.query.filter(
                        SmallCourseMember.scm_small_course_id == sc.id).all()
                    if not members:
                        return {"msg": "该时间段内的所有课程并未创建任何成员信息"}

                    all_members_behaviors_list = []
                    for member in members:
                        member_behaviors = MemberBehavior.query.filter(
                            MemberBehavior.mb_member_id == member.id).all()
                        # 将特定时段课程该学员的行为信息打包
                        behaviors_list = []
                        for member_behavior in member_behaviors:
                            behavior = Behavior.query.filter(
                                Behavior.id == member_behavior.mb_behavior_id).first()
                            behaviors_list.append(behavior)
                        member_data = {
                            "member_data": marshal(member, member_basic_data_fields),
                            "member_behaviors_data": marshal(behaviors_list, behavior_fields),
                        }
                        all_members_behaviors_list.append(member_data)

                    return all_members_behaviors_list
        else:
            # 有输入大课程信息
            big_course = big_course_status(bc_id)
            # 没有输入小课程信息，根据所选大课程查询其包含的成员行为信息
            if not sc_id:
                in_region_small_courses = SmallCourse.query.filter(
                    SmallCourse.sc_big_course_id == big_course.bc_id).all()
                if not in_region_small_courses:
                    return {"msg": "此大课程不存在任何小课程信息"}
                # 把该大课程下的所有小课程所包含的成员打包
                members_in_all_scs = []
                for small_course in in_region_small_courses:
                    members_in_sc = SmallCourseMember.query.filter(
                        SmallCourseMember.scm_small_course_id == small_course.sc_id).all()
                    members_in_all_scs.append(members_in_sc)
                if not members_in_all_scs:
                    return {"msg": "此大课程内没有任何成员信息"}
                all_members_behaviors_list = []
                # 逐步对每个小课程的所有成员查询
                for members in members_in_all_scs:
                    for member in members:
                        member_behaviors = MemberBehavior.query.filter(
                            MemberBehavior.mb_member_id == member.scm_id).all()
                        # 将特定时段课程该学员的行为信息打包
                        behaviors_list = []
                        for member_behavior in member_behaviors:
                            behavior = Behavior.query.filter(Behavior.b_id == member_behavior.mb_behavior_id).first()
                            behaviors_list.append(behavior)
                        member_data = {
                            "member_data": marshal(member, member_basic_data_fields),
                            "member_behaviors_data": marshal(behaviors_list, behavior_fields),
                        }
                        all_members_behaviors_list.append(member_data)

                return all_members_behaviors_list
            else:
                # 既输入了大课程信息，又输入了小课程信息，故返回该小课程内所有成员行为信息
                small_course = small_course_status(sc_id)
                members = SmallCourseMember.query.filter(
                    SmallCourseMember.scm_small_course_id == small_course.sc_id).all()
                if not small_course:
                    return {"msg": "此小课程不存在任何成员信息"}
                # 将该小课程内所有成员行为信息打包
                all_members_behaviors_list = []
                for member in members:
                    member_behaviors = MemberBehavior.query.filter(
                        MemberBehavior.mb_member_id == member.scm_id).all()
                    # 将特定时段课程该学员的行为信息打包
                    behaviors_list = []
                    for member_behavior in member_behaviors:
                        behavior = Behavior.query.filter(
                            Behavior.b_id == member_behavior.mb_behavior_id).first()
                        behaviors_list.append(behavior)
                    member_data = {
                        "member_data": marshal(member, member_basic_data_fields),
                        "member_behaviors_data": marshal(behaviors_list, behavior_fields),
                    }
                    all_members_behaviors_list.append(member_data)

                return all_members_behaviors_list


