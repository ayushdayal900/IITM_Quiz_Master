from datetime import datetime
import os
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func
from models.models import Quiz, Score, db, User_Info, Subject, Chapter, Question
from app import login_manager, bcrypt
# from models import db
import matplotlib
# Use a non-GUI backend to avoid Tkinter issues
matplotlib.use('Agg')  

import matplotlib.pyplot as plt  








# general routes
gen = Blueprint('general_routes', __name__)  
data = Blueprint('database_routes', __name__)  
admin = Blueprint('admin', __name__)  
user = Blueprint('user', __name__)  





# @gen.route('/test_flash')
# def test_flash():
#     flash("This is a test flash message!", "danger")
#     return redirect(url_for("general_routes.login"))








# general routes
@gen.route('/')
def home():
    return render_template('index.html')



@gen.route('/logout')
def logout():

    logout_user()
    return redirect(url_for("general_routes.home"))



from flask import session  # Ensure session is imported

@gen.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")

        usr = User_Info.query.filter_by(email=email).first()

        if usr and bcrypt.check_password_hash(usr.password, pwd): 
            login_user(usr)

            # Admin Login
            if usr.role == 0:
                flash("Welcome Admin!", "success")
                return redirect(url_for("admin.admin_dashboard"))
            # User Login
            else:
                flash("Login Successful, Welcome!", "success")
                return redirect(url_for("user.user_dashboard"))
        
        # If user does not exist or password is incorrect
        flash("Invalid Email Or Password.!", "danger")
        return redirect(url_for("general_routes.login"))

    return render_template('login.html')


@gen.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")
        full_name = request.form.get("full_name")
        quali = request.form.get("qualification")
        dob = request.form.get("date")
        dob = datetime.strptime(dob, "%Y-%m-%d").date()

        usr = User_Info.query.filter_by(email=email).first()
        if usr:
            flash("Sorry, this email is already registered!", "danger")
            return redirect(url_for("general_routes.signup"))
        
        hash_pwd = bcrypt.generate_password_hash(pwd).decode("utf-8")
        new_usr = User_Info(email=email, password=hash_pwd, full_name=full_name, qualification=quali, dob=dob)

        db.session.add(new_usr)
        db.session.commit()

        # flash("Registration Successful. Try Login Now.", "success")
        return redirect(url_for("general_routes.login"))  # Removed _external & _scheme

    return render_template('signup.html')
















# admin routes
@admin.route('/admin_dashboard')
@login_required
def admin_dashboard():
    subs = Subject.query.all()
    return render_template('admin_dashboard.html', subs = subs)



def get_users():
    users = User_Info.query.all()
    return users

def get_quizes():
    quizes = Quiz.query.all()
    return quizes



def get_users_quiz_summary():
    users = get_users()
    summary = {u.full_name: u.user_score for u in users}
    
    x_names = list(summary.keys())
    y_scores = list(summary.values())

    plt.figure(figsize=(10, 6))  # Set figure size
    bars = plt.bar(x_names, y_scores, color=["red", "blue", "green", "purple", "orange"])
    plt.title("Users Performance")
    plt.xlabel("Users")
    plt.ylabel("Score")
    
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom'
        )
        
    plt.tight_layout()
    return plt





def get_subject_score_summary():
    quizes = get_quizes()
    summary = {q.chapter.subject.name: q.quiz_maxm_score for q in quizes}
    
    x_names = list(summary.keys())
    y_scores = list(summary.values())

    plt.figure(figsize=(10, 6))  
    bars = plt.bar(x_names, y_scores, color=["red", "blue", "green", "purple", "orange"])
    plt.title("Subject Score Summary")
    plt.xlabel("Subject")
    plt.ylabel("Score")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom'
        )
        
    plt.tight_layout()
    return plt







def get_quiz_que_summary():
    quizes = get_quizes()   
    if not quizes:
        return
    summary = {

        f"Quiz-{q.id}": len(q.questions) for q in quizes

        }

    x_names = list(summary.keys())
    y_scores = list(summary.values())

    plt.figure(figsize=(10, 5))  
    plt.bar(x_names, y_scores, color="red", width=0.4)
    plt.title("Quiz Questions Summary")
    plt.xlabel("Quiz")
    plt.ylabel("Questions")
    return plt

    

