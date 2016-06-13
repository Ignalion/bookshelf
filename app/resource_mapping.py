"""
This module provides sets of rules for mapping urls routes to view functions
"""

from endpoints import index, about, contacts, login, register, booksauthors, \
    search

RULES = (
    ('/', index.IndexView.as_view('index')),
    ('/about', about.AboutView.as_view('about')),
    ('/contacts', contacts.ContactsView.as_view('contacts')),
    ('/login', login.LoginView.as_view('login')),
    ('/register', register.RegisterView.as_view('register')),
    ('/logout', login.logout),

    ('/booklist', booksauthors.BookList.as_view('booklist')),
    ('/authorlist', booksauthors.AuthorList.as_view('authorlist')),
    ('/addbook/', booksauthors.AddEditBook.as_view('addbook')),
    ('/editbook/<int:book_id>',
        booksauthors.AddEditBook.as_view('editbook')),
    ('/addauthor', booksauthors.AddEditAuthor.as_view('addauthor')),
    ('/editauthor/<int:author_id>',
        booksauthors.AddEditAuthor.as_view('editauthor')),
    ('/search/', search.SearchView.as_view('search')),

)

