# -*- coding:utf8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from app.np4 import  *


class LoginForm(FlaskForm):
    # DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登入')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '再次输入密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已注册')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已注册')


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('该用户名已注册')


class PostForm(FlaskForm):
    # post = TextAreaField('说点什么', validators=[
    S = '想分享什么模式呢？'
    '''post = TextAreaField('说点什么吧：', validators=[
        DataRequired(), Length(min=1, max=140)])'''
    '''pattern = TextAreaField(S, validators=[
        DataRequired(), Length(min=1, max=140)])'''
    # c = [(1, '1'), (2, '2'), (3, '3')]
    c = [('电视机开12:30，电视机关15:30', '电视机开12:30，电视机关15:30'),
         ('灯开12:30，灯关15:30', '灯开12:30，灯关15:30'),
         ('洗衣机开12:30，洗衣机关15:30', '洗衣机开12:30，洗衣机关15:30111111111111111111111111111111111111111111'
             '111111111111111111111111111111111111111111111111111111111111111111111'
             '111111111111111111111111111111111111111111111111111111111111111111')]
    S = read("s&t3.0.txt")
    # S2 = read("sequence.txt")
    S2 = open("record.txt", 'w+')
    # print(S)
    num_p = 0
    patterns = NprefixSpan(SquencePattern([], sys.maxsize), S, 3)
    new_patterns = filter_patterns(patterns)
    # print_patterns(patterns)
    npprefix = print_patterns(S, S2, new_patterns)
    a = npprefix.prefix3

    post = SelectField(label='请选择想要发布的模式',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'class': 'form-control'
        },
        choices=a,
        # default = 3,
        coerce=str
                          )
    submit = SubmitField('提交')


class PatternForm(FlaskForm):
    pattern1 = '洗衣机11:30'
    pattern2 = '电视12:50'
    submit = SubmitField('提交')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('请求重置密码')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '重复输入密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('重置密码')




