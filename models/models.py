from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User_Info(db.Model, UserMixin):
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    qualification = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, default=1)
    dob = db.Column(db.Date, nullable=False)
    user_score = db.Column(db.Integer, default=0)    

    quizs = db.relationship("Quiz", cascade="all,delete", backref="user_info", lazy=True)











class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    chaps = db.relationship("Chapter", cascade="all,delete", backref="subject", lazy=True)










class Chapter(db.Model):

    __tablename__ = "chapter"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    # no_of_ques= db.Column(db.Integer, default=0)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    
    ques = db.relationship("Question", cascade="all,delete", backref="chapter", lazy=True)
    quizs = db.relationship("Quiz", cascade="all,delete", backref="chapter", lazy=True)











class Question(db.Model):
    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)  
    description = db.Column(db.String, nullable=False)  
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    
    option1 = db.Column(db.String, nullable=False)  
    option2 = db.Column(db.String, nullable=False)  
    option3 = db.Column(db.String, nullable=False)  
    option4 = db.Column(db.String, nullable=False)  
    correct_option = db.Column(db.Integer, nullable=False)  
    








    

class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)

    date_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Time, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    is_attempted = db.Column(db.Boolean, default=False)
    
    quiz_maxm_score = db.Column(db.Integer, default=0)
    questions = db.relationship("Question", cascade="all,delete",backref="quiz",lazy=True)










class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, nullable=False)  # Added to store attempt score
