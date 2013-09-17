import datetime
import database
from flask import Flask, render_template #, url_for

ARCHIVE_LISTING_SHOTS = 3*2 + 6*3
HOME_TODAY_SHOTS = 6
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
    return "ok"
    
if __name__ == '__main__':
    app.run(debug=True)