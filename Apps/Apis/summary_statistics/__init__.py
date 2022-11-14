from flask_restful import Api

from Apps.Apis.summary_statistics.behavior_api import  AllBehaviorsResource, PutBehaviorResource, DeleteBehaviorResource
from Apps.Apis.summary_statistics.behaviors_summary.course_query_api import CourseQueryMembersResource
from Apps.Apis.summary_statistics.behaviors_summary.query_course_api import DateQueryBigCourseResource, \
    BCQuerySmallCourseResource
from Apps.Apis.summary_statistics.department_summary_api import DepartmentsResource
from Apps.Apis.summary_statistics.behaviors_summary.member_query_api import MemberQueryResource

summary_api = Api(prefix="/summary")


# 行为表
# 获取、新增、修改和删除行为信息
summary_api.add_resource(AllBehaviorsResource, '/behaviors/add/')
summary_api.add_resource(PutBehaviorResource, '/behaviors/put/')
summary_api.add_resource(DeleteBehaviorResource, '/behaviors/delete/')


# 行为明细
# 根据所选时间段查询符合条件的所有大课程
summary_api.add_resource(DateQueryBigCourseResource, '/big_courses/date_query/')
# 根据大课程信息查询其包含的所有小课程
summary_api.add_resource(BCQuerySmallCourseResource, '/small_courses/bc_query/')

# 课程查询
summary_api.add_resource(CourseQueryMembersResource, '/course_query/')
# 成员名字和电话号码查询
summary_api.add_resource(MemberQueryResource, '/member_query/')


# 部门汇总
summary_api.add_resource(DepartmentsResource, '/department_summary/')

