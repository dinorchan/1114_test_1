from Apps.Models import BaseModel
from Apps.exts import db


class BigCourse(BaseModel):
    __tablename__ = "big_course"
    bc_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, )
    bc_name = db.Column(db.String(32))
    bc_date = db.Column(db.String(32))
    bc_remark = db.Column(db.String(128), default=None)
    small_course = db.relationship("SmallCourse", backref="BigCourse",
                                   lazy="dynamic", cascade='all, delete-orphan')

