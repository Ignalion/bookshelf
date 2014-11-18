"""
This is index view. Start of the trip. Beginning of everything here.
"""
from flask import render_template
from flask.views import View
from flask_login import current_user


class IndexView(View):
    """
    Index view.
    That is shown to any user that come to the app first time
    """

    methods = ('GET',)

    def dispatch_request(self, t="index.html"):
        user = current_user
        return render_template(t,
                               user=user)
