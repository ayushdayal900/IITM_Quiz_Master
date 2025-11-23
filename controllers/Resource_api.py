import bcrypt
from flask_restful import Resource, Api
from flask import request
from models.models import *
from datetime import datetime


api = Api()

class UserApi(Resource):
    def get(self):
        users = User_Info.query.all()
        users_info = [
            {
                'id': u.id,
                'full_name': u.full_name,
                'email': u.email,
                'qualification': u.qualification,
                'role': u.role,
                'dob': u.dob.strftime('%Y-%m-%d'),
                'user_score': u.user_score,
                'quizzes': [q.id for q in u.quizs]
            }
            for u in users
        ]
        return users_info, 200
    
    # post
    def post(self):
        email = request.json.get("email")
        password = request.json.get("password")  
        full_name = request.json.get("full_name")
        qualification = request.json.get("qualification")
        role = request.json.get("role", 1)  
        dob = request.json.get("dob")
        user_score = request.json.get("user_score", 0) 

        
        dob = datetime.strptime(dob, "%Y-%m-%d")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User_Info(full_name=full_name,email=email,password=hashed_password, qualification=qualification,role=role,dob=dob,user_score=user_score)

        db.session.add(new_user)
        db.session.commit()

        return {"message": "New User Added!"}, 201

    # update
    def put(self,id):
        user = User_Info.query.filter_by(id = id).first()
        if user:
            user.email = request.json.get("email")
            user.password = request.json.get("password")
            user.full_name = request.json.get("full_name")
            user.qualification = request.json.get("qualification")
            user.role = request.json.get("role")
            user.dob = request.json.get("dob")
            user.user_score = request.json.get("user_score")

            dob = datetime.strptime(dob, "%Y-%m-%d")

            db.session.commit()
            return {"message : ": "User updated"}, 200
        
        return {"message : ": "User id not found"}, 404

    # delete
    def delete(self,id):
        user = User_Info.query.filter_by(id = id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message":"User Deleted"},200
        return {"message":"User not found"},404



class SubjectApi(Resource):
    def get(self):
        subjects = Subject.query.all()
        subjects_info = [
            {
                'id': s.id,
                'name': s.name,
                'description': s.description,
                'chaps': [{c.id: c.name} for c in s.chaps]
            }
            for s in subjects
        ]
        return subjects_info, 200

    def post(self):
        name = request.json.get("name")
        description = request.json.get("description")

        new_subject = Subject(name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        
        return {"message": "New Subject Added!"}, 201

    def put(self, id):
        subject = Subject.query.filter_by(id=id).first()
        if subject:
            subject.name = request.json.get("name")
            subject.description = request.json.get("description")
            db.session.commit()
            return {"message": "Subject Updated"}, 200
        return {"message": "Subject ID not found"}, 404

    def delete(self, id):
        subject = Subject.query.filter_by(id=id).first()
        if subject:
            db.session.delete(subject)
            db.session.commit()
            return {"message": "Subject Deleted"}, 200
        return {"message": "Subject not found"}, 404
    

class ChapterApi(Resource):
    def get(self):
        chapters = Chapter.query.all()
        chapters_info = [
            {
                'id': c.id,
                'name': c.name,
                'description': c.description,
                'subject_id': c.subject_id,
                'questions': [q.id for q in c.ques]
            }
            for c in chapters
        ]
        return chapters_info, 200

    def post(self):
        name = request.json.get("name")
        description = request.json.get("description")
        subject_id = request.json.get("subject_id")

        new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        
        return {"message": "New Chapter Added!"}, 201

    def put(self, id):
        chapter = Chapter.query.filter_by(id=id).first()
        if chapter:
            chapter.name = request.json.get("name")
            chapter.description = request.json.get("description")
            chapter.subject_id = request.json.get("subject_id")
            db.session.commit()
            return {"message": "Chapter Updated"}, 200
        return {"message": "Chapter ID not found"}, 404

    def delete(self, id):
        chapter = Chapter.query.filter_by(id=id).first()
        if chapter:
            db.session.delete(chapter)
            db.session.commit()
            return {"message": "Chapter Deleted"}, 200
        return {"message": "Chapter not found"}, 404



class QuestionApi(Resource):
    def get(self):
        questions = Question.query.all()
        questions_info = [
            {
                'id': q.id,
                'name': q.name,
                'description': q.description,
                'chapter_id': q.chapter_id,
                'quiz_id': q.quiz_id,
                'options': {
                    'option1': q.option1,
                    'option2': q.option2,
                    'option3': q.option3,
                    'option4': q.option4,
                    'correct_option': q.correct_option
                }
            }
            for q in questions
        ]
        return questions_info, 200

    def post(self):
        name = request.json.get("name")
        description = request.json.get("description")
        chapter_id = request.json.get("chapter_id")
        quiz_id = request.json.get("quiz_id")
        option1 = request.json.get("option1")
        option2 = request.json.get("option2")
        option3 = request.json.get("option3")
        option4 = request.json.get("option4")
        correct_option = request.json.get("correct_option")

        new_question = Question(
            name=name, description=description, chapter_id=chapter_id, quiz_id=quiz_id,
            option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option
        )

        db.session.add(new_question)
        db.session.commit()
        
        return {"message": "New Question Added!"}, 201

    def put(self, id):
        question = Question.query.filter_by(id=id).first()
        if question:
            question.name = request.json.get("name")
            question.description = request.json.get("description")
            question.chapter_id = request.json.get("chapter_id")
            question.quiz_id = request.json.get("quiz_id")
            question.option1 = request.json.get("option1")
            question.option2 = request.json.get("option2")
            question.option3 = request.json.get("option3")
            question.option4 = request.json.get("option4")
            question.correct_option = request.json.get("correct_option")

            db.session.commit()
            return {"message": "Question Updated"}, 200
        return {"message": "Question ID not found"}, 404

    def delete(self, id):
        question = Question.query.filter_by(id=id).first()
        if question:
            db.session.delete(question)
            db.session.commit()
            return {"message": "Question Deleted"}, 200
        return {"message": "Question not found"}, 404





class QuizApi(Resource):
    def get(self):
        quizzes = Quiz.query.all()
        quizzes_info = [
            {
                'id': q.id,
                'user_id': q.user_id,
                'chapter_id': q.chapter_id,
                'date_time': q.date_time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': str(q.duration),
                'score': q.score,
                'quiz_maxm_score': q.quiz_maxm_score,
                'questions': [que.id for que in q.questions]
            }
            for q in quizzes
        ]
        return quizzes_info, 200

    def post(self):
        user_id = request.json.get("user_id")
        chapter_id = request.json.get("chapter_id")
        date_time = request.json.get("date_time")
        duration = request.json.get("duration")
        score = request.json.get("score")
        quiz_maxm_score = request.json.get("quiz_maxm_score")

        date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

        new_quiz = Quiz(
            user_id=user_id, chapter_id=chapter_id, date_time=date_time,
            duration=duration, score=score, quiz_maxm_score=quiz_maxm_score
        )

        db.session.add(new_quiz)
        db.session.commit()

        return {"message": "New Quiz Added!"}, 201

    def delete(self, id):
        quiz = Quiz.query.filter_by(id=id).first()
        if quiz:
            db.session.delete(quiz)
            db.session.commit()
            return {"message": "Quiz Deleted"}, 200
        return {"message": "Quiz not found"}, 404


class ScoreApi(Resource):
    def get(self):
        scores = Score.query.all()
        scores_info = [
            {
                'id': s.id,
                'user_id': s.user_id,
                'quiz_id': s.quiz_id,
                'time_stamp_of_attempt': s.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S'),
                'score': s.score
            }
            for s in scores
        ]
        return scores_info, 200

    def post(self):
        user_id = request.json.get("user_id")
        quiz_id = request.json.get("quiz_id")
        time_stamp_of_attempt = request.json.get("time_stamp_of_attempt")
        score = request.json.get("score")

        time_stamp_of_attempt = datetime.strptime(time_stamp_of_attempt, "%Y-%m-%d %H:%M:%S")

        new_score = Score(user_id=user_id, quiz_id=quiz_id, time_stamp_of_attempt=time_stamp_of_attempt, score=score)
        db.session.add(new_score)
        db.session.commit()

        return {"message": "New Score Added!"}, 201



api.add_resource(UserApi, '/api/get_users', '/api/add_users', '/api/edit_users/<id>', '/api/delete_users/<id>')
api.add_resource(SubjectApi, '/api/get_subjects', '/api/add_subject', '/api/edit_subject/<id>', '/api/delete_subject/<id>')
api.add_resource(ChapterApi, '/api/get_chapters', '/api/add_chapter', '/api/edit_chapter/<id>', '/api/delete_chapter/<id>')
api.add_resource(QuestionApi, '/api/get_questions', '/api/add_questions', '/api/edit_questions/<id>', '/api/delete_questions/<id>')
api.add_resource(QuizApi, '/api/get_quizes', '/api/add_quiz', '/api/edit_quiz/<id>', '/api/delete_quiz/<id>')
api.add_resource(ScoreApi, '/api/get_scores', '/api/add_score', '/api/edit_score/<id>', '/api/delete_score/<id>')