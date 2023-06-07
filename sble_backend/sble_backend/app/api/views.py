from . import api
from .auth import token_auth
from .errors import bad_request, error_response
from ..classes import User, Data, Notification
from flask import jsonify, request, Response, g
from flask_login import current_user
import ast


@api.route('/get_profile', methods=['GET'])
@token_auth.login_required
def get_profile():
    return jsonify(User.find_user(email=token_auth.current_user().values['email']).to_dict())


@api.route('/save_data', methods=['POST'])
@token_auth.login_required
def save_data():
    response = {}
    request_data = request.get_json() or {}
    if request_data.get('data'):
        data = request_data.get('data')
        new_data = Data(email=token_auth.current_user().values['email'], data=data)
        new_data.create_data()
        response = {'status': f"{len(data)} samples saved"}
    else:
        response = {'status': 'Missing data parameter'}
    return jsonify(response)


@api.route('/get_data', methods=['GET'])
@token_auth.login_required
def get_data():
    response = {}
    args = request.args
    email = args.get('email')
    start_time = args.get('start_time')
    end_time = args.get('end_time')
    beacon_major = args.get('beacon_major')
    bbox_botleft = args.get('bbox_botleft')
    bbox_topright = args.get('bbox_topright')
    if bbox_botleft and bbox_topright:
        bbox_botleft = tuple(bbox_botleft.split(','))
        bbox_topright = tuple(bbox_topright.split(','))
    data_found = Data.find_data(email=email, start_time=start_time, end_time=end_time,
                                beacon_major=beacon_major, bbox_botleft=bbox_botleft,
                                bbox_topright=bbox_topright)

    if data_found:
        response['status'] = f"{len(data_found)} samples returned"
        response['data'] = data_found
        return response
    else:
        response = {'status': 'No results found'}
        return response


@api.route('/delete_data', methods=['GET','POST'])
@token_auth.login_required
def delete_data():
    response = {}
    args = request.args
    email = args.get('email')
    start_time = args.get('start_time')
    end_time = args.get('end_time')

    if email is None or start_time is None or end_time is None:
        response['status'] = "Missing email parameter"
        return response

    to_delete = Data.delete_data(email=email, start_time=start_time, end_time=end_time)
    response['status'] = 'ok'
    response['documents deleted'] = len(to_delete)
    return response


@api.route('/save_notifications', methods=['POST'])
@token_auth.login_required
def save_notification():
    response = {}
    notification = request.get_json() or {}
    if notification:
        new_notification = Notification(email=token_auth.current_user().values['email'],
                                        notification=notification)
        new_notification.create_data()
        response['status'] = "Notification saved"
    else:
        response['status'] = "No notifications received"
    return response


@api.route('/get_notifications', methods=['GET'])
@token_auth.login_required
def get_notification():
    response = {}
    args = request.args
    start_time = args.get('start_time')
    end_time = args.get('end_time')
    email = args.get('email')

    if email is None or start_time is None or end_time is None:
        response['status'] = "Missing parameters"
        return response

    notification_found = Notification.find_notification(email=email, start_time=start_time,
                                                        end_time=end_time)
    if notification_found:
        response['status'] = "ok"
        response['notifications'] = notification_found
    else:
        response['status'] = "No notifications found"
    return response


@api.route('/delete_notifications', methods=['GET', 'POST'])
@token_auth.login_required
def delete_notification():
    args = request.args
    start_time = args.get('start_time')
    end_time = args.get('end_time')
    email = args.get('email')
    if email is None:
        response = {'status': 'missing email parameter'}
        return jsonify(response)

    if start_time is None or end_time is None:
        response = {'status': 'missing time_interval parameter'}
        return jsonify(response)

    to_delete = Notification.delete_notification(email=email, start_time=start_time,
                                                 end_time=end_time)

    response = {"document deleted": len(to_delete)}
    return jsonify(response)


@api.route('/retrieve_leaderboard', methods=['GET'])
def retrieve_leaderboard():
    notification_response = Notification.retrieve_collecting_data_timestamps()
    response = {'response': notification_response}
    return response


@api.route('/test', methods=['GET'])
def test():
    content = "1,2,3\n4,5,6\n"
    return Response(content,
                    mimetype='text/csv')
