from flask import Flask,render_template,request,url_for,redirect
from models.models import *
from flask import current_app as app
from datetime import datetime

#starting route
@app.route("/")
def home():
    return render_template("index.html")

#admin login route
@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")

        usr=User.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role==0: #Existed and admin
            return redirect(url_for("admin_dashboard",name=uname))
        elif usr and usr.role==1: #Existed and user
            return redirect(url_for("user_dashboard",name=uname,id=usr.id))
        else:
            return render_template("login.html",msg="Invalid email or password. Please try again.")


    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        full_name=request.form.get("full_name")
        qualification=request.form.get("qualification")
     
        usr=User.query.filter_by(email=uname).first()
        if usr:
            return render_template("register.html",msg="This email is already registered. Please log in or use a different email.")

        new_usr=User(email=uname,password=pwd,full_name=full_name,qualification=qualification)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg1="Thank you for registering! Try logging in now.")

    return render_template("register.html")

#common route for admin
@app.route("/admin/<name>")
def admin_dashboard(name):
    subjects=get_subjects()
    return render_template("admin_dashboard.html",name=name,subjects=subjects)

#common route for user
@app.route("/user/<name>")
def user_dashboard():

    return render_template("user_dashboard.html")

@app.route("/subject/<name>",methods=["POST","GET"])
def add_subject(name):
    if request.method=="POST":
        sname=request.form.get("name")
        description=request.form.get("description")
 
        new_subject=Subject(name=sname, description=description)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))

    return render_template("add_subject.html",name=name)

@app.route("/chapter/<subject_id>/<name>",methods=["POST","GET"])
def add_chapter(name,subject_id):
    if request.method=="POST":
        cname=request.form.get("name")
        description=request.form.get("description")
 
        new_chapter=Chapter(name=cname, description=description,subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))

    return render_template("add_chapter.html",subject_id=subject_id,name=name)

@app.route("/edit_subject/<id>/<name>",methods=["GET","POST"])
def edit_subject(id,name):
    s=get_subject(id)
    if request.method=="POST":
        sname=request.form.get("sname")
        description=request.form.get("description")
        s.name=sname
        s.description=description
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    
    return render_template("edit_subject.html",subject=s,name=name)

@app.route("/delete_subject/<id>/<name>",methods=["GET","POST"])
def delete_subject(id,name):
    s=get_subject(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))

@app.route("/edit_chapter/<id>/<name>",methods=["GET","POST"])
def edit_chapter(id,name):
    c=get_chapter(id)

    if request.method=="POST":
        cname=request.form.get("cname")
        description=request.form.get("description")
        c.name=cname
        c.description=description
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    
    return render_template("edit_chapter.html",chapter=c,name=name)

@app.route("/delete_chapter/<id>/<name>",methods=["GET","POST"])
def delete_chapter(id,name):
    c=get_chapter(id)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))

@app.route("/quiz_management/<name>")
def quiz_management(name):
    chapters = Chapter.query.all()  # Fetch all chapters
    quizzes = Quiz.query.all()
    chapter_wise_quizzes = {}

    for chapter in chapters:
        quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
        if quizzes:
            chapter_wise_quizzes[chapter] = quizzes

    return render_template("quiz_management.html", name=name, chapter_wise_quizzes=chapter_wise_quizzes)
   
@app.route("/add_quiz/<name>", methods=["POST", "GET"])
def add_quiz(name):
    if request.method == "POST":
        cid = request.form.get("chapter_id")
        date_of_quiz = request.form.get("date_of_quiz")
        time_duration = request.form.get("time_duration")
        no_of_questions = request.form.get("no_of_questions")
        date = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()

        new_quiz = Quiz(chapter_id=cid,date_of_quiz=date,no_of_questions=no_of_questions, time_duration=time_duration)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for("quiz_management", name=name))

    # If it's a GET request, fetch chapter details
    chapters = Chapter.query.all()
    return render_template("add_quiz.html", name=name,chapters=chapters)

@app.route("/edit_quiz/<id>/<name>",methods=["GET","POST"])
def edit_quiz(id, name):
    q=get_quiz(id)
   
    if request.method=="POST":
        cid = request.form.get("chapter_id")
        date_of_quiz = request.form.get("date_of_quiz")
        time_duration = request.form.get("time_duration")
        no_of_questions = request.form.get("no_of_questions")
        q.chapter_id=cid
        q.date=date_of_quiz
        q.time=time_duration
        q.total_questions=no_of_questions
        db.session.commit()
        return redirect(url_for("quiz_management",name=name))
    
    chapters = Chapter.query.all()
    return render_template("edit_quiz.html",name=name,quiz=q,chapters=chapters)

@app.route("/delete_quiz/<id>/<name>", methods=["GET", "POST"])
def delete_quiz(id, name):  
    q = get_quiz(id)
    if q:
        db.session.delete(q)
        db.session.commit()
    return redirect(url_for("quiz_management", name=name))

@app.route("/add_question/<quiz_id>/<name>", methods=["POST", "GET"])
def add_question(quiz_id, name):
    if request.method=="POST":
        question=request.form.get("question_statement")
        option1=request.form.get("option1")
        option2=request.form.get("option2")
        option3=request.form.get("option3")
        option4=request.form.get("option4")
        correct_option=request.form.get("correct_option")

        new_question=Question(question_statement=question,quiz_id=quiz_id,option1=option1,option2=option2,option3=option3,option4=option4,correct_option=correct_option)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for("quiz_management",name=name))
    
    return render_template("add_question.html", quiz_id=quiz_id ,name=name)

@app.route("/edit_question/<id>/<name>",methods=["GET","POST"])
def edit_question(id,name):
    q=get_question(id)

    if request.method=="POST":
        question=request.form.get("question_statement")
        option1=request.form.get("option1")
        option2=request.form.get("option2")
        option3=request.form.get("option3")
        option4=request.form.get("option4")
        correct_option=request.form.get("correct_option")
        q.question_statement=question
        q.option1=option1
        q.option2=option2
        q.option3=option3
        q.option4=option4
        q.correct_option=correct_option
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    
    return render_template("edit_question.html",question=q,name=name)

@app.route("/delete_question/<id>/<name>",methods=["GET","POST"])
def delete_question(id,name):
    q=get_question(id)
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("quiz_management",name=name))

def get_subjects():
    subjects=Subject.query.all()
    return subjects

# def get_chapters():
#     chapters=Chapter.query.all()
#     return chapters

# def get_quizzes():
#     quizzes=Quiz.query.all()
#     return quizzes

def get_subject(id):
    subject=Subject.query.filter_by(id=id).first()
    return subject

def get_chapter(id):
    chapter=Chapter.query.filter_by(id=id).first()
    return chapter

def get_quiz(id):
    quiz=Quiz.query.filter_by(id=id).first()
    return quiz

def get_question(id):
    question=Question.query.filter_by(id=id).first()
    return question
