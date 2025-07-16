from flask import Flask, render_template, redirect, url_for, request, flash
from db import get_session
from models import Task, Comment, User
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from bcrypt import checkpw, hashpw, gensalt
import os
from dotenv import load_dotenv

load_dotenv(".env")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# help to get user info when he already logged
@login_manager.user_loader
def load_user(user_id):
    with get_session() as session:
        return session.get(User, user_id)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        with get_session() as session:
            new_user = User(
                username=username,
                password=hashed_password
            )
            session.add(new_user)
            session.commit()
            return render_template('login.html')
    elif request.method == 'GET':
        return render_template('registration.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with get_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user and checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                login_user(user)
                flash('Вы успешно зашли в систему ', 'success')
                return redirect(url_for('index'))
            else:
                flash('Неверное имя пользователя или пароль', 'error')
                return render_template('login.html')
    elif request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('index.html')
        else:
            return render_template('login.html')


@app.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return render_template('login.html')

    


@app.route('/')
@login_required
def redirect_to_tasks():
    return redirect(url_for('index'))



@app.route('/index/', methods=['GET'])
@login_required
def index():
    with get_session() as session:
        user_tasks = session.query(Task).filter_by(user_id=current_user.id)
        sort_by = request.args.get('sort_by', default='priority')
        sorted_tasks =  user_tasks.order_by(sort_by).all()
        return render_template(
            'index.html',
            sorted_tasks=sorted_tasks
        )


@app.route('/task/<int:task_id>/', methods=['GET', 'POST'])
@login_required
def task(task_id):
    with get_session() as session:
        if request.method == 'GET':
            task = session.get(Task, task_id)
            comments = session.query(Comment).filter_by(task_id=task_id).all()
            return render_template(
                'task.html',
                task=task,
                comments=comments
            )
        elif request.method == 'POST':
            comment_text = request.form.get('comment')
            if comment_text:
                new_comment = Comment(
                    task_id=task_id,
                    content=comment_text,
                    user_id=current_user.id
                )
                session.add(new_comment)
                session.commit()
            return redirect(url_for('task', task_id=task_id))


@app.route('/index/add_task/', methods=['GET', 'POST'])
@login_required
def add_task():
    with get_session() as session:
        if request.method == 'POST':
                name = request.form.get('name')
                category = request.form.get('category')
                description = request.form.get('description')
                priority = request.form.get('priority')
                status = request.form.get('status')
                user_id = current_user.id

                new_task = Task(
                    name=name,
                    category=category,
                    description=description,
                    priority=priority,
                    status=status,
                    user_id=user_id
                )
                session.add(new_task)
                session.commit()
                return redirect(url_for('index'))
        elif request.method == 'GET':
            return render_template('add_task.html')
        

@app.route('/index/task/edit_task/<int:task_id>/', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    with get_session() as session:
        task = session.get(Task, task_id)
        if request.method == 'GET':
            return render_template('edit_task.html', task=task)
        elif request.method == 'POST':
            task.name = request.form.get('name')
            task.category = request.form.get('category')
            task.description = request.form.get('description')
            task.priority = int(request.form.get('priority'))
            task.status = request.form.get('status')
            session.commit()
            return redirect(url_for('task', task_id=task_id))


@app.route('/index/task/delete_task/<int:task_id>/', methods=['POST'])
@login_required
def delete_task(task_id):
    with get_session() as session:
        task = session.get(Task, task_id)
        session.delete(task)
        session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
