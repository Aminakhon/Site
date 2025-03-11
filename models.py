
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