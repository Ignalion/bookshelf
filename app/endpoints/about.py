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
        page_title = 'About'
        return render_template(t,
                               page_title=page_title,
                               user=current_user)
