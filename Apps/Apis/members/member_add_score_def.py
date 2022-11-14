from flask import abort

from Apps.Models.behavior_score_model import Behavior, MemberBehavior


def add_member_score(small_course_member, scm_behaviors):
    member_all_behaviors = []
    for scm_behavior in scm_behaviors:
        # 逐一获取行为的具体信息
        behavior = Behavior.query.filter(Behavior.b_name == scm_behavior).first()
        if not behavior:
            abort(400, msg="不存在此行为相关信息")
        # 如果此行为拥有，则将此行为赋予该成员,通过中间表
        member_behavior = MemberBehavior()
        member_behavior.mb_member_id = small_course_member.scm_id
        member_behavior.mb_behavior_id = behavior.b_id
        member_all_behaviors.append(behavior)
        if not member_behavior.save():
            abort(400, msg="当前课程下该成员的行为信息保存失败")

    # 获取此次小课程该成员的所有行为的中间表，并将加减分各自汇总
    member_behaviors = MemberBehavior.query.filter(
        MemberBehavior.mb_member_id == small_course_member.scm_id).all()
    for member_behavior in member_behaviors:
        # 将行为逐一进行判断，筛选出加分项和减分项，并得出总加分和总减分
        m_behavior = Behavior.query.filter(
            Behavior.b_id == member_behavior.mb_behavior_id).first()
        if m_behavior.b_score > 0:
            small_course_member.scm_add_score += m_behavior.b_score
        else:
            small_course_member.scm_subtract_score += m_behavior.b_score
    small_course_member.scm_score = small_course_member.scm_subtract_score + small_course_member.scm_add_score

    if not small_course_member.save():
        abort(400, msg="成员打分保存失败")

    return member_all_behaviors
