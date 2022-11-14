from Apps.Models import BaseModel
from Apps.exts import db

COURSE_STATUS_ENDED = 0
COURSE_STATUS_ONGOING = 1
COURSE_STATUS_NOT_STARTED = 2

class SmallCourse(BaseModel):
    __tablename__ = "small_course"
    sc_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, )
    sc_name = db.Column(db.String(32))
    sc_group = db.Column(db.String(32))
    sc_start_time = db.Column(db.String(32))
    sc_end_time = db.Column(db.String(32))
    sc_room = db.Column(db.String(32))
    sc_date = db.Column(db.String(32))
    sc_remark = db.Column(db.String(128), default=None)
    sc_attendance_num = db.Column(db.Integer, default=0)
    sc_member_num = db.Column(db.Integer, default=0)
    sc_status = db.Column(db.Integer, default=COURSE_STATUS_NOT_STARTED)
    sc_big_course_id = db.Column(db.Integer,
                                 db.ForeignKey("big_course.bc_id", ondelete='CASCADE'))
    small_course_member = db.relationship("SmallCourseMember", backref="SmallCourse",
                                lazy="dynamic", cascade='all, delete-orphan')
    classroom = db.relationship("Classroom", backref="SmallCourse",
                                          lazy="dynamic", cascade='all, delete-orphan')
    department = db.relationship("SmallCourseDepartments", backref="SmallCourse",
                                lazy="dynamic", cascade='all, delete-orphan')


