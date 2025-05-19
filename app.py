from manage import *
from models import *
from presents import *


def presentsup(id):
    supplements = db.session.query(Supplements)\
                  .join(User_Supplements)\
                  .filter(User_Supplements.user_id == id)\
                  .all()
    return [present_supplement(sup) for sup in supplements]


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

    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id  # Сохраняем ID пользователя в сессии
        return redirect(f'/api/{user.id}/timetable')
    else:
        return render_template('login.html', error='Неверные учетные данные')

@app.route('/registred', methods=['GET'])
def reg():
    return render_template('reg.html', error = '')


@app.route('/registred', methods=['POST'])
def regin():
    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')

    if not all([login, password, name]):
        return render_template('reg.html', error='Все поля обязательны для заполнения')

    if Users.query.filter_by(login=login).first():
        return render_template('reg.html', error='Пользователь с таким логином уже существует')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = Users(login=login, name=name, password=hashed_password)

    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id  # Сохраняем ID пользователя в сессии
    return redirect(f'/api/{user.id}/timetable')

@app.route('/api/<int:id>/timetable')
def prof(id):
    user = Users.query.filter_by(id=id).first()
    present_user(user)
    notes = presentsup(id)
    return render_template('timetable.html', error = '', user=user, notes=notes, user_id=id)

# получаем все задачи
@app.route('/api/<int:id>/library', methods=['GET'])
def get_supplements(id):
    supplements = Supplements.query.all()
    return render_template('library.html', supplements=supplements, user_id=id)

@app.route('/api/<int:user_id>/library/<int:sup_id>', methods=['GET'])
def get_supplement(user_id, sup_id):
    supplement = Supplements.query.get_or_404(sup_id)
    return render_template('text.html',
                         supplement=supplement,
                         user_id=user_id)


@app.route('/api/<int:user_id>/library/<int:sup_id>', methods=['POST'])
def add_supplements(user_id, sup_id):
    supplement = Supplements.query.filter_by(id=sup_id)

    user = Users.query.filter_by(user_id=user_id, supplement_id=sup_id).first()

    if user:
        return render_template('library.html', error='БАД уже добавлен', user_id=user_id)

    user_supplement = User_Supplements(user_id=user_id, supplement_id=sup_id)

    db.session.add(user_supplement)
    db.session.commit()

    return redirect('/api/<user_id>/timetable')

@app.route('/api/<int:id>/profile', methods=['GET'])
def get_timetable(id):
    supplements = User_Supplements.query.filter_by(user_id=id)
    return render_template('profile.html', supplements=supplements, user_id=id)



@app.route('/favicon.ico')
def favicon():
    return '', 204  # Отдаем пустой ответ без ошибок
if __name__ == '__main__':
    app.run(port=8080)