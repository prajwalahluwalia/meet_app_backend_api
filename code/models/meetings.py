from db import db
import datetime
from models import users

class MeetingModel(db.Model):
    __tablename__ = 'meetings'

    meeting_id = db.Column(db.Integer, primary_key = True)
    created_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = db.Column(db.String(80), db.ForeignKey('users.username'))
    scheduled_on = db.Column(db.DateTime())
    start_time =  db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())
    subject = db.Column(db.String(1000))
    total_time = db.column(db.Time())
    attendes = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    flag = db.Column(db.Boolean, default = False)
    user = db.relationship('UserModel', primaryjoin = (users.id == attendes), secondaryjoin = (users.username == created_by), lazy = "dynamic")

    def __init__(self, scheduled_on, start_time, end_time, subject, created_by):

        self.scheduled_on = scheduled_on
        self.start_time = datetime.strptime(start_time,"%H%M%S")
        self.end_time = datetime.strptime(end_time,"%H%M%S")
        self.subject = subject
        self.created_by = created_by

    @classmethod
    def find_by_creator(cls, created_by, scheduled_on):
        return cls.query.filter_by(created_by = created_by, scheduled_on = scheduled_on).first()

    @classmethod
    def find_by_time(cls, scheduled_on, start_time, end_time):
        return cls.query.filter_by(scheduled_on = scheduled_on, start_time=start_time, end_time=end_time).first()

    @classmethod
    def num_of_meets_for_user(cls, user_id, scheduled_on):
        return cls.query.filter_by(user_id = user_id, scheduled_on = scheduled_on, flag = True).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()