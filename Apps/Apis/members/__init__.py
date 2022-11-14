from flask_restful import Api

from Apps.Apis.members.check_in_api import CheckInMemberResource
from Apps.Apis.members.member_score_api import AddMemberScoreResource
from Apps.Apis.members.members_data_api import AddMemberResource, ModifyMemberResource, DeleteMemberScoreResource

# from Apps.Apis.members.output_members_excel_api import OutputMembersExcelResource

members_api = Api(prefix="/members")

# 成员信息增加
members_api.add_resource(AddMemberResource, '/member_data/add/')
# 成员信息修改
members_api.add_resource(ModifyMemberResource, '/member_data/modify/')
# 成员信息删除
members_api.add_resource(DeleteMemberScoreResource, '/member_data/delete/')


# 成员签到
members_api.add_resource(CheckInMemberResource, '/member_checkin/')


# 成员打分
members_api.add_resource(AddMemberScoreResource, '/member_score/add/')


# 人员名单导入
# members_api.add_resource(InputMembersExcelResource, '/input_members_excel/')
# # 人员名单导出
# members_api.add_resource(OutputMembersExcelResource, '/output_members_excel/')