def get_chapter_score_summary():
    chapters = Chapter.query.all()
    chapter_scores = {}
    for chapter in chapters:
        if chapter.quizs:
            max_score = max(quiz.score for quiz in chapter.quizs)  # Changed to quiz.score
        else:
            max_score = 0  
        chapter_scores[chapter.name] = max_score

    x_names = list(chapter_scores.keys())
    y_scores = list(chapter_scores.values())

    plt.figure(figsize=(10, 6))
    plt.bar(x_names, y_scores, color="green")
    plt.title("Chapter & Total-Marks ")
    plt.xlabel("Chapter")
    plt.ylabel("Maximum Score")
    plt.tight_layout()
    
    return plt



@admin.route('/admin_summary')
@login_required

def admin_summary():


    users = (
        db.session.query(User_Info)
        .join(Score, User_Info.id == Score.user_id) 
        .distinct() 
        .all()
    )

    plot1 = get_users_quiz_summary()
    if(plot1):
        plot1.savefig("./static/images/users_summary.jpeg")
    else:
        return render_template('msg.html')
        # return render_template('msg.html', msg = "Plot image not found")

    plot2 = get_chapter_score_summary()
    if plot2:
        plot2.savefig("./static/images/chap_score_summary.jpeg")
    else:
        return render_template('msg.html')
        # return render_template('msg.html', msg = "Plot image not found")


    plot3 = get_quiz_que_summary()
    if plot3:
        plot3.savefig("./static/images/quiz_summary.jpeg") 
    else:
        return render_template('msg.html')
        # return render_template('msg.html', msg = "Plot image not found")
    
    plot4 = get_subject_score_summary()
    if plot4:
        plot4.savefig("./static/images/subject_score_summary.jpeg") 
    else:
        return render_template('msg.html')
        # return render_template('msg.html', msg = "Plot image not found")
    plt.close() 

    return render_template('admin_summary.html')







@admin.route('/quiz')
@login_required
def quiz():
    quizes = Quiz.query.all() 
    return render_template('quiz.html',quizes = quizes)






@admin.route('/quiz_details/<qzid>')
@login_required
def quiz_details(qzid):
    quiz = Quiz.query.filter_by(id=qzid).first() 
    return render_template('quiz_details.html',quiz = quiz)





@admin.route('/add_subject', methods=["POST", "GET"])
@login_required
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
@login_required
def add_chapter(sid):
    sub = Subject.query.filter_by(id=sid).first()
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')

        if name:    
            chap = Chapter(name = name, description = description, subject_id = sid)
            db.session.add(chap)
            db.session.commit()
        else:
            flash("Please Enter chap name","danger")
        return redirect(url_for("admin.admin_dashboard"))
    return render_template('add_chapter.html',sub = sub)



@admin.route('/add_quiz', methods=["POST", "GET"])
@login_required
def add_quiz():
    if request.method == "POST":
        # user_id = request.form.get("user_id")  
        
        chapter_id = request.form.get("chapter_id")  

        datetime_str = request.form.get("datetime")
        date_time = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")

        duration_str = request.form.get("duration")
        if len(duration_str) == 5:
            duration_str += ":00"

        duration = datetime.strptime(duration_str, "%H:%M:%S").time()

        score = request.form.get("score")

        # print(chapter_id)
        quiz = Quiz(user_id = current_user.id, chapter_id=chapter_id,date_time=date_time,duration=duration,score=score)
        
        db.session.add(quiz)
        db.session.commit()

        return redirect(url_for("admin.quiz"))
    
    chaps = Chapter.query.all()
    return render_template('add_quiz.html', chaps = chaps)




# @admin.route('/delete_quiz/<id>', methods=["POST", "GET"])
# def delete_quiz(id):
#     quiz = Quiz.query.filter_by(id == id).first()
#     db.session.delete(quiz)
#     db.session.commit()
#     return redirect(url_for("admin.admin_dashboard"))





