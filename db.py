import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_user(self, full_name, user_name, chat_id, lang):
        self.cur.execute("""insert into users(full_name, user_name, chat_id, lang) values (?,?,?,?)""",
                         (full_name, user_name, chat_id, lang))
        self.conn.commit()

    def get_user_by_chat_id(self, chat_id):
        self.cur.execute("""select * from users where chat_id = ?""", (chat_id,))
        user = dict_fetchone(self.cur)
        return user

    def get_users(self):
        self.cur.execute("""select * from users""")
        users = dict_fetchall(self.cur)
        return users

    def get_channels(self):
        self.cur.execute("""select * from channels""")
        channels = dict_fetchall(self.cur)
        return channels

    def create_channel(self, name, link):
        self.cur.execute("""insert into channels(name,link) values (?,?)""", (name, link))
        self.conn.commit()

    def delete_channel(self, name, link):
        self.cur.execute("""delete from channels where name= ? and link= ? """, (name, link))
        self.conn.commit()


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
