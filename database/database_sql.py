import sqlite3
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    user_name: str
    reg_time: str
    is_admin: bool

    @staticmethod
    def get_user_data(self) -> str:
        return f'User data:\n userID: {self.user_id}, username: {self.user_name},\n' \
               f'registered on: {self.reg_time}, is_admin: {self.is_admin}'


@dataclass
class Term:
    term_id: int
    term_ru: str
    term_en: str
    term_comments: str
    added_by: str
    added_on: str

    @staticmethod
    def get_term_data(self) -> str:
        return f'TermID: {self.term_id}, added_by: {self.added_by}\n' \
               f'{self.term_ru} == {self.term_en}\n' \
               f'comments: {self.term_comments}'


class BotDb:

    def __init__(self):
        self._db = sqlite3.connect('bot_users.db')

    def __enter__(self):
        self._create_tables_if_none()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()

    def _create_tables_if_none(self) -> None:  # also need table for log
        cursor = self._db.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS tbl_users(user_id INTEGER PRIMARY KEY, user_name TEXT,
                       reg_time TEXT, is_admin BOOLEAN)
                       ''')
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS tbl_terms(term_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       term_ru TEXT, term_en TEXT, term_comments TEXT, added_by TEXT, added_on TEXT)
                       ''')
        self._db.commit()
        cursor.close()

    def add_user(self, user_id: int, user_name: str, reg_time: str, is_admin: bool = False) -> None:
        cursor = self._db.cursor()
        cursor.execute('''
                       INSERT OR REPLACE INTO tbl_users(user_id, user_name, reg_time, is_admin)
                       VALUES(?,?,?,?)''',
                       (user_id, user_name, reg_time, is_admin))
        self._db.commit()
        cursor.close()

    def get_users(self) -> list:
        cursor = self._db.cursor()
        cursor.execute('''
                       SELECT * FROM tbl_users
                       ''')
        all_rows = cursor.fetchall()
        users_list = []
        for row in all_rows:
            users_list.append(User(user_id=row[0], user_name=row[1], reg_time=row[2], is_admin=row[3]))
        cursor.close()
        return users_list

    def add_term(self, term_ru: str, term_en: str, comments: str, added_by: int, added_on: str) -> None:
        cursor = self._db.cursor()
        cursor.execute('''
                       INSERT OR REPLACE INTO tbl_terms(term_ru, term_en, term_comments, added_by, added_on)
                       VALUES(?,?,?,?,?)
                       ''', (term_ru, term_en, comments, added_by, added_on))
        self._db.commit()
        cursor.close()

    def get_term(self, term) -> Term:
        cursor = self._db.cursor()
        cursor.execute('''
                       SELECT * FROM tbl_terms
                       ''')
        all_rows = cursor.fetchall()
        for row in all_rows:
            if term in row[1]:
                return Term(term_id=row[0], term_ru=row[1], term_en=row[2], term_comments=row[3],
                            added_by=row[4], added_on=row[5])
            else:
                pass
