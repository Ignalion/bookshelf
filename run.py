#!/usr/bin/env python

from app.main import app

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1")
    #app.run(debug=True, host="ignalion.me")