@admin.route('/add_question/<cid>/<qid>', methods=["POST", "GET"])
@login_required
def add_question(cid,qid):

    chap = Chapter.query.filter_by(id=cid).first()
    quiz = Quiz.query.filter_by(id=qid).first()
    print(chap)
    print(quiz)

    if request.method == "POST":
        chapter_id = cid
        quiz_id = qid
        name = request.form.get('name')
        description = request.form.get('description')

        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correct_option')

        if name and option1 and option2 and option3 and option4 and correct_option:
            que = Question(name = name, description = description, chapter_id = chapter_id, quiz_id=quiz_id, option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option)
            db.session.add(que)
            db.session.commit()
        else:
            flash("Please specify the questions", "danger")
        return redirect(url_for("admin.quiz"))
    return render_template('add_question.html',cid = cid,qid = qid,chap = chap, quiz = quiz)



@login_required
def search_by_username(e):
    user = User_Info.query.filter(User_Info.email.ilike(f"%{e}%")).first()     
    return user


@login_required
def search_by_sub_name(s):
    sub = Subject.query.filter(Subject.name.ilike(f"%{s}%")).all()     
    return sub



@login_required
def search_by_quiz_id(q):
    quiz = Quiz.query.filter(Quiz.id.ilike(f"%{q}%")).all()     
    return quiz




@admin.route("/search", methods=['POST', 'GET'])
@login_required
def search():
    if request.method == "POST":
        search_txt = request.form.get('search_txt')

        by_username = search_by_username(search_txt)
        by_subs = search_by_sub_name(search_txt)
        # by_chaps = search_by_chap_for_quiz_name(search_txt)
        by_quizs = search_by_quiz_id(search_txt)


        if by_username:
            print(by_username)
            return render_template('./search/user_profile.html', user= by_username)
        elif by_subs:
            return render_template('./admin_dashboard.html', subs= by_subs)
        # elif by_chaps:
        #     return render_template('./quiz.html', chaps= by_chaps)
        elif by_quizs:
            return render_template('./quiz.html', quizes= by_quizs)
        



    return redirect(url_for("admin.admin_dashboard"))



def get_sub(id):
    s = Subject.query.filter_by(id = id).first()
    return s


@admin.route("/edit_sub/<id>", methods=['GET','POST'])
@login_required
def edit_sub(id):
    s = get_sub(id)
    # print(s)
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        s.name = name
        s.description = description
        db.session.commit()

        return redirect(url_for("admin.admin_dashboard"))
    return render_template("edit_sub.html", sub = s)


@admin.route("/delete_sub/<id>", methods=['GET','POST'])
@login_required
def delete_sub(id):
    s = get_sub(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("admin.admin_dashboard"))





def get_chap(id):
    c = Chapter.query.filter_by(id = id).first()
    return c


@admin.route("/edit_chap/<id>", methods=['GET','POST'])
@login_required
def edit_chap(id):
    c = get_chap(id)
    
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        
        c.name = name
        c.description = description

        db.session.commit()

        return redirect(url_for("admin.admin_dashboard"))
    return render_template("edit_chap.html", chap = c)





@admin.route("/delete_chap/<id>", methods=['GET','POST'])
@login_required
def delete_chap(id):
    c = get_chap(id)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for("admin.admin_dashboard"))





def get_quiz(id):
    q = Quiz.query.filter_by(id = id).first()
    return q


@admin.route("/edit_quiz/<id>", methods=['GET','POST'])
@login_required
def edit_quiz(id):
    q = get_quiz(id)
    # print(s)
    if request.method == "POST":
        date_time_str = request.form.get("date_time")
        duration_str = request.form.get("duration")
        score = request.form.get("score")

        if len(duration_str) == 5:
            duration_str += ":00"

        
        duration = datetime.strptime(duration_str, "%H:%M:%S").time()
        date_time = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M")

        q.duration = duration
        q.date_time = date_time
        q.score = score

        db.session.commit()

        return redirect(url_for("admin.quiz"))
    
    return render_template("edit_quiz.html", quiz = q)


@admin.route("/delete_quiz/<id>", methods=['GET','POST'])
@login_required
def delete_quiz(id):
    q = get_quiz(id)
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("admin.quiz"))




def get_que(id):
    q = Question.query.filter_by(id = id).first()
    return q


