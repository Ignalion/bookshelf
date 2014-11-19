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
        page_title = "Home"
        return render_template(t,
                               page_title=page_title,
                               user=current_user)
