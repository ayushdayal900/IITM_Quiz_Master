from datetime import datetime
from flask import Blueprint, abort, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from models.models import Quiz, Score, db, User_Info, Subject, Chapter, Question
from app import login_manager
# from models import db





# general routes
gen = Blueprint('general_routes', __name__)  
data = Blueprint('database_routes', __name__)  
admin = Blueprint('admin', __name__)  
user = Blueprint('user', __name__)  











# general routes
@gen.route('/')
def home():
    return render_template('index.html')



@gen.route('/logout')
def logout():

    logout_user()
    return redirect(url_for("general_routes.login"))



@gen.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        pwd   = request.form.get("password")
        usr = User_Info.query.filter_by(email=email, password=pwd).first()
        
        #existed and admin
        if usr and usr.role==0: 
            login_user(usr)
            return redirect(url_for("admin.admin_dashboard"))
        #existed and user
        elif usr and usr.role==1:
            login_user(usr)
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
@login_required
def admin_dashboard():
    subs = Subject.query.all()
    return render_template('admin_dashboard.html', subs = subs)


@admin.route('/summary')
@login_required
def summary():
    return render_template('summary.html')


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
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        
        chap = Chapter(name = name, description = description, subject_id = sid)

        db.session.add(chap)
        db.session.commit()

        return redirect(url_for("admin.admin_dashboard"))
    return render_template('add_chapter.html',sid=sid)



@admin.route('/add_quiz', methods=["POST", "GET"])
@login_required
def add_quiz():
    if request.method == "POST":
        # user_id = request.form.get("user_id")  
        user_role = 0
        chapter_id = request.form.get("chapter_id")  

        datetime_str = request.form.get("datetime")
        date_time = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")

        duration_str = request.form.get("duration")
        if len(duration_str) == 5:
            duration_str += ":00"

        duration = datetime.strptime(duration_str, "%H:%M:%S").time()

        score = request.form.get("score")

        quiz = Quiz(user_role = user_role,chapter_id=chapter_id,date_time=date_time,duration=duration,score=score)
        
        db.session.add(quiz)
        db.session.commit()

        return redirect(url_for("admin.quiz"))
    return render_template('add_quiz.html')




# @admin.route('/delete_quiz/<id>', methods=["POST", "GET"])
# def delete_quiz(id):
#     quiz = Quiz.query.filter_by(id == id).first()
#     db.session.delete(quiz)
#     db.session.commit()
#     return redirect(url_for("admin.admin_dashboard"))





@admin.route('/add_question/<cid>/<qid>', methods=["POST", "GET"])
@login_required
def add_question(cid,qid):

    chaps = Chapter.query.filter_by(id=cid).first()
    print(chaps)

    if request.method == "POST":
        chapter_id = request.form.get('cid')
        quiz_id = request.form.get('qid')
        name = request.form.get('name')
        description = request.form.get('description')

        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correct_option')

        
        que = Question(name = name, description = description, chapter_id = chapter_id, quiz_id=quiz_id, option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option)

        db.session.add(que)
        db.session.commit()

        return redirect(url_for("admin.quiz"))
    return render_template('add_question.html',cid = cid,qid = qid,chaps = chaps)



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
    return render_template('user_dashboard.html',quizs = quizs, curr_dt = curr_dt)

@user.route('/view_quiz/<id>')
@login_required
def view_quiz(id):
    quiz = Quiz.query.filter_by(id = id).first()
    return render_template('quiz_details.html',quiz = quiz)



# ///////////////////////////////////////////////////////
@user.route("/quiz/<int:quiz_id>/question/<int:q_no>")
@login_required
def get_question(quiz_id, q_no):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    if not questions:
        abort(404)
    
    # Start new attempt when accessing the first question
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
    current_score_id = session.get('current_score_id')
    if not current_score_id:
        return redirect(url_for('user.get_question', quiz_id=quiz_id, q_no=1))
    
    score_entry = Score.query.get(current_score_id)
    if not score_entry:
        session.pop('current_score_id', None)
        return redirect(url_for('user.get_question', quiz_id=quiz_id, q_no=1))
    
    q_no = int(request.form["q_no"])
    selected_option = int(request.form["selected_option"])
    question = Question.query.get(request.form["question_id"])
    is_correct = (question.correct_option == selected_option)
    
    if is_correct:
        score_entry.score += 1
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
    
    # Update user's maximum score
    if score_entry.score > current_user.user_score:
        current_user.user_score = score_entry.score
        db.session.commit()
    
    session.pop('current_score_id', None)
    return render_template("summary.html", score=score_entry.score, max_score=current_user.user_score)
# /////////////////////////////////////////////////////////////////////
@user.route('/scores')
@login_required
def scores():

    quizs = Quiz.query.all()
    # score = Score.query.filter_by(user_id = user_id).first()
    # user_scores = Score.query.filter_by(user_id=current_user.id).first()
    print(current_user.email)
    return render_template('scores.html',quizs = quizs)
    # return render_template('scores.html')









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
