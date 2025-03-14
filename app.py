from manage import *
from models import *
from presents import *


# презентер для задачи


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
    user = Users.query.filter_by(login=login).first()

    if user and user.password == password:
        session['login'] = request.form.get('login')
        session['password'] = request.form.get('password')
        return redirect('/page')

    else:
        return render_template('login.html', error='Что-то не так')

@app.route('/register')
def reg():
    return render_template('reg.html', error = '')


@app.route('/register', methods=['POST'])
def regin():
    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')
    user = Users.query.filter_by(login=login).first()
    if user:
        return render_template('reg.html', error='Пользователь с данным логином уже зарегистрирован')
    elif login and password and name:

        user = Users(login=login, name=name, password=password)

        db.session.add(user)
        db.session.commit()
        return redirect('/api/profile/<user.id>')
    else:
        return render_template('reg.html', error='Вы не можете иметь пустой логин/пароль/имя')

@app.route('/api/profile/<int:id>')
def prof(id):
    user = Users.query.filter_by(id=id).first()
    present_user(user)
    return render_template('reg.html', error = '', user=user)

# получаем все задачи
@app.route('/api/library', methods=['GET'])
def get_supplements():
    supplements = Supplements.query.all()
    return render_template('library.html', supplements=supplements)






@app.route('/favicon.ico')
def favicon():
    return '', 204  # Отдаем пустой ответ без ошибок
if __name__ == '__main__':
    app.run(port=8080)