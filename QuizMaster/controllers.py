from flask import render_template, flash, redirect, session, request, url_for
from . import app, db
from .models import Users, Subjects, Chapters, Quizzes, Questions, Scores
from datetime import datetime, date


 


@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email =email, password=password).first()
        if user:
            if user.is_admin:
                session['admin_id'] = user.id
                session['is_admin'] = user.is_admin
                flash('Login Success!', 'success')
                return redirect('/admin_dashboard')
            else:
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                flash('Login Success!', "success")
                return redirect('/quiz_list')
        else:
            flash('Invalid credentials', "error")
            return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        fullname = request.form['fullname']
        qualification = request.form['qualification']
        dob = request.form['dob']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        user = Users(username=username, email=email, password=password, fullname=fullname, qualification=qualification, dob=dob, is_admin=False)
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful! Please login.", "success")
        return redirect(url_for('login'))
        
@app.route('/view_subjects', methods=['GET'])
def view_subjects():
    if session.get('is_admin'):
        print(session)
        subjects = Subjects.query.all()
        return render_template('view_subjects.html', all_subjects= subjects)
    return redirect('/login')

@app.route('/quiz_list', methods=['GET', 'POST'])
def quiz_list():
    if 'user_id' in session:
        quizzes = Quizzes.query.all()
        user = Users.query.filter_by(id=session['user_id']).first()
        return render_template('quiz_list.html', quizzes = quizzes, user=user)
    return redirect('/login')

@app.route('/create_subject', methods = ['GET', 'POST'])
def create_subject():
    if session.get('is_admin'):
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            new_subject = Subjects(name=name, description=description)
            db.session.add(new_subject)
            db.session.commit()
            return redirect('/view_subjects')
        else:
            return render_template('create_subject.html')
    return redirect('/login')

@app.route('/edit_subject/<int:subject_id>', methods = ['GET', 'POST'])
def edit_subject(subject_id):
    if session.get('is_admin'):
        subject = Subjects.query.filter_by(id = subject_id).first()
        if not subject:
            flash('Subject not found', 'error')
            return redirect('/view_subjects')
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            subject.name=name 
            subject.description=description
            db.session.commit()
            return redirect('/view_subjects')
        else:
            return render_template('edit_subject.html', subject=subject)
    return redirect('/login')

@app.route('/delete_subject/<int:subject_id>', methods = ['GET'])
def delete_subject(subject_id):
    if session.get('is_admin'):
        subject = Subjects.query.filter_by(id = subject_id).first()
        if not subject:
            flash('Subject not found', 'error')
            return redirect('/admin_dashboard')
        db.session.delete(subject)
        db.session.commit()
        return redirect('/view_subjects')
    return redirect('/login')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/create_chapter/<int:subject_id>', methods = ['GET', 'POST'])
def create_chapter(subject_id):
    if session.get('is_admin'):
        subject = Subjects.query.filter_by(id=subject_id).first()
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            new_chapter = Chapters(name=name, description=description, subject_id= subject_id)
            db.session.add(new_chapter)
            db.session.commit()
            return redirect(f'/view_chapters/{subject_id}')
        else:
            return render_template('create_chapter.html', subject=subject)
    return redirect('/login')

@app.route('/edit_chapter/<int:chapter_id>', methods = ['GET', 'POST'])
def edit_chapter(chapter_id):
    if session.get('is_admin'):
        chapter = Chapters.query.filter_by(id = chapter_id).first()
        subject = Subjects.query.filter_by(id = chapter.subject_id).first()
        if not chapter:
            flash('Chapter not found', 'error')
            return redirect('/admin_dashboard')
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            chapter.name=name 
            chapter.description=description
            db.session.commit()
            return redirect(f'/view_chapters/{subject.id}')
        else:
            return render_template('edit_chapter.html', chapter=chapter)
    return redirect('/login')

@app.route('/delete_chapter/<int:chapter_id>', methods = ['GET'])
def delete_chapter(chapter_id):
    if session.get('is_admin'):
        chapter = Chapters.query.filter_by(id = chapter_id).first()
        if not chapter:
            flash('Chapter not found', 'error')
            return redirect('/admin_dashboard')
        db.session.delete(chapter)
        db.session.commit()
        return redirect(f'/view_chapters/{chapter.subject_id}')
    return redirect('/login')

