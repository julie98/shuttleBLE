import time
from . import Utils
from flask import g


class Post:
    def __init__(self, email=None, body=None, _id=None, created_on=None):
        self.values = {'email': email, 'body': body,
                       'type': 'post', 'created_on': created_on}
        if _id is not None:
            self.values['_id'] = _id

    def __str__(self):
        return str(self.values)

    def get_id(self):
        return self.values['_id']

    def create_post(self):
        self.values['created_on'] = time.time()
        hash_str = self.values['email'] + str(self.values['created_on'])
        self.values['_id'] = (Utils.create_id(hash_str=hash_str))

        doc = g.db.create_document(self.values)
        doc.save()
        return self.values['_id']

    @staticmethod
    def find_posts(email=None):
        """Searches for the posts in the database.

        Retrieves all the Posts document of the current user from the database using the email.

        Args:
            email: The email of the author of the post.

        Returns:
            A list of Post object populated with the fields from the database.

        Raises:
            IndexError: Unable to find document in the database.
        """
        try:
            retrieved = g.post_view(key=email, include_docs=True)
            posts = []
            for row in retrieved['rows']:
                post = Post(email=row['doc'].get('email'), body=row['doc'].get('body'),
                            created_on=row['doc'].get('created_on'))
                # print(row)
                posts.append(post)
            posts = sorted(posts, key=lambda _post: _post.values['created_on'], reverse=True)
            # print(posts)
            return posts

        except KeyError as e:
            print(e)
            return None
