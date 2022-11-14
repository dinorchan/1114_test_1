import datetime

from flask_restful import abort
from sqlalchemy import and_

from Apps.Models.big_course_model import BigCourse
from Apps.Models.small_course_dapartments_model import SmallCourseDepartments
from Apps.Models.small_course_member_model import SmallCourseMember, INPUT_STATUS, CHECK_IN_STATUS, BE_LATE, ABSENCE
from Apps.Models.small_course_model import SmallCourse

# 传入大课程日期+名字，判断是否存在这个大课程，存在则返回大课程
def big_course_status(bc_id):
    big_course = BigCourse.query.filter(BigCourse.bc_id == bc_id).first()
    if not big_course:
        abort(400, msg="不存在这个大课程")
    return big_course

# 传入大课程+小课程名字，判断是否存在课程，存在则返回小课程
def small_course_status(sc_id):

    small_course = SmallCourse.query.filter(SmallCourse.sc_id == sc_id).first()
    if not small_course:
        abort(400, msg="不存在这个小课程")
    return small_course

def member_status(scm_id):
    member = SmallCourseMember.query.filter(SmallCourseMember.scm_id == scm_id).first()
    if not member:
        abort(400, msg="此小课程不存在该成员")
    return member

def small_course_department_update(sc_id, scm_firm_or_department):

    sc_department_status = SmallCourseDepartments.query.filter(
        and_(SmallCourseDepartments.scd_small_course_id == sc_id,
             SmallCourseDepartments.scd_name == scm_firm_or_department)).first()
    # 此小课程下，该部门信息不存在，故新建此小课程下的部门信息
    if not sc_department_status:
        new_department = SmallCourseDepartments()
        new_department.scd_name = scm_firm_or_department
        new_department.scd_small_course_id = sc_id
        new_department.scd_member_num += 1
        if not new_department.save():
            abort(400, msg="新建部门保存失败")
    else:
        # 此小课程下该部门存在，更新部门信息
        sc_department_status.scd_member_num += 1
        if not sc_department_status.save():
            abort(400, msg="新建部门保存失败")


# 修改小课程成员的签到状态
def member_check_status(small_course, member):

    # 获取当前时间
    check_time = datetime.datetime.now()

    # 获取课程日期
    date_now = small_course.sc_date
    # 缺席时间
    absence_time_str = small_course.sc_date + " 23:59:59"
    absence_time = datetime.datetime.strptime(absence_time_str, '%Y-%m-%d %H:%M:%S')
    # 签到时间范围(0-15)
    course_start_time = date_now + " " + small_course.sc_start_time
    start_time = datetime.datetime.strptime(course_start_time, '%Y-%m-%d %H:%M:%S')
    end_time = start_time + datetime.timedelta(minutes=15)

    # 如果成员的签到状态不为导入状态，则不可进行正常签到
    if member.scm_status != INPUT_STATUS:
        return member
    else:
        # 过早签到，数据不变化
        if check_time < start_time:
            member.scm_status = INPUT_STATUS
        # 正常签到时间范围
        elif check_time > start_time and check_time < end_time:
            member.scm_status = CHECK_IN_STATUS
        # 迟到
        elif check_time > end_time and check_time < absence_time:
            member.scm_status = BE_LATE
        # 缺席
        else:
            member.scm_status = ABSENCE

    # 保存成员和其部门的修改信息
    if not member.save():
        abort(400, msg="成员信息修改保存失败")

    return member

