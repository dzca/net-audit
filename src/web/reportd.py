#!/usr/bin/python
#https://github.com/mitsuhiko/flask/tree/master/examples/flaskr
from flask import Flask, render_template, session, redirect, url_for, \
    request, flash
from utils.logger import Logger
from query.query_parser import QueryParser
from db.mongodb import MongoDB
from pager import Pager
import pymongo, ConfigParser
from datetime import datetime

#from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
logger = Logger().getLogger("web.events")
config = ConfigParser.ConfigParser()

parser = QueryParser()
db = MongoDB('esm')
page_size = 25
quest_dict = {}

app.secret_key = '^\x1b\x08\xd3\xc5\xd7\x9c8\xbd\xfa\xf5\x98\xe2h\x1bi\xa3\nML\x92\xbf\xac\x80'

    
def get_users(user_name):
    cursor = db.get_user(user_name)
    users = {}
    for u in cursor:
        users[u['username']] = u['password']
    return users

@app.route('/')
def index():
    if not 'user_id' in session:
        return redirect('/login')
    else:
        return redirect('/event')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users(username)
        if not users.has_key(username) :
            error = 'Invalid username'
        elif password != users[username]:
            logger.debug('pwd is ' + password)
            error = 'Invalid password'
        else:
            session['user_id'] = username
            flash('You were logged in')
#            return redirect(url_for('event'))
            return redirect('/event')
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.tpl', error=error)

@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/help')
def help_controller():
    return render_template('help.tpl')

@app.route('/event', methods=['GET'])
def events_default_controller(page_num=1):
    if not 'user_id' in session:
        return redirect('/login')
    else:
        if 'event_query' in session:
            session['event_query'] = None
    
        events = get_events(page_size, 1, {})
        pager = Pager(page_size, count_events({}), 1)
        return render_template('events.tpl', events = events, pager = pager)

def count_events(query):
    return db.count("events", query)
    
    
def get_events(size, page, query):
    event_cursor = db.find('events',size, page, 'create_time',pymongo.DESCENDING, query)
    events = []
    
    i = size * (page - 1) + 1
    for e in event_cursor:
        event = {}
        event['index'] = i
        event['time'] = e.get('create_time').strftime("%Y-%m-%dT%H:%M:%SZ")
        event['domain'] = e.get('domain')
        event['ip'] = e.get('ip')
        event['size'] = e.get('size')
        events.append(event)
        i += 1
    return events

@app.route('/event/<int:page>', methods=['GET'])
def events_page_controller(page=1):
    '''Controller to initialize the quest Form'''
    if not 'user_id' in session:
        return redirect('/login')
    else:
        if 'event_query' in session:
            query_string = session['event_query']
            if query_string is not None and len(query_string) > 0:
                query = parser.parse(query_string)
                logger.debug('query_string=' + query_string)
            else:
                session['event_query'] = None
                query = {}
        else:
            query = {}
        
        events = get_events(page_size, page, query)
        pager = Pager(page_size, count_events(query), page)
        return render_template('events.tpl', events = events, pager = pager)
    
@app.route('/event', methods=['POST'])
def events_form_controller():
    if not 'user_id' in session:
        return redirect('/login')
    else:
        query_string = request.form['event_query'].strip()
        if query_string is not None and len(query_string) > 0:
            session['event_query'] = query_string
            query = parser.parse(query_string)
            logger.debug('query_string=' + query_string)
        else:
            query = {}
        
        events = get_events(page_size, 1, query)
        pager = Pager(page_size, count_events(query), 1)
        return render_template('events.tpl', events = events, pager = pager)

@app.route('/stat', methods=['GET'])
def stat_form_controller():
    '''Controller to initialize the statistics Form'''
    
    if not 'user_id' in session:
        return redirect('/login')
    else:
        #default statics is current day's statistics
        current_date = datetime.now().strftime("%Y-%m-%d")
        stat_quest = 'time in ' + current_date
        db_query = parser.parse(stat_quest)
        logger.debug(db_query)
        stats = get_stats(db_query)
        logger.debug(stats)
        return render_template('stat.tpl', stats = stats, time = current_date)

@app.route('/monthly', methods=['GET'])
def stat_monthly_controller():
    '''Controller to initialize the statistics Form'''
    if not 'user_id' in session:
        return redirect('/login')
    else:
        #default statics is current day's statistics
        current_month = datetime.now().strftime("%Y-%m")
        stat_quest = 'time in ' + current_month
        db_query = parser.parse(stat_quest)
        logger.debug(db_query)
        stats = get_stats(db_query)
    #    logger.debug(stats)
    #    stats = []
        return render_template('stat.tpl', stats = stats, time = current_month)

def get_stats(query):
    stats_cursor = db.countSize('events',query)
    stats = []
    
    for s in stats_cursor:
        stat = {}
        stat['ip'] = s.get('ip')
        stat['size'] = s.get('size')
        stats.append(stat)
    return stats

@app.route('/stat', methods=['POST'])
def stat_controller():
    '''Controller to initialize the statistics Form'''
    if not 'user_id' in session:
        return redirect('/login')
    else:
        stat_quest = request.form['stat_query'].strip()
        #default statics is current day's statistics
        db_query = parser.parse(stat_quest)
        logger.debug(db_query)
        stats = get_stats(db_query)
        return render_template('stat.tpl', stats = stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)