import json
import sqlite3
from uuid import uuid4
from passlib.hash import sha256_crypt


def create_table(cur):
    table_aire = """CREATE TABLE IF NOT EXISTS aire (id INTEGER PRIMARY KEY, age_min INTEGER, age_max INTEGER, polygone_type TEXT, nom TEXT, surface REAL, nombre_de_jeux INTEGER)"""
    cur.execute(table_aire)
    table_aire_geo = """CREATE TABLE IF NOT EXISTS aire_geo (id INTEGER, lat REAL, lon REAL, FOREIGN KEY (id) REFERENCES aire (id))"""
    cur.execute(table_aire_geo)


class MoteurDB:
    def __init__(self):
        self.conn = sqlite3.connect('aires_de_jeux.sq3', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        create_table(cur)
        self.conn.commit()
        with open('clefs.json', 'r') as keys_file:
            self.keys = json.load(keys_file)

    def authorize(self, key):
        hash_key = sha256_crypt.encrypt(key)
        return hash_key in self.keys

    def get_authorization(self):
        clef_api = str(uuid4())
        hash_clef_api = sha256_crypt.encrypt(clef_api)
        self.keys.append(hash_clef_api)
        with open('clefs.json', 'w') as keys_file:
            json.dump(self.keys, keys_file)
        return clef_api


    def get_schema(self, key):
        if not self.authorize(key):
            return 'You are not authorized to access this at the moment, please enter your API key'

        cursor = self.conn.cursor()

        cursor.execute("PRAGMA table_info('aires_de_jeux')")
        columns = cursor.fetchall()

        column_names = [column[1] for column in columns]

        return column_names

    def get_aires(self, key: str, champs: str, condition: str):
        if not self.authorize(key):
            return 'You are not authorized to access this at the moment, please enter your API key'

        cursor = self.conn.cursor()

        if condition is None:
            cursor.execute(f"SELECT {champs} FROM aires_de_jeux")
        else:
            cursor.execute(f"SELECT {champs} FROM aires_de_jeux WHERE {condition}")

        aires = list(cursor.fetchall())

        return aires

    def close(self):
        self.conn.close()
