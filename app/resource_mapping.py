"""
This module inserts all the routes to the GLOBAL_ENDPOINTS list that will
be registered in __init__.py by add_url_rule function
"""

from app import GLOBAL_ENDPOINTS
from app import endpoints

ENDPOINTS = (
    ('/', endpoints.index.IndexView.as_view('index')),
    ('/about', endpoints.about.AboutView.as_view('about')),
    ('/contacts', endpoints.contacts.ContactsView.as_view('contacts')),
    ('/login', endpoints.login.LoginView.as_view('login')),
    ('/register', endpoints.register.RegisterView.as_view('register')),
    ('/logout', endpoints.login.logout),

    ('/booklist', endpoints.booksauthors.BookList.as_view('booklist')),
    ('/authorlist', endpoints.booksauthors.AuthorList.as_view('authorlist')),
    ('/addbook/', endpoints.booksauthors.AddEditBook.as_view('addbook')),
    ('/editbook/<int:book_id>',
        endpoints.booksauthors.AddEditBook.as_view('editbook')),
    ('/addauthor', endpoints.booksauthors.AddEditAuthor.as_view('addauthor')),
    ('/editauthor/<int:author_id>',
        endpoints.booksauthors.AddEditAuthor.as_view('editauthor')),
    ('/search/', endpoints.search.SearchView.as_view('search')),

)


def register_routes():
    for route in ENDPOINTS:
        GLOBAL_ENDPOINTS.append(route)
