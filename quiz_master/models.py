from . import db
from sqlalchemy.orm import relationship
from flask import Flask, render_template, flash, redirect, session, request, url_for

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    user_score_list = db.relationship('Scores', back_populates = 'user_name', cascade = 'all, delete-orphan')

class Subjects(db.Model):
    __tablename__ ='subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    chapter_list = db.relationship('Chapters', back_populates = 'subject_name', cascade = 'all, delete-orphan')

class Chapters(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    subject_name = db.relationship('Subjects', back_populates = 'chapter_list')
    quiz_list = db.relationship('Quizzes', back_populates = 'chapter_name', cascade = 'all, delete-orphan')

class Quizzes(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date_of_quiz = db.Column(db.String(80), nullable=False)
    time_duration = db.Column(db.String(5), nullable=False)
    remarks = db.Column(db.String(80), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    chapter_name = db.relationship('Chapters', back_populates = 'quiz_list')
    question_list = db.relationship('Questions', back_populates = 'quiz_name', cascade = 'all, delete-orphan')
    quiz_score_list = db.relationship('Scores', back_populates = 'quiz_name', cascade = 'all, delete-orphan')

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_statement = db.Column(db.String(80), nullable=False)
    option1 = db.Column(db.String(80), nullable=False)
    option2 = db.Column(db.String(80), nullable=False)
    option3 = db.Column(db.String(80), nullable=False)
    option4 = db.Column(db.String(80), nullable=False)
    answer = db.Column(db.String(80), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    quiz_name = db.relationship('Quizzes', back_populates = 'question_list')

class Scores(db.Model):
    __tablename__ ='scores'
    id = db.Column(db.Integer, primary_key=True)
    total_scored = db.Column(db.Integer, nullable=False)
    time_stamp_of_attempt = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_name = db.relationship('Users', back_populates = 'user_score_list')
    quiz_name = db.relationship('Quizzes', back_populates = 'quiz_score_list')


def create_admin():
    admin_user = Users.query.filter(Users.is_admin == True).first()
    if not admin_user :
        admin_user = Users(username='admin', email='admin@gmail.com', password='admin', fullname='Admin User', qualification='Admin', dob='1990-01-01', is_admin=True)
        db.session.add(admin_user)
        db.session.commit()


