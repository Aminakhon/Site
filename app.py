from manage import *
from models import *
from presents import *




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/')
def main():
    return render_template('hello.html')


@app.route('/login', methods=['GET'])
def login():
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def add_login():
    login = request.form.get('login')
    password = request.form.get('password')
    user = Users.query.filter_by(login=login).first()

    if user and user.password == password:
        return redirect('/api/<user.id>/profile')

    else:
        return render_template('login.html', error='Что-то не так')

@app.route('/registred', methods=['GET'])
def reg():
    return render_template('reg.html', error = '')


@app.route('/registred', methods=['POST'])
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
        return redirect('/api/<user.id>/profile')
    else:
        return render_template('reg.html', error='Вы не можете иметь пустой логин/пароль/имя')

@app.route('/api/<int:id>/profile')
def prof(id):
    user = Users.query.filter_by(id=id).first()
    present_user(user)
    return render_template('reg.html', error = '', user=user)

# получаем все задачи
@app.route('/api/<int:id>/library', methods=['GET'])
def get_supplements(id):
    supplements = Supplements.query.all()
    return render_template('library.html', supplements=supplements, id=id)

@app.route('/api/<int:user_id>/library/<int:sup_id>', methods=['POST'])
def add_supplements(user_id, sup_id):
    supplement = Supplements.query.filter_by(id=sup_id)

    user = Users.query.filter_by(user_id=user_id, supplement_id=sup_id).first()

    if user:
        return render_template('library.html', error='БАД уже добавлен')

    user_supplement = User_Supplements(user_id=user_id, supplement_id=sup_id)

    db.session.add(user_supplement)
    db.session.commit()

    return redirect('/api/<user_id>/timetable')

@app.route('/api/<int:id>/timetable', methods=['GET'])
def get_timetable(id):
    supplements = User_Supplements.query.filter_by(user_id=id)
    return render_template('timetable.html', supplements=supplements)



@app.route('/favicon.ico')
def favicon():
    return '', 204  # Отдаем пустой ответ без ошибок
if __name__ == '__main__':
    app.run(port=8080)