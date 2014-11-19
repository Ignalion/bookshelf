#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from app.lib.abstract import (
    UserAbstraction,
    BookAbstraction,
    AuthorAbstraction,
)


USERS = (
    {'username': 'test1', 'email': 'test1@example.com', 'password': '123'},
)

BOOKS = (
    'Test Book #1. About Python, I guess.',
    'Test Book #2. Also about Python (Why not?)',
    'This one about Javascript',
    'Another one Javascript. It\'s trending.',
    'How to code Python and have a perfect life',
    'The book. Just the book',
    'Another book. Just a book',
    'No idea. Did\'n even read it',
    'Work hard die young!',
    'Test Book #3. HTML, let\'s say',
    'I\'m out of ideas. Really',
    'No, really. No ideas. Let\'s back to numbers',
    'Enough!',
)

AUTHORS = (
    'Some Clever Man #1',
    'Some Clever Man #2',
    'Some Clever Man #3',
    'Another Clever Man #1',
    'Another Clever Man #2',
    'Another Clever Man #3',
    'Another Clever Man #4',
    'Another Clever Man #5',
    'Not Very Clever #1',
    'Not Very Clever #2',
    'Very Clever Man',
    'Anonymous',
)


def create_test_data():
    user_mgr = UserAbstraction()
    author_mgr = AuthorAbstraction()
    book_mgr = BookAbstraction()
    user = USERS[0]
    user['password'] = user_mgr.set_password(user['password'])
    user = user_mgr.create(**user)
    authors = []
    for author in AUTHORS:
        author_obj = author_mgr.create(user=user, name=author)
        authors.append(author_obj)

    for book in BOOKS:
        authors_for_book = random.sample(authors, random.randint(1, 3))
        book_obj = {
            'title': book,
            'authors': authors_for_book,
        }
        book_mgr.create(user=user, **book_obj)

if __name__ == '__main__':
    create_test_data()
