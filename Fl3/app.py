from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Используйте SQLite для простоты
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Импортируйте модели из файла models.py
from models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт создан!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/')
def home():
    return "Главная страница"

if __name__ == '__main__':
    app.run(debug=True)
