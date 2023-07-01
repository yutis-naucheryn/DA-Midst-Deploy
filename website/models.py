from . import db    #'from .' means from this package 
from flask_login import UserMixin
from sqlalchemy.sql import func     #func get current date and time
import pytz     #to have asia timezone
from datetime import datetime

# To get Malaysia current time ## previously using func but func can only save UTC+0 time which is not Malaysia time zone
malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
now_malaysia = datetime.now(malaysia_tz)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=now_malaysia)
    #this foreign key is only for one-to-many relationsip
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   #use lowercase when doing foreign key
    updated_on = db.Column(db.DateTime(timezone=True), default=now_malaysia)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)  #invalid for user to have same email with another user
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    is_verified = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note')     #use the name of the target class when doing relationship

class SentimentResult(db.Model):
    sentResult_id = db.Column(db.Integer, primary_key=True)
    sent_neg = db.Column(db.Float)
    sent_neu = db.Column(db.Float)
    sent_pos = db.Column(db.Float)
    sent_com = db.Column(db.Float)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

class DASSResult(db.Model):
    dass_id = db.Column(db.Integer, primary_key=True)
    depression = db.Column(db.Integer)
    anxiety = db.Column(db.Integer)
    stress = db.Column(db.Integer)
    submission_time = db.Column(db.DateTime(timezone=True), default=now_malaysia)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 