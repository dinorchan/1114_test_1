from Apps.Models import BaseModel
from Apps.exts import db

INPUT_STATUS = 0
CHECK_IN_STATUS = 1
BE_LATE = 2
ABSENCE = 3

class SmallCourseMember(BaseModel):
    __tablename__ = "small_course_member"
    scm_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, )
    scm_name = db.Column(db.String(32))
    scm_phone = db.Column(db.String(32))
    scm_course = db.Column(db.String(32))
    scm_seat_number = db.Column(db.String(32))
    scm_date = db.Column(db.String(32), default=None)
    scm_checkin_time = db.Column(db.DateTime, default=None)
    scm_status = db.Column(db.Integer, default=INPUT_STATUS)
    scm_score = db.Column(db.Float, default=0)
    scm_group = db.Column(db.String(32))
    scm_firm_or_department = db.Column(db.String(128))
    scm_job = db.Column(db.String(32))
    scm_license_plate = db.Column(db.String(32))
    scm_destination = db.Column(db.String(32))
    scm_remark = db.Column(db.String(256))
    scm_add_score = db.Column(db.Float, default=0)
    scm_subtract_score = db.Column(db.Float, default=0)
    scm_behavior = db.Column(db.String(128), default=None)
    scm_small_course_id = db.Column(db.Integer,
                                    db.ForeignKey("small_course.sc_id", ondelete='CASCADE'))
    member_behavior = db.relationship("MemberBehavior", backref="SmallCourseMember",
                                      lazy="dynamic", cascade='all, delete-orphan')


