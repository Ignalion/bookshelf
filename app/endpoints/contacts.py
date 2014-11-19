"""
This is contacts view. Shows contact information
"""
from flask import render_template, views
from flask_login import current_user


class ContactsView(views.View):
    """
    Contact view.
    If by any chance you want to contact me - you have all information you need
    just here.
    """

    def dispatch_request(self, t="contacts.html"):
        page_title = 'Contacts'
        return render_template(t,
                               page_title=page_title,
                               user=current_user)
