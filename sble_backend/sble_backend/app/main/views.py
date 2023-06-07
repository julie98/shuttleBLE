from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import main
from .forms import PostForm, DataForm
from ..classes.post import Post
from ..classes.data import Data
from ..classes.user import User
from ..classes.notification import Notification
from datetime import datetime


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    # print(current_user)
    form = PostForm()
    posts = None
    if current_user.is_authenticated:
        if form.validate_on_submit():
            new_post = Post(email=current_user.values['email'],
                            body=form.post.data)
            new_post.create_post()
            flash('New post submitted.')
            return redirect(url_for('main.index'))
        posts = Post.find_posts(email=current_user.values['email'])

    return render_template('index.html', title='Home Page', form=form, posts=posts)


@main.route('/profile', methods=['GET'])
def profile():
    info = User.find_user(email=current_user.values['email']).to_dict()
    return render_template('profile.html', title='Profile', info=info)


@main.route('/leaderboard', methods=['GET'])
def leaderboard():
    entries = Notification.retrieve_collecting_data_timestamps()
    return render_template('leaderboard.html', title='Leaderboard', entries=entries)


@main.route('/search_data', methods=['GET', 'POST'])
def search_data():
    form = DataForm()
    filtered_data = []
    if current_user.is_authenticated:
        if form.validate_on_submit():
            # Convert start/end time form to datatime timestamp
            start_month = int(form.start_month.data) if form.start_month.data != "" else None
            start_day = int(form.start_day.data) if form.start_day.data != "" else None
            start_year = int(form.start_year.data) if form.start_year.data != "" else None
            start_hour = int(form.start_hour.data) if form.start_hour.data != "" else None
            start_minute = int(form.start_minute.data) if form.start_minute.data != "" else None
            start_period = int(form.start_period.data) if form.start_period.data != "" else None

            end_month = int(form.end_month.data) if form.end_month.data != "" else None
            end_day = int(form.end_day.data) if form.end_day.data != "" else None
            end_year = int(form.end_year.data) if form.end_year.data != "" else None
            end_hour = int(form.end_hour.data) if form.end_hour.data != "" else None
            end_minute = int(form.end_minute.data) if form.end_minute.data != "" else None
            end_period = int(form.end_period.data) if form.end_period.data != "" else None
            try:
                start_timestamp = datetime(start_year, start_month, start_day,
                                           start_hour + start_period, start_minute).timestamp()
                end_timestamp = datetime(end_year, end_month, end_day,
                                         end_hour + end_period, end_minute).timestamp()

                beacon_major = int(form.beacon_major.data) if form.beacon_major.data != "" \
                    else None
                bbox_botleft = float(form.bbox_botleft.data) if form.bbox_botleft.data != "" \
                    else None
                bbox_topright = float(form.bbox_topright.data) if form.bbox_topright.data != "" \
                    else None

                filtered_data = Data.find_data(email=current_user.values['email'],
                                               start_time=start_timestamp,
                                               end_time=end_timestamp,
                                               beacon_major=beacon_major,
                                               bbox_botleft=bbox_botleft,
                                               bbox_topright=bbox_topright)
            except Exception as e:
                return render_template('search_data.html', title='Search Data', form=form,
                                       error="Error: "+ str(e))
    return render_template('search_data.html', title='Search Data', form=form,
                           filtered_data=filtered_data)


@main.route('/maps', methods=['GET'])
def maps():
    return render_template('google_map.html', title='Map')
