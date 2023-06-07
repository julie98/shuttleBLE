import base64
import os
import time
from flask import g
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import Utils
import ast
from datetime import datetime


class User(UserMixin):
    def __init__(self, first_name=None, last_name=None, email=None,
                 password=None, is_active=False, _id=None, created_on=None,
                 token=None, token_expiration=None, username=None):
        self.values = {'first_name': first_name, 'last_name': last_name,
                       'email': email, 'password': password,
                       'is_active': is_active, 'type': 'user',
                       'created_on': created_on,
                       'token_expiration': token_expiration,
                       'token': token, 'username': username}
        if _id is not None:
            self.values['_id'] = _id

    def __str__(self):
        return str(self.values)

    def verify_password(self, password):
        return check_password_hash(self.values['password'], password)

    def get_id(self):
        return self.values['_id']

    def create_user(self):
        if not User.user_exists(email=self.values['email']):
            self.values['created_on'] = time.time()
            self.values['_id'] = Utils.create_id(hash_str=self.values['email'])
            self.values['is_active'] = True

            # Retrieve username list, choose random and assign to user, mark and save username list
            username_list_doc = g.db['username_list']
            username_list = ast.literal_eval(username_list_doc.get('username_list'))
            chosen_name = None
            for idx, val in enumerate(username_list):
                if val[1] is False:
                    chosen_name = val[0]
                    username_list[idx] = (val[0], self.values['email'])
                    break
            if chosen_name is None:  # Name cannot be assigned
                print("chosen_name is None")
                return None
            else:  # Assign name to user and finish creation
                self.values["username"] = chosen_name
                username_list_doc['username_list'] = str(username_list)
                username_list_doc.save()

            doc = g.db.create_document(self.values)
            doc.save()
            return self.values['_id']
        else:
            return None

    @staticmethod
    def user_exists(email):
        found_user = User.find_user(email)
        return True if found_user is not None else False

    @staticmethod
    def find_user(email=None, user_id=None):
        """Searches for the user in the database.

        Retrieves the User document from the database using the user_id.

        Args:
            email: The email of the user.

        Returns:
            A User object populated with the fields from the database.

        Raises:
            IndexError: Unable to find document in the database.
        """
        try:
            doc_user_id = ''
            if email and not user_id:
                doc_user_id = Utils.create_id(hash_str=email)
            elif not email and user_id:
                doc_user_id = user_id
            user_doc = g.db[doc_user_id]
            user_found = User(first_name=user_doc.get('first_name'),
                              last_name=user_doc.get('last_name'),
                              email=user_doc.get('email'),
                              password=user_doc.get('password'),
                              is_active=user_doc.get('is_active'),
                              _id=user_doc.get('_id'),
                              created_on=user_doc.get('created_on'),
                              username=user_doc.get('username'))
            return user_found
        except KeyError:
            return None

    @staticmethod
    def generate_password(password):
        return generate_password_hash(password, salt_length=8)

    def to_dict(self):
        data = {
            'firstname': self.values['first_name'],
            'lastname': self.values['last_name'],
            'email': self.values['email'],
            'created_on': datetime.fromtimestamp(self.values['created_on'])
                                  .strftime("%b %-d, %Y"),
            'username': self.values['username']
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.generate_password(data['password'])

    def get_token(self, expires_in=3600, email=None):
        now = time.time()
        if self.values['token'] and self.values['token_expiration'] > now + 60:
            return self.values['token']
        self.values['token'] = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.values['token_expiration'] = now + expires_in

        user_id = Utils.create_id(hash_str=email)
        user_doc = g.db[user_id]
        user_doc['token'] = self.values['token']
        user_doc['token_expiration'] = self.values['token_expiration']
        user_doc.save()
        return self.values['token']

    def revoke_token(self):
        self.values['token_expiration'] = time.time() - 1

    @staticmethod
    def check_token(token=None):
        retrieved = g.user_token_view(startkey=[token, {}], endkey=[token], descending=True, include_docs=True)
        if len(retrieved['rows']) == 0:
            return None

        row = retrieved['rows'][0]
        user_found = User(email=row['doc'].get('email'), first_name=row['doc'].get('first_name'),
                          last_name=row['doc'].get('last_name'), is_active=row['doc'].get('is_active'),
                          created_on=row['doc'].get('created_on'), token=row['doc'].get('token'),
                          token_expiration=row['doc'].get('token_expiration'), password=row['doc'].get('password'))
        user_found.token = row['doc'].get('token')
        user_found.token_expiration = row['doc'].get('token_expiration')

        if user_found is None or user_found.token_expiration < time.time():
            return None
        return user_found
