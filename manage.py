from flask import Flask, request, jsonify, send_file, render_template, redirect, abort, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt

import jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
CORS(app)
db = SQLAlchemy(app)
Migrate(app, db)
app.secret_key = 'jrfasefasefgj'