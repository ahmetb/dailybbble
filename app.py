import datetime
import database
from dateutil.relativedelta import relativedelta
import calendar
import os
from flask import Flask, render_template, redirect, url_for


ARCHIVE_LISTING_SHOTS = 3*2 + 6*4
HOME_TODAY_SHOTS = 6
CALENDAR_START = datetime.date(2013, 05, 30)
app = Flask(__name__)


@app.route('/')
def home():
    today_utc = datetime.datetime.utcnow().date() - datetime.timedelta(days=1)
    today_popular = database.popular_shots_of_day(today_utc, HOME_TODAY_SHOTS)
    return render_template('pages/home.html', today_popular=today_popular,
                           today=today_utc)


@app.route('/archive/<int:year>/<int:month>/<int:day>/')
def archive_day(year, month, day):
    date = datetime.date(year, month, day)
    shots = database.popular_shots_of_day(date, ARCHIVE_LISTING_SHOTS)
    return render_template('pages/archive_day.html', shots=shots,
                            day=date)


@app.route('/archive/<int:year>/<int:month>/')
def archive_month(year, month):
    calendar_start_month = datetime.date(CALENDAR_START.year,
                                         CALENDAR_START.month, 1)
    
    first_month_redir = redirect(url_for('archive_month',
                                        year=CALENDAR_START.year,
                                        month=CALENDAR_START.month));
    if year == 0 or month == 0:
        return first_month_redir

    date = datetime.date(year, month, 1)
    if date < calendar_start_month:
        return first_month_redir

    cal = calendar.Calendar()
    days = list(cal.itermonthdays2(date.year, date.month))

    today = datetime.datetime.utcnow().date()
    prev = date - relativedelta(months=1)
    next = date + relativedelta(months=1)
    prev_disabled = prev < calendar_start_month
    next_disabled = next > today

    return render_template('pages/archive_month.html', date=date, days=days,
                            prev=prev, prev_disabled=prev_disabled,
                            next=next, next_disabled=next_disabled,
                            today=today)

if __name__ == '__main__':
    port = int(os.environ['PORT']) if 'PORT' in os.environ else None
    debug = True if not port else False
    app.run(port=port, debug=debug)