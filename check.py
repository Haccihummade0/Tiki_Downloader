from db import Database

db = Database("Tiki_database.db")


def check_user(user):
    db_user = db.get_user_by_chat_id(user.id)

    if db_user:
        return db_user
    else:
        db.create_user(
            full_name=user.full_name,
            user_name=user.username,
            chat_id=user.id,
            lang="uz"
        )
        return False


def get_channels(user):
    channels = db.get_channels()
    return channels
