from manage import db


class Supplements(db.Model):
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

class User_Supplements(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    supplement_id = db.Column(db.Integer, db.ForeignKey('supplement.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('Users', backref=db.backref('site', lazy=False))
    supplement = db.relationship('Supplements', backref=db.backref('site', lazy=True), lazy=False)