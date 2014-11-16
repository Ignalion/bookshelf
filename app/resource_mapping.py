from app import GLOBAL_ENDPOINTS
from app import endpoints

ENDPOINTS = (
    ('/', endpoints.index.IndexView.as_view('home')),
)

def register_routes():
    for route in ENDPOINTS:
        GLOBAL_ENDPOINTS.append(route)
