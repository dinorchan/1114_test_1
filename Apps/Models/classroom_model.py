from Apps.Models import BaseModel
from Apps.exts import db


class Classroom(BaseModel):
    __tablename__ = "classroom"
    c_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, )
    c_name = db.Column(db.String(32))
    c_date = db.Column(db.String(32))
    c_start_time = db.Column(db.String(32))
    c_end_time = db.Column(db.String(32))
    c_small_course_id = db.Column(db.Integer,
                                  db.ForeignKey("small_course.sc_id", ondelete='CASCADE'))
