from app import GLOBAL_ENDPOINTS
from app import endpoints

ENDPOINTS = (
    ('/', endpoints.index.IndexView.as_view('index')),
    ('/login', endpoints.login.LoginView.as_view('login')),
    ('/register', endpoints.register.RegisterView.as_view('register')),
    ('/logout', endpoints.login.logout)
)


def register_routes():
    for route in ENDPOINTS:
        GLOBAL_ENDPOINTS.append(route)