@admin.route("/edit_que/<id>", methods=['GET','POST'])
@login_required
def edit_que(id):
    q = get_que(id)
    # print(s)
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        option1 = request.form.get("op1")
        option2 = request.form.get("op2")
        option3 = request.form.get("op3")
        option4 = request.form.get("op4")
        correct_option = request.form.get("correct_option")
        
        q.name = name
        q.description = description
        q.option1 = option1 
        q.option2 = option2 
        q.option3 = option3 
        q.option4 = option4 
        q.correct_option = correct_option 

        db.session.commit()

        return redirect(url_for("admin.quiz"))
    return render_template("edit_que.html", que = q)


@admin.route("/delete_que/<id>", methods=['GET','POST'])
@login_required
def delete_que(id):
    q = get_que(id)

    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("admin.quiz"))



















# user routes


@user.route('/user_dashboard')
@login_required
def user_dashboard():
    quizs = Quiz.query.all()
    curr_dt = datetime.now()
    return render_template('user_dashboard.html', quizs=quizs, curr_dt=curr_dt)






@user.route('/view_quiz/<id>')
@login_required
def view_quiz(id):
    quiz = Quiz.query.filter_by(id=id).first()
    return render_template('quiz_details.html', quiz=quiz)





def get_scores(user, q):
    scores = Score.query.filter_by(user_id=user.id, quiz_id=q.id).order_by(Score.time_stamp_of_attempt).all()
    return scores

def get_subs():
    subs = Subject.query.all()
    return subs





def get_users_score_summary(quizes):
    # check folder exists or not exists
    image_folder = "./static/images/summary"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    
    # List to hold relative paths of saved images
    image_paths = []  
    
    for i, q in enumerate(quizes):
        scores = get_scores(current_user, q)
        
        # Extract time stamps and corresponding scores
        x_values = [s.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S') for s in scores]
        y_values = [s.score for s in scores]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker="o", linestyle="-", color="blue")
        plt.title(f"Performance in Quiz-{q.id} Chap : {q.chapter.name}")
        plt.xlabel("Time")
        plt.ylabel("Score")
        plt.gcf().autofmt_xdate()
        plt.grid(True)
        plt.tight_layout()
        
        # Save image with a unique name
        filename = f"users_score_summary_{i}.jpeg"
        filepath = os.path.join(image_folder, filename)
        plt.savefig(filepath)
        plt.close()  
        
        # Save the relative path (without the dot)
        image_paths.append(f"static/images/summary/{filename}")
        
    return image_paths






def get_subs_chaps_summary():
    subs = get_subs()
    
    summary = {s.name: len(s.chaps) for s in subs}
    x_names = list(summary.keys())
    y_scores = list(summary.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x_names, y_scores, color=["red", "blue", "green", "purple", "orange"])
    plt.title("Subjects Chapters Summary")
    plt.xlabel("Subjects")
    plt.ylabel("Chapters")
    
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom'
        )
        
    plt.tight_layout()
    image_folder = "./static/images/summary"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    filename = "subs_chaps_summary.jpeg"
    filepath = os.path.join(image_folder, filename)
    plt.savefig(filepath)
    plt.close()
    
    return f"static/images/summary/{filename}"




@user.route('/user_summary')
@login_required
def user_summary():
    user = User_Info.query.get(current_user.id)
    quizes_by_user = user.quizs

    quiz_image_paths = get_users_score_summary(quizes_by_user)
    subs_chaps_image_path = get_subs_chaps_summary()
    
    return render_template('user_summary.html',
                           quizzes=quizes_by_user,
                           quiz_image_paths=quiz_image_paths,
                           subs_chaps_image_path=subs_chaps_image_path)

















@user.route("/quiz/<int:quiz_id>/question/<int:q_no>")
@login_required
def get_question(quiz_id, q_no):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    quiz.is_attempted = True
    quiz.user_id = current_user.id
    db.session.commit()

    if not questions:
        abort(404)
    
    if q_no == 1:
        new_score = Score(
            user_id=current_user.id,
            quiz_id=quiz_id,
            time_stamp_of_attempt=datetime.utcnow(),
            score=0
        )
        db.session.add(new_score)
        db.session.commit()
        session['current_score_id'] = new_score.id
    
    if q_no > len(questions):
        return redirect(url_for("user.quiz_summary", quiz_id=quiz_id))
    
    question = questions[q_no - 1]
    return render_template("question.html", question=question, q_no=q_no, total=len(questions))





