import sqlalchemy
from sqlalchemy.orm import Query
# from models import db_session, User, Subscription, News
from user_db.models import db_session, User, Subscription, News


def users_db_add_user(chat_id, first_name=None, last_name=None, username=None):
    user = db_session.query(User).filter(User.user_id == chat_id).first()
    if user:  # если chat_id уже есть в БД - обновляет инфу
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
    else:
        new_user = User(chat_id, first_name, last_name, username)  # если chat_id нет в БД - добавляет
        db_session.add(new_user)
    try:
        db_session.commit()  # обновляет данные в БД
        return 'add_user: User created' if not user else 'add_user: User is exist, data have updated'
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        return 'add_user: Error'


def subscriptions_db_add_sub(chat_id, title=None, is_active=None):
    subscription = db_session.query(Subscription).filter(
        Subscription.user_id == chat_id,
        Subscription.title == title,
    ).first()
    if subscription:  # если chat_id и подписка уже есть в БД - обновляет инфу
        subscription.is_active = is_active
    else:
        new_subscription = Subscription(chat_id, title, is_active)  # если подписки нет в БД - добавляет
        db_session.add(new_subscription)
    try:
        db_session.commit()  # обновляет данные в БД
        return 'add_subscription: Subscription created' if not subscription else 'add_subscription: Subscription is exist, data have updated'
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        return 'add_subscription: Error'


def news_db_add_news(title, date, time, news_title, news_link, news_short_link, is_sent=False):
    news = db_session.query(News).filter(
        News.news_link == news_link
    ).first()
    if not news:
        new_news = News(title, date, time, news_title, news_link, news_short_link, is_sent)  # если новости нет в БД - добавляет
        db_session.add(new_news)
        try:
            db_session.commit()  # обновляет данные в БД
            return 'add_news: News added'
        except sqlalchemy.exc.IntegrityError:
            db_session.rollback()
            return 'add_news: Error'
    else:
        return 'add_news: News is exist'


def subscription_check(chat_id, title):
    s = Subscription
    subscription_status = s.query.filter(s.user_id == chat_id,
                                         s.title == title
                                         ).first()
    if subscription_status is None:
        result = False
    else:
        result = subscription_status.is_active
    return result


def subscribers_list(title):
    result = list()
    s = Subscription
    select = s.query.filter(s.title == title,
                            s.is_active == 1
                            ).all()
    for sub in select:
        result.append(sub.user_id)
    return result


def unsent_news_list(title):
    result = list()
    n = News
    result = n.query.filter(n.is_sent == 0).order_by(n.time).all()
    return result


def mark_sent_news(news_list):
    for news in news_list:
        news.is_sent = True
    try:
        db_session.commit()  # обновляет данные в БД
        return 'mark_sent_news: News marked'
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        return 'mark_sent_news: Error'


def last_news(counter, title):
    n = News
    result = n.query.filter(n.title == title).order_by(n.time)[-counter:]
    return result


if __name__ == '__main__':
    pass
    # db_session.rollback() значит откатить изменения
    # но это можно сделать только до db_session.commit()

    # a = subscriptions_db_add_sub('192204203', 'Лента', True)
    # print(a)
    # b = news_db_add_news('РБК', '2017-10-21', '19:39', 'В Москве при пожаре в коллекторе около МГИМО погибли два человека', 'http://www.rbc.ru/rbcfreenews/59eb8e079a7947c6feb50008', 'https://goo.gl/A2gVFC')
    # print(b)

    # s = Subscription
    # u = User
    # print(s)
    # subscriptions = s.query.all()
    # print(subscriptions)
    # for subscription in subscriptions:
    #     username = u.query.filter(User.user_id == subscription.user_id).first()
    #     print(username.last_name)
    
    # print(s)
    # subscriptions = s.query.all()
    # print(subscriptions)
    # for subscription in subscriptions:
    #     username = u.query.filter(User.user_id == subscription.user_id).first()
    #     print(username.last_name)
    # print(subscription_check('192204203', 'РБК'))
