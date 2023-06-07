import pdb
import time
from cloudant.client import Cloudant
from cloudant.design_document import DesignDocument
from cloudant.view import View

from flask_apscheduler import scheduler

from . import Utils
from flask import g
import ast


class Notification:
    def __init__(self, email=None, _id=None, created_on=None, notification=None, start_time=None,
                 end_time=None):
        self.values = {'email': email, 'type': 'notification', 'created_on': created_on,
                       'notification': notification}

        if _id is not None:
            self.values['_id'] = _id

    def __str__(self):
        return str(self.values)

    def get_id(self):
        return self.values['_id']

    def create_data(self):
        self.values['created_on'] = time.time()
        hash_str = self.values['email'] + str(self.values['created_on'])
        self.values['_id'] = (Utils.create_id(hash_str=hash_str))

        doc = g.db.create_document(self.values)
        doc.save()
        return self.values['_id']

    @staticmethod
    def find_notification(start_time=None, end_time=None, email=None):
        try:
            if email and start_time and end_time:
                retrieved = g.notification_email_view(key=email, include_docs=True, limit=1000)
            else:
                retrieved = g.notification_view(startkey=[email, start_time],
                                                endkey=[email, end_time],
                                                include_docs=True, limit=1000)

            res = []
            for row in retrieved['rows']:
                res.append(row['doc']['notification'])
            return res

        except KeyError as e:
            print(e)
            return None

    @staticmethod
    def delete_notification(email=None, start_time=None, end_time=None):
        try:
            retrieved = g.notification_delete_view(startkey=[email, float(start_time)],
                                                   endkey=[email, float(end_time)],
                                                   include_docs=True)

            to_delete = []
            for row in retrieved['rows']:
                _id = row['value'][0]
                _rev = row['value'][1]
                to_delete.append({"_id": _id, "_rev": _rev, "_deleted": True})

            g.db.bulk_docs(to_delete)
            return to_delete

        except KeyError as e:
            print(e)
            return None

    # Finds pairs of collecting_data=True/False and calculates difference between timestamps to get
    # total time spent collecting data
    @staticmethod
    def retrieve_collecting_data_timestamps(view, db):  # tc = O(nlogn), sp = O(n)
        response = {}

        if view:
            retrieved = view()
        else:
            retrieved = g.collecting_data_timestamps_view()
        timestamps_dict = {}  # key is email, value is tuple (true/false, timestamp)  test@gmail.com: (true, 1) (false, 3) (true, 5) ( false, 7)

        for row in retrieved['rows']:
            if row['key'] in timestamps_dict:
                val1 = True if row['value'][0] == "true" else False
                timestamps_dict[row['key']].append((val1, int(row['value'][1])))
            else:
                val1 = True if row['value'][0] == "true" else False
                timestamps_dict[row['key']] = [(val1, int(row['value'][1]))]

        for key in timestamps_dict:
            timestamps_dict[key].sort(key=lambda x: x[1], reverse=True)

        # Calculate total time for each user, using true/false pairs
        for key in timestamps_dict:
            total_time = 0
            calc_next = False
            running_val = 0
            for val in timestamps_dict[key]:
                if calc_next:
                    if val[0]:
                        running_val = 0
                        calc_next = False
                        continue
                    running_val -= val[1]
                    total_time += running_val
                    calc_next = False
                elif not val[0]:
                    calc_next = True
                    running_val = val[1]
            response[key] = {'total_time_minutes': int(total_time / 60)}

        # Convert email to username
        new_response = {}
        if db:
            username_list_doc = db['username_list']
        else:
            username_list_doc = g.db['username_list']
        username_list = ast.literal_eval(username_list_doc.get('username_list'))
        for key in response:
            for username, email in username_list:
                if email == key:
                    new_response[username] = response[key]
                    break
        print(new_response)
        return new_response

    # @staticmethod
    # def leaderboard_update_job():
    # leaderboard_dict = Notification.retrieve_collecting_data_timestamps()
    # leaderboard_doc = g.db['leaderboard_stats']
    # leaderboard_doc['stats'] = leaderboard_dict
    # leaderboard_doc.save()

    @staticmethod
    def leaderboard_update_job():
        try:
            DATABASE_NAME = "testing_database"
            USERNAME = "apikey-3730efc62a2b4511b2e06864bd07665f"
            PASSWORD = "2f597ad5576f71b62bf37603b383fa96811fc285"
            URL = "https://d4182120-61de-4f84-a811-078a6712c9d7-bluemix.cloudant.com"

            client = Cloudant(USERNAME, PASSWORD, url=URL, connect=True)

            client.connect()
            db = client[DATABASE_NAME]
        except:
            print('error')
            raise

        print(db.design_documents())
        collecting_data_timestamps_ddoc = DesignDocument(db, '_design/notification')
        collecting_data_timestamps_view = View(collecting_data_timestamps_ddoc,
                                               'collecting-data-timestamps')

        pdb.set_trace()
        # stats = db['leaderboard_stats']

        leaderboard_dict = Notification.retrieve_collecting_data_timestamps(view=collecting_data_timestamps_view, db=db)
        leaderboard_doc = db['leaderboard_stats']
        leaderboard_doc['stats'] = leaderboard_dict
        leaderboard_doc.save()

        # client.disconnect()
