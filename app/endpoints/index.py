from flask import render_template
from flask.views import View
from app import models

class IndexView(View):
    def dispatch_request(self, t="index.html"):
        return render_template(t)
