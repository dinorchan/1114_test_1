from Apps.Models import BaseModel
from Apps.exts import db


class Behavior(BaseModel):
    __tablename__ = "behavior"
    b_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, )
    b_name = db.Column(db.String(64), unique=True)
    b_status = db.Column(db.String(32), default=None)
    b_score = db.Column(db.Float, default=0)
    member_behavior = db.relationship("MemberBehavior", backref="Behavior",
                                      lazy="dynamic", cascade='all, delete-orphan')

class MemberBehavior(BaseModel):
    __tablename__ = "member_behaviors"
    mb_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, )
    mb_member_id = db.Column(db.Integer, db.ForeignKey("small_course_member.scm_id",
                                                       ondelete='CASCADE'))
    mb_behavior_id = db.Column(db.Integer, db.ForeignKey("behavior.b_id",
                                                         ondelete='CASCADE'))