@app.route('/view_chapters/<int:subject_id>')
def view_chapters(subject_id):
    if session.get('is_admin'):
        subject = Subjects.query.filter_by(id=subject_id).first()
        if not subject:
            flash('Subject not found', 'error')
            return redirect('/admin_dashboard')
        chapters = Chapters.query.filter_by(subject_id=subject_id).all()
        return render_template('view_chapters.html', subject= subject, chapters=chapters)
    return redirect('/login')

@app.route('/view_quizzes/<int:chapter_id>')
def view_quizzes(chapter_id):
    if session.get('is_admin'):
        chapter = Chapters.query.filter_by(id=chapter_id).first()
        if not chapter:
            flash('Chapter not found', 'error')
            return redirect('/admin_dashboard')
        quizzes = Quizzes.query.filter_by(chapter_id = chapter_id).all()
        return render_template('view_quizzes.html', chapter= chapter, quizzes=quizzes)
    return redirect('/login')
@app.route('/create_quiz/<int:chapter_id>', methods = ['GET', 'POST'])
def create_quiz(chapter_id):
    if session.get('is_admin'):
        chapter = Chapters.query.filter_by(id=chapter_id).first()
        if request.method == 'POST':
            name = request.form['name']
            date_of_quiz = request.form['date_of_quiz']
            time_duration = request.form['time_duration']
            remarks = request.form['remarks']

            doq = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()

            new_quiz = Quizzes(name=name, date_of_quiz=date_of_quiz,time_duration=time_duration,remarks=remarks, chapter_id= chapter_id)
            db.session.add(new_quiz)
            db.session.commit()
            return redirect(f'/view_quizzes/{chapter_id}')
        else:
            return render_template('create_quiz.html', chapter=chapter)
    return redirect('/login')


@app.route('/edit_quiz/<int:quiz_id>', methods = ['GET', 'POST'])
def edit_quiz(quiz_id):
    if session.get('is_admin'):
        quiz = Quizzes.query.filter_by(id = quiz_id).first()
        chapter = Chapters.query.filter_by(id = quiz.chapter_id).first()
        if not quiz:
            flash('Quiz not found', 'error')
            return redirect('/admin_dashboard')
        if request.method == 'POST':
            name = request.form['name']
            date_of_quiz = request.form['date_of_quiz']
            time_duration = request.form['time_duration']
            remarks = request.form['remarks']

            doq = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()

            quiz.name=name 
            quiz.date_of_quiz=doq
            quiz.time_duration=time_duration 
            quiz.remarks=remarks
            
            db.session.commit()
            return redirect(f'/view_quizzes/{chapter.id}')
        else:
            return render_template('edit_quiz.html', quiz=quiz)
    return redirect('/login')

@app.route('/delete_quiz/<int:quiz_id>', methods = ['GET'])
def delete_quiz(quiz_id):
    if session.get('is_admin'):
        quiz = Quizzes.query.filter_by(id = quiz_id).first()
        if not quiz:
            flash('Quiz not found', 'error')
            return redirect('/admin_dashboard')
        db.session.delete(quiz)
        db.session.commit()
        return redirect(f'/view_quizzes/{quiz.chapter_id}')
    return redirect('/login')


@app.route('/view_questions/<int:quiz_id>')
def view_questions(quiz_id):
    if session.get('is_admin'):
        quiz = Quizzes.query.filter_by(id=quiz_id).first()
        if not quiz:
            flash('Quiz not found', 'error')
            return redirect('/admin_dashboard')
        questions = Questions.query.filter_by(quiz_id = quiz_id).all()
        return render_template('view_questions.html', quiz= quiz, questions=questions)
    return redirect('/login')

@app.route('/create_question/<int:quiz_id>', methods = ['GET', 'POST'])
def create_question(quiz_id):
    if session.get('is_admin'):
        quiz = Quizzes.query.filter_by(id=quiz_id).first()
        if request.method == 'POST':
            question_statement = request.form['question_statement']
            option1 = request.form['option1']
            option2 = request.form['option2']
            option3 = request.form['option3']
            option4 = request.form['option4']
            answer = request.form['answer']

            new_question = Questions(question_statement=question_statement, option1=option1, option2=option2, option3=option3, option4=option4, answer=answer, quiz_id= quiz_id)
            db.session.add(new_question)
            db.session.commit()
            return redirect(f'/view_questions/{quiz_id}')
        else:
            return render_template('create_question.html', quiz=quiz)
    return redirect('/login')


