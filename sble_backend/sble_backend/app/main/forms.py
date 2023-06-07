from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    post = TextAreaField('say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class DataForm(FlaskForm):
    months = [(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'),
              (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'),
              (11, 'Nov'), (12, 'Dec')]
    days = [(i+1, i+1) for i in range(31)]
    years = [(2022, 2022), (2023, 2023)]
    hours = [(i+1, i+1) for i in range(11)]
    hours.insert(0, (0, 12))
    minutes = [(i, "{:02d}".format(i)) for i in range(60)]
    periods = [(0, 'AM'), (12, 'PM')]

    start_month = SelectField('Month:', choices=months)
    start_day = SelectField('Day:', choices=days)
    start_year = SelectField('Year:', choices=years)
    start_hour = SelectField('Hour:', choices=hours)
    start_minute = SelectField('Minute:', choices=minutes)
    start_period = SelectField('Period:', choices=periods)
    end_month = SelectField('Month:', choices=months)
    end_day = SelectField('Day:', choices=days)
    end_year = SelectField('Year:', choices=years)
    end_hour = SelectField('Hour:', choices=hours)
    end_minute = SelectField('Minute:', choices=minutes)
    end_period = SelectField('Period:', choices=periods)

    beacon_major = StringField('Beacon Major ID:')
    bbox_botleft = StringField('Bounding Box Bottom Left:')
    bbox_topright = StringField('Bounding Box Top Right:')
    submit = SubmitField('Search')
