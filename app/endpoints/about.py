"""
This is about view. Just all about me and this project
"""
from flask import render_template, views
from flask_login import current_user


class AboutView(views.View):
    """
    About view.
    Just information about me and project
    """

    def dispatch_request(self, t="about.html"):
        return render_template(t,
                               user=current_user)