@app.route('/edit_question/<int:question_id>', methods = ['GET', 'POST'])
def edit_question(question_id):
    if session.get('is_admin'):
        question = Questions.query.filter_by(id = question_id).first()
        
        if not question:
            flash('Question not found', 'error')
            return redirect('/admin_dashboard')
        quiz = Quizzes.query.filter_by(id = question.quiz_id).first()
        if request.method == 'POST':
            question_statement = request.form['question_statement']
            option1 = request.form['option1']
            option2 = request.form['option2']
            option3 = request.form['option3']
            option4 = request.form['option4']
            answer = request.form['answer']

            question.question_statement = question_statement
            question.option1 = option1
            question.option2 = option2
            question.option3 = option3
            question.option4 = option4
            question.answer = answer
            
            db.session.commit()
            return redirect(f'/view_questions/{quiz.id}')
        else:
            return render_template('edit_question.html', question=question)
    return redirect('/login')

@app.route('/delete_question/<int:question_id>', methods = ['GET'])
def delete_question(question_id):
    if session.get('is_admin'):
        question = Questions.query.filter_by(id = question_id).first()
        if not question:
            flash('Question not found', 'error')
            return redirect('/admin_dashboard')
        db.session.delete(question)
        db.session.commit()
        return redirect(f'/view_questions/{question.quiz_id}')
    return redirect('/login')

