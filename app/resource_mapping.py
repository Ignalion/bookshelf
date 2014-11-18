from app import GLOBAL_ENDPOINTS
from app import endpoints

ENDPOINTS = (
    ('/', endpoints.index.IndexView.as_view('index')),
    ('/login', endpoints.login.LoginView.as_view('login')),
    ('/register', endpoints.register.RegisterView.as_view('register')),
    ('/logout', endpoints.login.logout),

    ('/booklist', endpoints.booksauthors.BookList.as_view('booklist')),
    ('/authorlist', endpoints.booksauthors.AuthorList.as_view('authorlist')),
    ('/addbook/', endpoints.booksauthors.AddBook.as_view('addbook')),
    ('/editbook/<int:book_id>',
        endpoints.booksauthors.AddBook.as_view('editbook')),
    ('/addauthor', endpoints.booksauthors.AddAuthor.as_view('addauthor')),
    ('/editauthor/<int:author_id>',
        endpoints.booksauthors.AddAuthor.as_view('editauthor')),
    ('/search/', endpoints.search.SearchView.as_view('search')),

)


def register_routes():
    for route in ENDPOINTS:
        GLOBAL_ENDPOINTS.append(route)
