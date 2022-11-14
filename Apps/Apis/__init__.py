

from Apps.Apis.courses import courses_api
from Apps.Apis.members import members_api
from Apps.Apis.summary_statistics import summary_api
# import flask_excel as excel

def init_api(app):
    courses_api.init_app(app)
    members_api.init_app(app)
    summary_api.init_app(app)
    # excel.init_excel(app)