@user.route("/quiz/<int:quiz_id>/answer", methods=["POST"])
@login_required
def submit_answer(quiz_id):

    selected_option = -1
    is_correct = False

    current_score_id = session.get('current_score_id')
    if not current_score_id:
        return redirect(url_for('user.get_question', quiz_id=quiz_id, q_no=1))
    
    score_entry = Score.query.get(current_score_id)
    if not score_entry:
        session.pop('current_score_id', None)
        return redirect(url_for('user.get_question', quiz_id=quiz_id, q_no=1))
    
    
    if request.form.get("q_no"):
        q_no = int(request.form.get("q_no"))

    if request.form.get("selected_option"):
        selected_option = int(request.form.get("selected_option"))
        
    question = Question.query.get(request.form.get("question_id"))
    if question:
        is_correct = (question.correct_option == selected_option)
    
    if is_correct:
        score_entry.score += 10
        db.session.commit()
    
    return redirect(url_for("user.get_question", quiz_id=quiz_id, q_no=q_no + 1))







@user.route("/quiz/<int:quiz_id>/summary")
@login_required
def quiz_summary(quiz_id):
    current_score_id = session.get('current_score_id')
    if not current_score_id:
        return redirect(url_for('user.get_question', quiz_id=quiz_id, q_no=1))

    score_entry = Score.query.get(current_score_id)
    if not score_entry:
        session.pop('current_score_id', None)
        return redirect(url_for('user.get_question', quiz_id=quiz_id, q_no=1))

    
    if score_entry.score > current_user.user_score:
        current_user.user_score = score_entry.score
        db.session.commit()

    session.pop('current_score_id', None)

    
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if not quiz:
        flash("Quiz not found.", "danger")
        return redirect(url_for("user.dashboard")) 

    
    max_score_raw = db.session.query(func.max(Score.score)).filter(Score.quiz_id == quiz_id, Score.user_id == current_user.id).scalar() or 0
    print(max_score_raw)
    
    if quiz.score > 0:
        max_score = int((max_score_raw * 100) / (len(quiz.questions) * 10))
    else:
        max_score = 0  

    print(max_score)

    quiz.quiz_maxm_score = int((quiz.score * max_score) /100)
    db.session.commit()

    # \n Your Score for thhis Quiz :{score_entry.score}
    flash(f"Your Max Score in % : {max_score} ","info")
    return redirect(url_for("user.quizes"))
    # return render_template("question.html", current_quiz_score=score_entry.score, overall_max_score=max_score)













@login_required
def search_by_quiz_score(s):
    quizs = Quiz.query.filter(Quiz.score.ilike(f"%{s}%")).all()     
    return quizs


@login_required
def search_by_quiz_date(s):
    quizs = Quiz.query.filter(Quiz.date_time.ilike(f"%{s}%")).all()     
    return quizs





@user.route("/usr_search", methods=['POST', 'GET'])
@login_required
def usr_search():
    if request.method == "POST":

        search_txt = request.form.get('search_txt')

        curr_dt = datetime.now()

        by_score = search_by_quiz_score(search_txt)
        by_date = search_by_quiz_date(search_txt)
        print(by_score)
        print(by_date)

        if by_score:
            print(by_score)
            return render_template('./user_dashboard.html', quizs = by_score, curr_dt = curr_dt)
        elif by_date:
            return render_template('./user_dashboard.html', quizs = by_date, curr_dt = curr_dt)
        
        
    return redirect(url_for("user.user_dashboard"))




@user.route("/subjects")
@login_required
def subjects():
    subs = Subject.query.all()
    return render_template('subjects.html', subs = subs)

@user.route("/quizes")
@login_required
def quizes():
    quizes = Quiz.query.all()
    return render_template('quizes.html', quizes = quizes)

@user.route("/detail_sub/<sid>")
@login_required
def detail_sub(sid):
    sub = Subject.query.filter_by(id = sid).first()
    print(sub)
    return render_template('detail_sub.html', sub = sub)





# database routes
@data.route("/users")
@login_required
def users():
    user = User_Info.query.all()
    curr_dt = datetime.now()
    return render_template('user_list.html', users = user)


@data.route('/search')
@login_required
def search():
    user = User_Info.query.all()
    curr_dt = datetime.now()
    return render_template('user_dashboard.html', users = user, curr_dt = curr_dt)
