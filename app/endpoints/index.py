from flask import render_template
from flask.views import View
from flask_login import current_user


class IndexView(View):

    methods = ('GET',)

    def dispatch_request(self, t="index.html"):
        user = current_user
        return render_template(t,
                               user=user)
