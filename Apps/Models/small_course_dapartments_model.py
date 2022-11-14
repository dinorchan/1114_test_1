from Apps.Models import BaseModel
from Apps.exts import db


class SmallCourseDepartments(BaseModel):
    scd_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, )
    scd_name = db.Column(db.String(32))
    scd_add_score = db.Column(db.Float, default=0)
    scd_subtract_score = db.Column(db.Float, default=0)
    scd_attendance_num = db.Column(db.Integer, default=0)
    scd_small_course_id = db.Column(db.Integer,
                                    db.ForeignKey("small_course.sc_id", ondelete='CASCADE'))
    scd_member_num = db.Column(db.Integer, default=0)

