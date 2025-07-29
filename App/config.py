import os

POSTGRES = {
    'user': 'your_user',
    'pw': 'your_password',
    'db': 'finch_db',
    'host': 'localhost',
    'port': '5432',
}

SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES['user']}:{POSTGRES['pw']}@{POSTGRES['host']}:{POSTGRES['port']}/{POSTGRES['db']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
