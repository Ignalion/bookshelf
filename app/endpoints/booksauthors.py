from flask import (
    render_template,
    request,
    redirect,
    url_for,
    views,
)

from flask_login import login_required, current_user

from app.lib.abstract import BookAbstraction, AuthorAbstraction
from app.forms import AddBookForm, AddAuthorForm, BookListForm, AuthorListForm


# class BookList(views.View):
#
#     @login_required
#     def dispatch_request(self, t="old_booklist.html"):
#         book_mgr = BookAbstraction()
#         books = book_mgr.get_book_list(current_user)
#
#         return render_template(t,
#                                books=books,
#                                user=current_user)
#

class BookList(views.View):

    methods = ('GET', 'POST')

    @login_required
    def dispatch_request(self, t="booklist.html"):
        book_mgr = BookAbstraction()
        books = book_mgr.get_book_list(current_user)

        form = BookListForm()
        if request.method == 'GET':
            for book_obj in books:
                form.books.append_entry(book_obj)
                # Dirty hack!
                form.books[-1].book_id.data = book_obj.id

        if request.method == 'POST':
            target = filter(
                lambda book: any((book.data['edit'], book.data['delete'])),
                form.books)[0]
            if target.edit.data:
                return redirect(url_for('editbook',
                                book_id=target.data['book_id']))
            elif target.delete.data:
                book_mgr.delete(id=int(target.data['book_id']))
                return redirect(url_for('booklist'))

        return render_template(t,
                               form=form,
                               user=current_user)


class AuthorList(views.View):

    methods = ('GET', 'POST')

    @login_required
    def dispatch_request(self, author_id=None, t="authorlist.html"):
        author_mgr = AuthorAbstraction()
        authors = author_mgr.get_author_list(current_user)

        form = AuthorListForm()
        if request.method == 'GET':
            for author_obj in authors:
                form.authors.append_entry(author_obj)
                # And another one!
                form.authors[-1].author_id.data = author_obj.id

        if request.method == 'POST':
            target = filter(
                lambda author: any((author.data['edit'],
                                    author.data['delete'])),
                form.authors)[0]
            if target.edit.data:
                return redirect(url_for('editauthor',
                                author_id=target.data['author_id']))
            elif target.delete.data:
                author_mgr.delete(id=int(target.data['author_id']))
                return redirect(url_for('authorlist'))

        return render_template(t,
                               form=form,
                               user=current_user)

        return render_template(t,
                               authors=authors,
                               user=current_user)


class AddBook(views.View):

    methods = ('GET', 'POST')

    @login_required
    def dispatch_request(self, book_id=None, t="addbook.html"):
        book_mgr = BookAbstraction()
        form = AddBookForm(request.form, current_user)
        form.authors.choices = [(a.id, a.name) for a in current_user.authors]

        if book_id is not None and request.method == 'GET':
            book = current_user.books.filter(
                book_mgr.model.id == book_id).one()
            form.authors.default = [a.id for a in book.authors]
            form.process()
            form.new_book.data = book.title
            form.submit.label.text = 'Edit book'

        if request.method == 'POST':
            book = {
                'title': form.new_book.data,
                'authors': form.authors.data,
                'id': book_id
            }
            book_mgr.add_edit_book(current_user, book)

            return redirect(url_for('booklist'))

        return render_template(t,
                               form=form,
                               user=current_user)


class AddAuthor(views.View):
    methods = ('GET', 'POST')

    @login_required
    def dispatch_request(self, author_id=None, t="addauthor.html"):
        author_mgr = AuthorAbstraction()
        form = AddAuthorForm(request.form, current_user)
        form.books.choices = [(b.id, b.title) for b in current_user.books]

        if author_id is not None and request.method == 'GET':
            author = current_user.authors.filter(
                author_mgr.model.id == author_id).one()
            form.books.default = [b.id for b in author.books]
            form.process()
            form.new_author.data = author.name
            form.submit.label.text = 'Edit author'

        if request.method == 'POST':
            author = {
                'name': form.new_author.data,
                'books': form.books.data,
                'id': author_id,
            }
            author_mgr.add_edit_author(current_user, author)

            return redirect(url_for('authorlist'))

        return render_template(t,
                               form=form,
                               user=current_user)