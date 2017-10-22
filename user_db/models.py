from sqlalchemy import create_engine
from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///user_db/newsbot.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50))

    def __init__(self, user_id=None, first_name=None, last_name=None, username=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    def __repr__(self):
        return '<User {} {} {} {}>'.format(self.user_id, self.first_name, self.last_name,
                                           self.username)


class Subscription(Base):
    __tablename__ = 'subscriptions'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, )
    title = Column(String(140), primary_key=True)
    is_active = Column(Boolean)

    def __init__(self, user_id=None, title=None, is_active=None):
        self.user_id = user_id
        self.title = title
        self.is_active = is_active

    def __repr__(self):
        return '<Subscription {} {} {}>'.format(self.user_id, self.title, self.is_active)


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(140), ForeignKey('subscriptions.title'))
    date = Column(String(10))
    time = Column(String(5))
    news_title = Column(String(300))
    news_link = Column(String(150))
    news_short_link = Column(String(100))
    is_sent = Column(Boolean)

    def __init__(self, title=None, date=None, time=None, news_title=None,
                 news_link=None, news_short_link=None, is_sent=None):
        self.title = title
        self.date = date
        self.time = time
        self.news_title = news_title
        self.news_link = news_link
        self.news_short_link = news_short_link
        self.is_sent = is_sent

    def __repr__(self):
        return '<News {} {} {} {} {}>'.format(self.title, self.date, self.time, self.news_title,
                                              self.news_link, self.news_short_link, self.is_sent)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    # new_sub = Subscription('192204203', 'РБК', True)
    # db_session.add(new_sub)
    # new_sub = Subscription('192204203', 'Cnews', True)
    # db_session.add(new_sub)
    # new_sub = Subscription('192204203', 'Тест2', True)
    # db_session.add(new_sub)
    # db_session.commit()
