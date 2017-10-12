import sqlalchemy
from sqlalchemy.orm import Query
from user_db.models import db_session, User, Subscription
# from models import db_session, User, Subscription


def user_db_add_user(chat_id, first_name=None, last_name=None, username=None):
    user = db_session.query(User).filter(User.user_id == chat_id).first()
    if user: # если chat_id уже есть в БД - обновляет инфу
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
    else:
        new_user = User(chat_id, first_name, last_name, username) # если chat_id нет в БД - добавляет
        db_session.add(new_user)    
    try:
        db_session.commit() # обновляет данные в БД
        return 'add_user: User created' if not user else 'add_user: User is exist, data have updated'
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        return 'add_user: Error'


def subscriptions_db_add_sub(chat_id, title=None, is_active=None):
    subscription = db_session.query(Subscription).filter(
        Subscription.user_id == chat_id,
        Subscription.title == title,
    ).first()
    if subscription: # если chat_id и подписка уже есть в БД - обновляет инфу
        subscription.is_active = is_active
    else:
        new_subscription = Subscription(chat_id, title, is_active) # если подписки нет в БД - добавляет
        db_session.add(new_subscription)    
    try:
        db_session.commit() # обновляет данные в БД
        return 'add_subscription: Subscription created' if not subscription else 'add_subscription: Subscription is exist, data have updated'
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        return 'add_subscription: Error'

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
                            s.is_active == True
                                         ).all()
    for sub in select:
        result.append(sub.user_id)
    return result

if __name__ == '__main__':
    pass
    # db_session.rollback() значит откатить изменения
    # но это можно сделать только до db_session.commit()

    # a = subscriptions_db_add_sub('192204203', 'Лента', True)
    # print(a)


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
    print(subscription_check('192204203', 'РБК'))

