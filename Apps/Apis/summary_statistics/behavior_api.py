import json

from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal

from Apps.Apis.api_constant import HTTP_CREATE_OK, HTTP_PUT_OK, HTTP_DELETE_OK, HTTP_OK
from Apps.Models.behavior_score_model import Behavior

parse_add = reqparse.RequestParser()
parse_add.add_argument("b_name", required=True, help="请输入具体的行为名称")
parse_add.add_argument("b_status", required=True, help="请输入加分或减分")
parse_add.add_argument("b_score", required=True, help="请输入行为分值")

parse_put = reqparse.RequestParser()
parse_put.add_argument("b_name", required=True, help="请输入具体的行为名称")
parse_put.add_argument("b_status", required=True, help="请输入加分或减分")
parse_put.add_argument("b_score", required=True, help="请输入行为分值")

parse_delete = reqparse.RequestParser()
parse_delete.add_argument("b_name", required=True, help="请输入具体的行为名称")

behavior_fields = {
    "b_id": fields.Integer,
    "b_name": fields.String,
    "b_status": fields.String,
    "b_score": fields.Float,
}

multi_behaviors_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    "data": fields.List(fields.Nested(behavior_fields))
}

# 获取所有行为信息
class AllBehaviorsResource(Resource):

    # 获取行为信息
    def get(self):

        behaviors = Behavior.query.all()
        if not behaviors:
            abort(400, msg="目前没有任何行为信息")
        data = {
            "msg": "获取行为信息成功",
            "status": HTTP_OK,
            "data": behaviors
        }

        return marshal(data, multi_behaviors_fields)

class AddBehaviorsResource(Resource):

    # 新增行为信息
    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        b_name = data["b_name"]
        b_status = data["b_status"]
        b_score = data["b_score"]

        behavior_name = Behavior.query.filter(Behavior.b_name == b_name).first()
        if behavior_name:
            abort(400, msg="该行为已存在")

        behavior = Behavior()

        behavior.b_name = b_name
        behavior.b_status = b_status
        behavior.b_score = b_score

        if not behavior.save():
            abort(400, msg="该行为保存失败")
        data = {
            "msg": "该行为添加成功",
            "status": HTTP_CREATE_OK,
            "data": marshal(behavior, behavior_fields)
        }

        return data


# 修改行为信息
class PutBehaviorResource(Resource):

    # 修改行为信息
    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        b_name = data["b_name"]
        b_status = data["b_status"]
        b_score = data["b_score"]

        behavior = Behavior.query.filter(Behavior.b_name == b_name).first()
        if not behavior:
            abort(400, msg="该行为不存在")

        behavior.b_name = b_name
        behavior.b_status = b_status
        behavior.b_score = b_score

        if not behavior.save():
            abort(400, msg="该行为保存失败")
        data = {
            "msg": "该行为修改成功",
            "status": HTTP_PUT_OK,
            "data": marshal(behavior, behavior_fields)
        }

        return data


# 删除行为信息
class DeleteBehaviorResource(Resource):

    def post(self):
        data_json = request.get_data()
        data = json.loads(data_json)
        b_name = data["b_name"]

        behavior = Behavior.query.filter(Behavior.b_name == b_name).first()
        if not behavior:
            return {"msg": "该行为不存在"}
        if not behavior.delete():
            abort(400, msg="该行为删除失败")
        data = {
            "msg": "该行为删除成功",
            "status": HTTP_DELETE_OK,
        }

        return data
