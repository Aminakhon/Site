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
    try:
        # Проверка существования связи
        if User_Supplements.query.filter_by(user_id=user_id, supplement_id=sup_id).first():
            return redirect(f'/api/{user_id}/library')

        # Создание связи
        new_link = User_Supplements(user_id=user_id, supplement_id=sup_id)
        db.session.add(new_link)
        db.session.commit()

        return redirect(f'/api/{user_id}/timetable')

    except Exception as e:
        db.session.rollback()
        return redirect(f'/api/{user_id}/library')



@app.route('/api/<int:id>/profile', methods=['GET'])
def get_timetable(id):
    supplements = User_Supplements.query.filter_by(user_id=id)
    user = Users.query.filter_by(id=id).first()
    if not user:
        return redirect('/')
    return render_template('profile.html', supplements=supplements, user=user, user_id=id)

@app.route('/api/<int:id>/timetable/<int:sup_id>', methods=['POST'])
def del_sup(id, sup_id):
    if request.form.get('_method') == 'DELETE':
        supplement = User_Supplements.query.filter_by(supplement_id=sup_id, user_id=id).first()

    if not supplement:
        return jsonify({'reason': 'Supplement not found'}), 400
    # удаляем запись
    db.session.delete(supplement)
    # сохраняем изменения
    db.session.commit()
    return redirect(f'/api/{id}/timetable')

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Отдаем пустой ответ без ошибок
if __name__ == '__main__':
    app.run(port=8080)