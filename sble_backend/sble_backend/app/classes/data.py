import time
from . import Utils
from flask import g
from cloudant.document import Document


class Data:
    def __init__(self, email=None, _id=None, created_on=None, data=None, beacon_majors=None,
                 start_time=None, bbox_botleft=None, bbox_topright=None):
        self.values = {'email': email, 'type': 'data', 'created_on': created_on,
                       'data': data, 'beacon_majors': beacon_majors}

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

        # Choose first timestamp as start_time
        self.values['start_time'] = self.values['data'][0]['timestamp']

        # Extract beacon_majors
        ble_majors = set()
        for sample in self.values['data']:
            ble_entries = sample.get('BLE')
            for i in range(len(ble_entries)):
                ble_entry = ble_entries[i]
                ble_major = ble_entry.get('major')
                ble_majors.add(ble_major)
        self.values['beacon_majors'] = list(ble_majors)

        doc = g.db.create_document(self.values)
        doc.save()
        return self.values['_id']

    @staticmethod
    def find_data(email=None, start_time=None, end_time=None, beacon_major=None, bbox_botleft=None,
                  bbox_topright=None):
        """Searches for the data in the database.
        Retrieves all the data documents of the current user from the database using the email.

        Args:
            email: The email of the user of the data.

        Returns:
            A list of data object populated with the fields from the database.

        Raises:
            IndexError: Unable to find the document in the database.
        """
        try:
            # Convert the type of the parameters into the correct type
            beacon_major = int(beacon_major) if beacon_major is not None else None
            s_time = int(start_time) if start_time is not None else None
            e_time = int(end_time) if end_time is not None else None
            b_bl = bbox_botleft if bbox_botleft is not None else None
            b_tr = bbox_topright if bbox_topright is not None else None

            if email is None and (s_time is None or e_time is None):
                response = {'status': 'Missing email address or time interval'}
                return response
            if email and (s_time is None or e_time is None):
                retrieved = g.data_email_view(key=email, include_docs=True, limit=1000)
            if email is None and (s_time and e_time):
                if e_time - s_time >= 1010000:
                    response = {'status':
                                'The time range is too long, please limit to less than two week'}
                    return response
                else:
                    retrieved = g.data_time_view(startkey=s_time, endkey=e_time, include_docs=True,
                                                 limit=1000)
            if email and s_time and e_time:
                retrieved = g.data_view(startkey=[email, s_time], endkey=[email, e_time],
                                        include_docs=True, limit=1000)

            res = []
            for row in retrieved['rows']:
                # if row['value'][0] and row['value'][1] and row['value'][2]:
                #     b_major = row['value'][0]
                #     y = row['value'][1]
                #     x = row['value'][2]
                #     if beacon_major:
                #         if beacon_major not in b_major:
                #             continue
                #     if b_bl and b_tr:
                #         if not ((b_bl[1] <= x <= b_tr[1]) and b_bl[0] <= y <= b_tr[0]):
                #             continue
                #     else:
                #         res.append(row['doc']['data'])
                for data in row['doc']['data']:
                    res.append(data)

            res = sorted(res, key=lambda _entry: _entry.get('timestamp'))
            return res

        except KeyError as e:
            print(e)
            return None

    @staticmethod
    def delete_data(email=None, start_time=None, end_time=None):
        try:
            if email is None or start_time is None or end_time is None:
                return {'status': "Missing parameters"}
            retrieved = g.data_delete_view(startkey=[email, float(start_time)],
                                           endkey=[email, float(end_time)], include_docs=True)

            to_delete = []
            print(retrieved)
            for row in retrieved['rows']:
                _id = row['value'][0]
                _rev = row['value'][1]
                to_delete.append({"_id": _id, "_rev": _rev, "_deleted": True})

            g.db.bulk_docs(to_delete)
            return to_delete

        except KeyError as e:
            print(e)
            return None
