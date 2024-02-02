# create a user modal

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, password, profile_pic):
        self.id = id
        self.username = username
        self.password = password
        self.profile_pic = profile_pic