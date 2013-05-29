# -*- coding: utf-8 -*-

'''
Dahu: Picture gallery
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    Web forms
'''

from flask.ext.wtf import Form, TextField, PasswordField, Required

class LoginForm(Form):
    username = TextField('Username', validators=[Required(message='Username is required.')])
    password = PasswordField('Password', validators=[Required(message='Password is required.')])
