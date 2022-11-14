from flask import Flask
from flask_cors import CORS

from Apps.Apis import init_api
from Apps.exts import init_exts


def create_app():

    app = Flask("__name__")
    # 加载配置
    app.config['SECRET_KEY'] = '123456'
    app.config['SQLALCHEMY_DATABASE_URI'] = "{}+{}://{}:{}@{}:{}/{}".\
        format("mysql", "pymysql", "root", "root", "localhost", "3306", "1114test")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config.from_object(envs.get(env))
    # 初始化第三方库
    init_exts(app)

    CORS(app, supports_credentials=True)
    # 初始化API
    init_api(app=app)

    return app

