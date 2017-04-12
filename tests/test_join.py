from jsonjoin.core import join_

TICKETS = [
    {"ticket": 1, "status": "Open"},
    {"ticket": 2, "status": "Closed"},
    {"ticket": 3, "status": "Pending"},
    {"ticket": 4, "status": "Open"}
]

CARDS = [
    {"ticket": 10, "priority": "High"},
    {"ticket": 2, "priority": None},
    {"ticket": 3, "priority": "Low"}
]


CARDS_DIFFERENT_KEY = [
    {"card": 10, "priority": "High"},
    {"card": 2, "priority": None},
    {"card": 3, "priority": "Low"}
]

INNER_JOIN_DIFFERENT_KEY = [
    {"card": 2, "ticket": 2, "priority": None, "status": "Closed"},
    {"card": 3, "ticket": 3, "priority": "Low", "status": "Pending"}
]

INNER_JOIN = [
    {"ticket": 2, "priority": None, "status": "Closed"},
    {"ticket": 3, "priority": "Low", "status": "Pending"}
]

LEFT_JOIN = [
    {"ticket": 1, "status": "Open"},
    {"ticket": 2, "priority": None, "status": "Closed"},
    {"ticket": 3, "priority": "Low", "status": "Pending"},
    {"ticket": 4, "status": "Open"}
]

RIGHT_JOIN = [
    {"ticket": 3, "priority": "Low", "status": "Pending"},
    {"ticket": 10, "priority": "High"},
    {"ticket": 2, "priority": None, "status": "Closed"}
]

OUTER_JOIN = [
    {"ticket": 1, "status": "Open"},
    {"ticket": 2, "priority": None, "status": "Closed"},
    {"ticket": 3, "priority": "Low", "status": "Pending"},
    {"ticket": 4, "status": "Open"},
    {"ticket": 10, "priority": "High"}
]

SYMMETRIC_JOIN = [
    {"ticket": 1, "status": "Open"},
    {"ticket": 4, "status": "Open"},
    {"ticket": 10, "priority": "High"}
]

DATA = (TICKETS, CARDS)


def test_inner_join():
    assert join_(DATA, keys='ticket') == INNER_JOIN
    assert join_(DATA, keys=('ticket', 'ticket')) == INNER_JOIN
    assert join_(DATA, keys='ticket', jointype='inner') == INNER_JOIN


def test_inner_join_different_key():
    assert join_(DATA, keys=('ticket', 'ticket')) == INNER_JOIN

    data = (CARDS_DIFFERENT_KEY, TICKETS)
    assert join_(data, keys=('card', 'ticket')) == INNER_JOIN_DIFFERENT_KEY


def test_left_join():
    assert join_(DATA, keys='ticket', jointype='left') == LEFT_JOIN


def test_right_join():
    assert join_(DATA, keys='ticket', jointype='right') == RIGHT_JOIN


def test_outer_join():
    assert join_(DATA, keys='ticket', jointype='outer') == OUTER_JOIN


def test_symmetric_join():
    assert join_(DATA, keys='ticket', jointype='symmetric') == SYMMETRIC_JOIN
