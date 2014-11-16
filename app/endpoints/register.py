from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    views
)

from flask_login import current_user

from app.forms import RegisterForm
from app.lib.abstract import UserAbstraction
# from app.models import User


class RegisterView(views.View):
    """ Register user with data, provided by himself on the register page """

    methods = ('GET', 'POST',)

    def dispatch_request(self):
        if current_user.is_authenticated():
            return redirect(url_for('index'))

        user_data = session.get('form_data', {})

        form = RegisterForm(request.form, **user_data)

        if request.method == 'POST':
            if form.validate_on_submit():
                user_mgr = UserAbstraction()
                user_mgr.create(**form.data)
                return redirect(url_for('index'))

        form_errors = form.errors

        return render_template('register.html',
                               form=form,
                               user=current_user,
                               form_errors=form_errors)
