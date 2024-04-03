import mysql.connector

from flask import current_app, g


def getdb():
    if 'db' not in g or not g.db.is_connected():
        g.db = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            user=current_app.config['DB_USERNAME'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_DATABASE']
        )
        print('connected')
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        # close the database 
        db.close()