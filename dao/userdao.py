from models.user import User


class UserDao(object):

    @staticmethod
    def does_user_exist(user_id):
        return User.query.get(user_id)

    @staticmethod
    def add_user(user_id, name, api_key, access_token):
        new_user = User(user_id, name, api_key, access_token)
        User.session.add(new_user)
        User.session.commit()
        return new_user

    @staticmethod
    def valid_api_key(key):
        return User.query.filter_by(api_key=key).count()
