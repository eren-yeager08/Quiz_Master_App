from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, default=1)
    full_name = db.Column(db.String(255), nullable=False)
    qualification = db.Column(db.String(255), nullable=True)

    scores = db.relationship("Score", cascade="all,delete", backref="user", lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    chapters = db.relationship("Chapter", cascade="all,delete", backref="subject", lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)

    quizzes = db.relationship("Quiz", cascade="all,delete", backref="chapter", lazy=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.String(50), nullable=False)
    no_of_questions = db.Column(db.Integer, nullable=False) 

    questions = db.relationship("Question", cascade="all,delete", backref="quiz", lazy=True)
    scores = db.relationship("Score", cascade="all,delete", backref="quiz", lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(200), nullable=False)  
    option2 = db.Column(db.String(200), nullable=False) 
    option3 = db.Column(db.String(200), nullable=False)  
    option4 = db.Column(db.String(200), nullable=False)  
    correct_option = db.Column(db.String(200), nullable=False) 

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)