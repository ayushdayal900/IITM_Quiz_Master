from datetime import datetime
from flask import Blueprint, redirect, render_template, request, url_for
from models.models import Quiz, db, User_Info, Subject, Chapter, Question
# from models import db


# general routes
gen = Blueprint('general_routes', __name__)  
dB = Blueprint('database_routes', __name__)  
admin = Blueprint('admin', __name__)  
user = Blueprint('user', __name__)  



# general routes
@gen.route('/')
def home():
    return render_template('index.html')

@gen.route('/logout')
def logout():
    return render_template('login.html')



@gen.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        pwd   = request.form.get("password")
        usr = User_Info.query.filter_by(email=email, password=pwd).first()
        
        #existed and admin
        if usr and usr.role==0: 
            return redirect(url_for("admin.admin_dashboard"))
        #existed and user
        elif usr and usr.role==1:
            return redirect(url_for("user.user_dashboard"))
        # no one
        else:
            return render_template('login.html',msg="Invalid User Credentials.")
    return render_template('login.html',msg="")


@gen.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        email = request.form.get("email")
        pwd   = request.form.get("password")
        full_name   = request.form.get("full_name")
        quali   = request.form.get("qualification")
        dob   = request.form.get("date")
        dob = datetime.strptime(dob, "%Y-%m-%d").date()

        usr = User_Info.query.filter_by(email=email).first()
        # email already exists
        if usr:
            return render_template('signup.html',msg="Sorry, this email is already register...!")
        
        new_usr = User_Info(email=email, password=pwd, full_name=full_name, qualification=quali, dob = dob)
        db.session.add(new_usr)
        db.session.commit()
        
        return render_template("login.html",msg="Registration Successful. Try Login Now.")
    return render_template('signup.html')




# admin routes
@admin.route('/admin_dashboard')
def admin_dashboard():
    subs = Subject.query.all()
    return render_template('admin_dashboard.html', subs = subs)


@admin.route('/summary')
def summary():
    return render_template('summary.html')


@admin.route('/quiz')
def quiz():
    quizes = Quiz.query.all()
    return render_template('quiz.html', quizes = quizes)



@admin.route('/add_subject', methods=["POST", "GET"])
def add_subject():
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        
        sub = Subject(name = name, description = description)

        db.session.add(sub)
        db.session.commit()

        
        return redirect(url_for("admin.admin_dashboard"))
    return render_template('add_subject.html')




@admin.route('/add_chapter/<sid>', methods=["POST", "GET"])
def add_chapter(sid):
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        
        chap = Chapter(name = name, description = description, subject_id = sid)

        db.session.add(chap)
        db.session.commit()

        return redirect(url_for("admin.admin_dashboard"))
    return render_template('add_chapter.html',sid=sid)



@admin.route('/add_quiz', methods=["POST", "GET"])
def add_quiz():
    if request.method == "POST":
        user_id = request.form.get("user_id")  
        subject_id = request.form.get("subject_id")  
        chapter_id = request.form.get("chapter_id")  
        question_id = request.form.get("question_id")  

        datetime_str = request.form.get("datetime")
        date_time = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")

        duration = request.form.get("duration")
        score = request.form.get("score")

        quiz = Quiz(user_id=user_id,subject_id=subject_id,chapter_id=chapter_id,question_id=question_id,date_time=date_time,duration=duration,score=score)
        
        db.session.add(quiz)
        db.session.commit()

        return redirect(url_for("admin.quiz"))
    return render_template('add_quiz.html')



# user routes
@user.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')





# database routes
@dB.route('/users')
def users():
    user = User_Info.query.all()
    return render_template('user_dashboard.html', users = user)


@dB.route('/search')
def search():
    user = User_Info.query.all()
    return render_template('user_dashboard.html', users = user)
