from flask import Flask, g, session
from flask_apscheduler import APScheduler
from flask_login import LoginManager, current_user
from config import config
from cloudant.client import Cloudant
from cloudant.design_document import DesignDocument
from cloudant.view import View
from .classes import User, Notification
import pdb

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # initialize schedular
    scheduler = APScheduler()
    scheduler.init_app(app)

    @scheduler.task('interval', seconds=10, misfire_grace_time=15)
    def job():
        print("job executed")
        with app.app_context():
            # pdb.set_trace()
            Notification.leaderboard_update_job()

    scheduler.start()

    login_manager.init_app(app)

    @app.before_request
    def before_request():
        if not hasattr(g, 'db'):
            connect = connect_db(config[config_name])
            g.db = connect[0]
            g.client = connect[1]
        if not hasattr(g, 'user_view'):
            user_ddoc = DesignDocument(g.db, '_design/user')
            g.user_view = View(user_ddoc, 'user-view')
        if not hasattr(g, 'user_token_view'):
            user_token_ddoc = DesignDocument(g.db, '_design/user')
            g.user_token_view = View(user_token_ddoc, 'user-token-view')
        if not hasattr(g, 'post_view'):
            post_ddoc = DesignDocument(g.db, '_design/post')
            g.post_view = View(post_ddoc, 'post-view')
        if not hasattr(g, 'data_view'):
            data_ddoc = DesignDocument(g.db, '_design/data')
            g.data_view = View(data_ddoc, 'data-view')
        if not hasattr(g, 'data_email_view'):
            data_email_ddoc = DesignDocument(g.db, '_design/data')
            g.data_email_view = View(data_email_ddoc, 'data-email-view')
        if not hasattr(g, 'data_time_view'):
            data_time_ddoc = DesignDocument(g.db, '_design/data')
            g.data_time_view = View(data_time_ddoc, 'data-time-view')
        if not hasattr(g, 'data_delete_view'):
            data_delete_ddoc = DesignDocument(g.db, '_design/data')
            g.data_delete_view = View(data_delete_ddoc, 'data-delete-view')
        if not hasattr(g, 'notification_view'):
            notification_ddoc = DesignDocument(g.db, '_design/notification')
            g.notification_view = View(notification_ddoc, 'notification-view')
        if not hasattr(g, 'notification_email_view'):
            notification_email_ddoc = DesignDocument(g.db, '_design/notification')
            g.notification_email_view = View(notification_email_ddoc, 'notification-email-view')
        if not hasattr(g, 'notification_delete_view'):
            notification_delete_ddoc = DesignDocument(g.db, '_design/notification')
            g.notification_delete_view = View(notification_delete_ddoc, 'notification-delete-view')
        if not hasattr(g, 'collecting-data-timestamps'):
            collecting_data_timestamps_ddoc = DesignDocument(g.db, '_design/notification')
            g.collecting_data_timestamps_view = View(collecting_data_timestamps_ddoc,
                                                     'collecting-data-timestamps')

    @app.teardown_appcontext
    def close_db(error):
        if hasattr(g, 'client'):
            g.client.disconnect()

    # Setup Blueprints
    from .main import main as main_blueprint
    from .user import user as user_blueprint
    from .api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


def connect_db(config_obj):
    try:
        client = Cloudant(config_obj.USERNAME, config_obj.PASSWORD,
                          url=config_obj.URL, connect=True)
        client.connect()
        db = client[config_obj.DATABASE_NAME]
    except:
        raise
    return [db, client]
