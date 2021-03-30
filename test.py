# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask import session, redirect, url_for
from flask import flash
from flask_bootstrap import Bootstrap
#使用Flask-Moment本地化日期和时间
from flask_moment import Moment
from datetime import datetime
#定义表单类
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
#配置数据库
import os
from flask_sqlalchemy import SQLAlchemy
#数据库迁移框架
from flask_migrate import Migrate
#初始化Flask-Mail
from flask_mail import Mail
#电子邮件支持
from flask_mail import Message
#异步发送电子邮件
from threading import Thread

app = Flask(__name__)
bootstrap = Bootstrap(app)#模板对象
moment = Moment(app)#Flask-Moment对象
#SQLite数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICIATIONS'] = False
db = SQLAlchemy(app)
#初始化Flask-Migrate
migrate = Migrate(app, db)
#配置Flask-Mail使用Gmail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
#电子邮件支持
app.config['FLASK_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASK_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
#初始化Flask-Mail
mail = Mail(app)

#配置Flask-WTF
app.config['SECRET_KEY'] = 'hard to guess string'

#表单类
class NameFrom(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
    pass
#定义Role和User模型
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #定义关系
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role %r>' % self.name
    pass

class User(db.Model):
    __tablenmae__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    #定义关系
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username
    pass

#添加一个shell上下文
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)    

#异步发送电子邮件
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        
#发送电子邮件
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, 
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start
    return thr
    
#设置路由
@app.route('/', methods=['GET', 'POST'])
def index():    
    form = NameFrom()
    if form.validate_on_submit(): 
        #处理web表单 & 闪现消息
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        #在视图函数操作数据库
        user = User.query.filter_by(username=form.name.data)
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    
    return render_template('index.html', form=form, name=session.get('name'), 
                           known=session.get('known',  False), 
                           current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




if __name__=='__main__':
    app.run