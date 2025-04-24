import ast
from sqlalchemy import Column, BigInteger, String
from ChannelBot.database import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(BigInteger, primary_key=True)
    channels = Column(String, nullable=True)

    def __init__(self, user_id, channels=None):
        self.user_id = user_id
        self.channels = channels


# Create table with bind
Users.__table__.create(bind=SESSION.get_bind(), checkfirst=True)


def num_users():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()


def add_channel(user_id, channel_id):
    q = SESSION.query(Users).get(user_id)
    if q:
        if q.channels:
            channels = list(set(ast.literal_eval(q.channels)))
            if channel_id not in channels:
                channels.append(channel_id)
            q.channels = str(channels)
        else:
            q.channels = str([channel_id])
    else:
        SESSION.add(Users(user_id, str([channel_id])))
    SESSION.commit()


def remove_channel(user_id, channel_id):
    q = SESSION.query(Users).get(user_id)
    if q and q.channels:
        channels = list(set(ast.literal_eval(q.channels)))
        if channel_id in channels:
            channels.remove(channel_id)
            q.channels = str(channels) if channels else None
    SESSION.commit()


def get_channels(user_id):
    q = SESSION.query(Users).get(user_id)
    if q:
        if q.channels:
            channels = ast.literal_eval(q.channels)
            SESSION.close()
            return True, channels
        else:
            return False, []
    else:
        SESSION.add(Users(user_id))
        SESSION.commit()
        return False, []
