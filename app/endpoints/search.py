from flask import (
    render_template,
    request,
    redirect,
    url_for,
    views,
)
from flask_login import current_user

from app.lib.abstract import BookAbstraction, AuthorAbstraction
from app.forms import SearchForm


class SearchView(views.View):

    methods = ('GET', 'POST')

    def dispatch_request(self, t="search.html"):
        book_mgr = BookAbstraction()
        author_mgr = AuthorAbstraction()
        result = []

        form = SearchForm()

        if request.method == 'POST':
            if len(form.search.data) < 2:
                return redirect(url_for('search'))

            result = book_mgr.book_search(form.search.data)
            result.extend(author_mgr.author_search(form.search.data))

        return render_template(t,
                               form=form,
                               result=set(result),
                               user=current_user)
