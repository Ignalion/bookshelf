"""
This module provides everything about login in the booksgelf app
"""
from flask import redirect, render_template, request, views, url_for
from flask_login import login_user, current_user, login_required, logout_user

from app import login_manager
from app.models import User
from app.forms import LoginForm


class LoginView(views.View):
    """ Log user in by provided credentials """

    methods = ('GET', 'POST')

    def dispatch_request(self, t='login.html'):
        form = LoginForm()

        if current_user.is_authenticated():
            return redirect(url_for('index'))

        if request.method == 'POST':
            if form.validate_on_submit():
                login_user(form.user_obj,
                           remember=form.remember.data)
                return redirect(url_for('index'))
        return render_template(t,
                               form=form,
                               user=current_user,
                               page_title='Login',
                               )


@login_manager.user_loader
def user_load(userid):
    user = None
    user = User.query.filter_by(id=userid).one()
    return user


@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
