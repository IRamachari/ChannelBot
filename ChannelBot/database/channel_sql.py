from sqlalchemy import Column, String, Boolean, BigInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Create a database engine
DATABASE_URL = "sqlite:///channelbot.db"
engine = create_engine(DATABASE_URL)

# Create a base class for declarative models
BASE = declarative_base()

# Create a session factory
session_factory = sessionmaker(bind=engine)
SESSION = scoped_session(session_factory)


class Channel(BASE):
    __tablename__ = "channels"
    __table_args__ = {'extend_existing': True}
    channel_id = Column(BigInteger, primary_key=True)
    admin_id = Column(BigInteger)
    caption = Column(String, nullable=True)
    buttons = Column(String, nullable=True)
    position = Column(String, nullable=True)
    sticker_id = Column(String, nullable=True)
    edit_mode = Column(String, nullable=True)
    webpage_preview = Column(Boolean)

    def __init__(self, channel_id, admin_id, caption=None, buttons=None, edit_mode=None, position=None, webpage_preview=False, sticker_id=None):
        self.channel_id = channel_id
        self.admin_id = admin_id
        self.caption = caption
        self.buttons = buttons
        self.position = position
        self.webpage_preview = webpage_preview
        self.sticker_id = sticker_id
        self.edit_mode = edit_mode


# Create all tables in the engine
BASE.metadata.create_all(engine)


async def num_channels():
    try:
        return SESSION.query(Channel).count()
    finally:
        SESSION.close()


async def add_channel(channel_id, user_id):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if not q:
            SESSION.add(Channel(channel_id, user_id))
            SESSION.commit()
        return True
    except Exception as e:
        SESSION.rollback()
        raise e
    finally:
        SESSION.close()


async def remove_channel(channel_id):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q:
            SESSION.delete(q)
            SESSION.commit()
            return True
        return False
    except Exception as e:
        SESSION.rollback()
        raise e
    finally:
        SESSION.close()


async def get_channel_info(channel_id):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q:
            info = {
                'admin_id': q.admin_id,
                'buttons': q.buttons,
                'caption': q.caption,
                'position': q.position,
                'sticker_id': q.sticker_id,
                'webpage_preview': q.webpage_preview,
                'edit_mode': q.edit_mode
            }
            return True, info
        else:
            return False, {}
    finally:
        SESSION.close()


async def set_caption(channel_id, caption):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q:
            q.caption = caption
            SESSION.commit()
            return True
        else:
            return False
    except Exception as e:
        SESSION.rollback()
        raise e
    finally:
        SESSION.close()


async def get_caption(channel_id):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q and q.caption:
            return q.caption
        else:
            return ''
    finally:
        SESSION.close()


async def set_buttons(channel_id, buttons):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q:
            q.buttons = buttons
            SESSION.commit()
            return True
        else:
            return False
    except Exception as e:
        SESSION.rollback()
        raise e
    finally:
        SESSION.close()


async def get_buttons(channel_id):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q and q.buttons:
            return q.buttons
        else:
            return None
    finally:
        SESSION.close()


async def set_position(channel_id, position):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q:
            q.position = position
            SESSION.commit()
            return True
        else:
            return False
    except Exception as e:
        SESSION.rollback()
        raise e
    finally:
        SESSION.close()


async def get_position(channel_id):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q and q.position:
            return q.position
        else:
            return 'below'
    finally:
        SESSION.close()


async def set_sticker(channel_id, sticker):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q:
            q.sticker_id = sticker
            SESSION.commit()
            return True
        else:
            return False
    except Exception as e:
        SESSION.rollback()
        raise e
    finally:
        SESSION.close()


async def get_sticker(channel_id):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q and q.sticker_id:
            return q.sticker_id
        else:
            return None
    finally:
        SESSION.close()


async def toggle_webpage_preview(channel_id, value):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q:
            q.webpage_preview = bool(value)
            SESSION.commit()
            return True
        else:
            return False
    except Exception as e:
        SESSION.rollback()
        raise e
    finally:
        SESSION.close()


async def get_webpage_preview(channel_id):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q and q.webpage_preview:
            return True
        else:
            return False
    finally:
        SESSION.close()


async def set_edit_mode(channel_id, edit_mode):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q:
            q.edit_mode = edit_mode
            SESSION.commit()
            return True
        else:
            return False
    except Exception as e:
        SESSION.rollback()
        raise e
    finally:
        SESSION.close()


async def get_edit_mode(channel_id):
    try:
        q = SESSION.query(Channel).get(channel_id)
        if q and q.edit_mode:
            return q.edit_mode
        else:
            return 'media'
    finally:
        SESSION.close()