@app.route('/start_quiz/<int:quiz_id>')
def start_quiz(quiz_id):
    if 'user_id' in session:
        quiz = Quizzes.query.filter_by(id = quiz_id).first()
        questions = Questions.query.filter_by(quiz_id = quiz_id).all()

        if not quiz:
            flash("Quiz not found", 'danger')
            return redirect("/quiz_list")

        if len(questions) == 0:
            flash("No questions found for this quiz", 'info')
            return redirect("/quiz_list")
        

        if date.today() < datetime.strptime(quiz.date_of_quiz, "%Y-%m-%d").date():
            flash("The quiz is only available on or after its scheduled date", 'info')
            return redirect("/quiz_list")
        
        session['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        user = Users.query.filter_by(id = session['user_id']).first()
        return redirect(f"/quiz/{quiz_id}" )
    return redirect('/login')

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz_page(quiz_id):
    if 'user_id' in session:
        quiz = Quizzes.query.filter_by(id = quiz_id).first()
        questions = Questions.query.filter_by(quiz_id = quiz_id).all()
        user = Users.query.filter_by(id = session['user_id']).first()
        return render_template("quiz.html", quiz=quiz, questions=questions, user=user)
    return redirect('/login')



@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    if 'user_id' in session:
        questions = Questions.query.filter_by(quiz_id=quiz_id).all()
        user = Users.query.get(session['user_id'])
        score = 0

        for question in questions:
            selected_answer = request.form.get(f'question_{question.id}')
            correct_answer_text = getattr(question, f'option{question.answer[-1]}')
            if selected_answer == correct_answer_text:
                score += 1

        new_score = Scores(
            total_scored=score,
            time_stamp_of_attempt=session['timestamp'],
            user_id=user.id,
            quiz_id=quiz_id
        )
        db.session.add(new_score)
        db.session.commit()

        flash(f'Your score is {score}/{len(questions)}', 'info')

        session['quiz_result'] = {'score': score, 'total': len(questions)}

        return redirect(url_for('quiz_result', quiz_id=quiz_id))

    return redirect('/login')

@app.route('/quiz_result/<int:quiz_id>')
def quiz_result(quiz_id):
    if 'quiz_result' not in session:
        return redirect(url_for('quiz_list'))
    
    user = Users.query.get(session['user_id'])
    result = session.pop('quiz_result')
    return render_template('result.html', score=result['score'], total=result['total'], user=user)

@app.route('/user_history')
def user_history():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Users.query.get(user_id)
        scores = Scores.query.filter_by(user_id=user_id).all()
        return render_template('user_history.html', scores=scores, user=user)
    return redirect('/login')



@app.route('/admin_dashboard/search', methods=['GET'])
def admin_search():
    if "admin_id" in session:
        search_query = request.args.get('search_query', '').strip()
        search_type = request.args.get('search_type', 'all')  

        if not search_query:  
            return redirect('/admin')

        users = Users.query.filter(Users.username.ilike(f'%{search_query}%')).all()
        subjects = Subjects.query.filter(Subjects.name.ilike(f'%{search_query}%')).all()
        chapters = Chapters.query.filter(Chapters.name.ilike(f'%{search_query}%')).all()
        quizzes = Quizzes.query.filter(Quizzes.name.ilike(f'%{search_query}%')).all()
        
        return render_template('admin_search.html', users=users, subjects=subjects, chapters=chapters, quizzes=quizzes, search_query=search_query, search_type=search_type)

    return redirect("/login")

@app.route('/admin_history')
def admin_history():        
    if 'admin_id' not in session:
        return redirect('/login')
    
    scores = Scores.query.all()[::-1]
    return render_template('admin_history.html', scores=scores)


@app.route('/admin_dashboard')
def admin_summary():
    if 'admin_id' not in session:
        return redirect("/login")    

    
    users = Users.query.all()
    subjects = Subjects.query.all()
    chapters = Chapters.query.all()

    
    all_questions = Questions.query.all()
    total_questions_dict = {}
    for question in all_questions:
        quiz_id = question.quiz_id
        total_questions_dict[quiz_id] = total_questions_dict.get(quiz_id, 0) + 1

    
    user_avg_scores = {}
    all_scores = Scores.query.all()
    
    user_total_scores = {}  
    user_quiz_count = {}    

    for score in all_scores:
        user_id = score.user_id
        quiz_id = score.quiz_id

        total_questions = total_questions_dict.get(quiz_id, 1)  
        percentage_score = (score.total_scored / total_questions) * 100 if total_questions else 0

        user_total_scores[user_id] = user_total_scores.get(user_id, 0) + percentage_score
        user_quiz_count[user_id] = user_quiz_count.get(user_id, 0) + 1

    for user_id in user_total_scores:
        user_avg_scores[user_id] = round(user_total_scores[user_id] / user_quiz_count[user_id], 2)

    
    month_wise_quizzes = {}
    all_quizzes = Quizzes.query.all()

    for quiz in all_quizzes:
        date_obj = datetime.strptime(quiz.date_of_quiz, "%Y-%m-%d")  
        month = date_obj.strftime("%b")  
        month_wise_quizzes[month] = month_wise_quizzes.get(month, 0) + 1

    
    subject_data = {}
    for quiz in all_quizzes:
        subject_name = quiz.chapter_name.subject_name.name  
        subject_data[subject_name] = subject_data.get(subject_name, 0) + 1

    
    score_data = {}
    quiz_scores = {}

    for score in all_scores:
        quiz_name = score.quiz_name.name
        quiz_scores[quiz_name] = quiz_scores.get(quiz_name, []) + [score.total_scored]

    for quiz_name, scores in quiz_scores.items():
        max_score = max(scores) if scores else 1  
        avg_score = sum(scores) / len(scores) if scores else 0
        score_data[quiz_name] = round((avg_score / max_score) * 100 if max_score else 0, 2)

    return render_template(
        'admin_dashboard.html',
        users=users,
        avg_scores_dict={user.id: user_avg_scores.get(user.id, 0.0) for user in users},
        month_data=month_wise_quizzes,
        subject_data=subject_data,
        score_data=score_data,
        subjects=subjects,
        chapters=chapters,
    )

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect("/login")

    user_id = session['user_id']
    user = Users.query.get(user_id)

    
    all_questions = Questions.query.all()
    total_questions_dict = {}
    for question in all_questions:
        quiz_id = question.quiz_id
        total_questions_dict[quiz_id] = total_questions_dict.get(quiz_id, 0) + 1

    
    user_scores = Scores.query.filter_by(user_id=user_id).all()

    total_score = 0
    total_quizzes = len(user_scores)

    quiz_scores = {}
    for score in user_scores:
        quiz_id = score.quiz_id
        quiz_name = score.quiz_name.name
        total_questions = total_questions_dict.get(quiz_id, 1)  

        percentage_score = (score.total_scored / total_questions) * 100 if total_questions else 0
        quiz_scores[quiz_name] = round(percentage_score, 2)

        total_score += percentage_score

    avg_score = round(total_score / total_quizzes, 2) if total_quizzes else 0

    
    month_wise_quizzes = {}
    for score in user_scores:
        date_obj = datetime.strptime(score.quiz_name.date_of_quiz, "%Y-%m-%d")
        month = date_obj.strftime("%b")
        month_wise_quizzes[month] = month_wise_quizzes.get(month, 0) + 1

    return render_template(
        "user_dashboard.html",
        user=user,
        avg_score=avg_score,
        quiz_scores=quiz_scores,
        month_data=month_wise_quizzes,
    )
    
