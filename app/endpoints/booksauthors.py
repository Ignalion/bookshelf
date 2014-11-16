from flask import (
    render_template,
    request,
    redirect,
    url_for,
    views,
)

from flask_login import login_required, current_user

from app.lib.abstract import BookAbstraction, AuthorAbstraction
from app.forms import AddBookForm, AddAuthorForm


class BookList(views.View):

    @login_required
    def dispatch_request(self, t="booklist.html"):
        book_mgr = BookAbstraction()
        books = book_mgr.get_book_list(current_user)

        return render_template(t,
                               books=books,
                               user=current_user)


class AuthorList(views.View):

    @login_required
    def dispatch_request(self, t="authorlist.html"):
        author_mgr = AuthorAbstraction()
        authors = author_mgr.get_authors_list(current_user)

        return render_template(t,
                               authors=authors,
                               user=current_user)


class AddBook(views.View):

    methods = ('GET', 'POST')

    @login_required
    def dispatch_request(self, t="addbook.html"):
        form = AddBookForm()
        book_mgr = BookAbstraction()

        if request.method == 'POST':
            book_mgr.add_book(current_user, form.new_book.data)

            return redirect(url_for('index'))  # FIXME

        return render_template(t,
                               form=form,
                               user=current_user)


class AddAuthor(views.View):
    methods = ('GET', 'POST')

    @login_required
    def dispatch_request(self, t="addauthor.html"):
        form = AddAuthorForm()
        author_mgr = AuthorAbstraction()

        if request.method == 'POST':
            author_mgr.add_author(current_user, form.new_author.data)

            return redirect(url_for('index'))  # FIXME

        return render_template(t,
                               form=form,
                               user=current_user)
