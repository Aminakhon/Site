from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
CORS(app)
db = SQLAlchemy(app)
Migrate(app, db)

# модель для хранения задачи
class Bads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False, default=False)
    time = db.Column(db.String(80), nullable=False)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False, default=False)
    phone = db.Column(db.String(100), nullable=False, default=False)
    email = db.Column(db.String(100), nullable=False, default=False)

class User_Bad(db.Model):


# презентер для задачи
def present_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "is_done": task.is_done
    }

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/')
def main():
    return render_template('hello.html')

@app.route('/login', methods=['POST'])

def login():
    sth = False
    login = request.form.get('login')
    password = request.form.get('password')
    user = User.query.filter_by(login=login).first()

    if user and user.password == password:
        session['login'] = request.form.get('login')
        session['password'] = request.form.get('password')
        return redirect('/page')

    else:
        return render_template('login.html', error='Что-то не так')

@app.route('/reg')
def reg():
    return render_template('reg.html', error = '')


@app.route('/reg', methods=['POST'])
def regin():
    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')
    user = User.query.filter_by(login=login).first()
    if user:
        return render_template('reg.html', error='Пользователь с данным логином уже зарегистрирован')
    elif login and password and name:

        user = User(login=login, name=name, password=password)

        db.session.add(user)
        db.session.commit()
        return redirect('/page')
    else:
        return render_template('reg.html', error='Вы не можете иметь пустой логин/пароль/имя')


# получаем все задачи
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return [present_task(task) for task in tasks]




@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()

    # если нет названия - возвращаем ошибку
    if not data.get('title'):
        return jsonify({'error': 'no title'}), 400

    task = Task(title=data['title'])
    db.session.add(task)
    db.session.commit()

    return present_task(task)

@app.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def get_change(task_id):
    data = request.get_json()
    title = data.get('title')
    is_done = data.get('is_done')
    if not title or not Task.query.filter_by(id=task_id).first():
        return jsonify({'error': 'no title'}), 400
    task = Task.query.filter_by(id=task_id).first()
    task.is_done = is_done
    task.title = title
    db.session.commit()
    return present_task(task)

# при запросе главной страницы возвращаем html файл с фронтендом как файл (без шаблонизатора)
@app.route('/')
def index():
    return send_file('index.html')


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def del_tasks(task_id):
    task = Task.query.filter_by(id=task_id).first()

    if not task:
        return jsonify({'reason': 'Task not found'}), 400
    # удаляем запись
    db.session.delete(task)
    # сохраняем изменения
    db.session.commit()

    # возвращаем успешный ответ
    return jsonify({'success': True})

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Отдаем пустой ответ без ошибок
if __name__ == '__main__':
    app.run(port=8080)