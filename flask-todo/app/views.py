from flask import render_template, redirect, request
from app import app
from app.models import Todo
from sqlalchemy import desc

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class TodoForm(FlaskForm):
    content = StringField('content', validators=[DataRequired(), Length(min=5, max=20)])

@app.route('/')
def index():
    form = TodoForm()
    todos = Todo.query.order_by(desc(Todo.time)).all()
    return render_template('index.html', todos=todos, form=form)

@app.route('/add', methods=['POST'])
def add():
    # form = TodoForm(request.form)
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(content=form.content.data)
        todo.save()
    todos = Todo.query.order_by(desc(Todo.time)).all()
    return render_template('index.html', todos=todos, form=form)
