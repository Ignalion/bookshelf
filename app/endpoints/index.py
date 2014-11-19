"""
This is index view. Start of the trip. Beginning of everything here.
"""
from flask import render_template, views
from flask_login import current_user


class IndexView(views.View):
    """
    Index view.
    That is shown to any user that come to the app first time
    """

    methods = ('GET',)

    def dispatch_request(self, t="index.html"):
        return render_template(t,
                               user=current_user)
