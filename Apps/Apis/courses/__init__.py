from flask_restful import Api

from Apps.Apis.courses.big_course_api import AddBigCourseResource, EndedBigCoursesResource, DeleteBigCourseResource, \
    AllBigCourseResource, FutureBigCoursesResource
from Apps.Apis.courses.small_course_api import AddSmallCourseResource, DeleteSmallCourseResource

courses_api = Api(prefix='/courses')


courses_api.add_resource(AllBigCourseResource, "/big_courses/all/")

# 增加大课程
courses_api.add_resource(AddBigCourseResource, "/big_course/add/")
# 删除大课程
courses_api.add_resource(DeleteBigCourseResource, "/big_course/delete/")
# 查看未结束大课程
courses_api.add_resource(FutureBigCoursesResource, "/big_course/future/")
# 查看已结束大课程
courses_api.add_resource(EndedBigCoursesResource, "/big_course/past/")


# 增加小课程
courses_api.add_resource(AddSmallCourseResource, "/small_course/add/")
# 删除小课程
courses_api.add_resource(DeleteSmallCourseResource, "/small_course/delete/")

