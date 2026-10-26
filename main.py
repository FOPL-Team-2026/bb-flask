from api.fopl_connection_api import fopl_connection_api

from api.fopl_auth_api import fopl_auth_api  # FOPL login/register

from api.fopl_admin_api import fopl_admin_api  # FOPL admin dashboard

from api.fopl_puzzle_api import fopl_puzzle_api  # FOPL puzzle stats

from api.fopl_book_api import fopl_book_api       # FOPL book CRUD

from api.fopl_chat_api import fopl_chat_api       # FOPL AI search + chatbot

from api.fopl_calendar_api import fopl_calendar_api  # FOPL calendar events

from api.fopl_facematch_api import fopl_facematch_api  # FOPL face match

from api.fopl_volunteer_api import fopl_volunteer_api  # FOPL volunteer applications

from model.fopl_user import FoplUser

from model.fopl_puzzle import FoplPuzzleStat  # ensures table is created

from model.fopl_book   import FoplBook  # book catalog model

from model.fopl_event  import FoplEvent  # calendar events model

from model.fopl_volunteer import FoplVolunteerApplication  # ensures table is created

from scripts.fopl_seed import initFoplUsers, initFoplBooks, updateFoplBookPrices  # seed data


# imports from flask
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify, current_app, g # import render_template from "public" flask libraries
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup
from flask_login import current_user, login_required
from flask import current_app
from dotenv import load_dotenv

# import "objects" from "this" project
from __init__ import app, db, login_manager  # Key Flask objects 
from model.persona import Persona, initPersonas, initPersonaUsers
from model.presence_schedule import seed_schedules
# API endpoints
from api.user import user_api 
from api.python_exec_api import python_exec_api
from api.javascript_exec_api import javascript_exec_api
from api.section import section_api
from api.persona_api import persona_api
from api.skill_snapshot_api import skill_passport_api
from api.pfp import pfp_api
from api.analytics import analytics_api
from api.student import student_api
from api.groq_api import groq_api
from api.gemini_api import gemini_api
from api.ainpc_api import ainpc_api
from api.microblog_api import microblog_api
from api.classroom_api import classroom_api
from api.data_export_import_api import data_export_import_api
from api.leaderboard import dynamic_api, events_api
from hacks.joke import joke_api  # Import the joke API blueprint
from api.post import post_api  # Import the social media post API
from api.congrats_api import congrats_api  # Import the congrats API
from api.profile_game import profile_game_api  # CS Pathway Game profile persistence
from api.snapshot_proxy import snapshot_proxy
from api.rfid_api import rfid_api
from api.presence_api import presence_api
#from api.announcement import announcement_api ##temporary revert

# database Initialization functions
from model.user import User, initUsers
from model.user import Section;
from model.github import GitHubUser
from model.feedback import Feedback
from api.analytics import get_date_range
# from api.grade_api import grade_api
from api.study import study_api
from api.feedback_api import feedback_api
from model.study import Study, initStudies
from model.classroom import Classroom
from model.skill_snapshot import SkillSnapshot
from model.post import Post, init_posts
from model.microblog import MicroBlog, Topic, initMicroblogs
from model.leaderboard import ScoreCounterEvent, ElementaryLeaderboardEvent
from hacks.jokes import initJokes 
# from model.announcement import Announcement ##temporary revert

# server only Views

import os

# Load environment variables
load_dotenv()



# register URIs for api endpoints
app.register_blueprint(python_exec_api)
app.register_blueprint(javascript_exec_api)
app.register_blueprint(user_api)
app.register_blueprint(section_api)
app.register_blueprint(persona_api)
app.register_blueprint(skill_passport_api)
app.register_blueprint(pfp_api) 
app.register_blueprint(groq_api)
app.register_blueprint(gemini_api)
app.register_blueprint(ainpc_api)
app.register_blueprint(microblog_api)

app.register_blueprint(analytics_api)
app.register_blueprint(student_api)
# app.register_blueprint(grade_api)
app.register_blueprint(study_api)
app.register_blueprint(classroom_api)
app.register_blueprint(feedback_api)
app.register_blueprint(data_export_import_api)  # Register the data export/import API
app.register_blueprint(dynamic_api)  # Register the dynamic leaderboard API
app.register_blueprint(events_api)  # Register the elementary leaderboard API
app.register_blueprint(joke_api)  # Register the joke API blueprint
app.register_blueprint(post_api)  # Register the social media post API
app.register_blueprint(congrats_api)  # Register the congrats message API
app.register_blueprint(profile_game_api)  # CS Pathway Game profile persistence
app.register_blueprint(snapshot_proxy)  # Register the snapshot proxy API
app.register_blueprint(rfid_api)  # Register the RFID attendance API
app.register_blueprint(presence_api)  # Register the generic presence event API
# app.register_blueprint(announcement_api) ##temporary revert

app.register_blueprint(fopl_connection_api)

app.register_blueprint(fopl_auth_api)   # FOPL login/register

app.register_blueprint(fopl_admin_api)  # FOPL admin dashboard

app.register_blueprint(fopl_puzzle_api) # FOPL puzzle stats

app.register_blueprint(fopl_book_api)   # FOPL book CRUD

app.register_blueprint(fopl_chat_api)   # FOPL AI search + chatbot

app.register_blueprint(fopl_calendar_api) # FOPL calendar events

app.register_blueprint(fopl_facematch_api)   # FOPL face match

app.register_blueprint(fopl_volunteer_api)  # FOPL volunteer applications


# Jokes file initialization
with app.app_context():
    initJokes()
    initFoplUsers()
    initFoplBooks()
    updateFoplBookPrices()

# Tell Flask-Login the view function name of your login route
login_manager.login_view = "login"

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login', next=request.path))

# register URIs for server pages
@login_manager.user_loader
def load_user(user_id):
    # user_id is the composite "id:token_version" from User.get_id(). A mismatched
    # token_version means the session predates a password change on this account --
    # returning None here tells Flask-Login the session is invalid.
    #
    # A session issued before this field existed at all has no ":" -- treat that as
    # token_version "0" (matching a fresh/unchanged account) instead of invalidating
    # it outright. It still correctly fails below once the account's real
    # token_version has moved past 0 from an actual password change.
    if ":" in user_id:
        raw_id, token_version = user_id.split(":", 1)
    else:
        raw_id, token_version = user_id, "0"
    try:
        raw_id = int(raw_id)
    except ValueError:
        return None
    user = User.query.get(raw_id)
    if user is None or str(user.token_version) != token_version:
        return None
    return user

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Helper function to check if the URL is safe for redirects
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/ocslogin', methods=['GET', 'POST'])
def login():
    error = None
    next_page = request.args.get('next', '') or request.form.get('next', '')
    if request.method == 'POST':
        user = User.query.filter_by(_uid=request.form['username']).first()
        if user and user.is_password(request.form['password']) and not user.active:
            error = 'Account pending verification.'
        elif user and user.is_password(request.form['password']):
            login_user(user)
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template("login.html", error=error, next=next_page)

@app.route('/studytracker')  # route for the study tracker page
def studytracker():
    return render_template("studytracker.html")

@app.route('/congrats')
@login_required
def congrats():
    from model.congrats_message import CongratsMessage

    messages = CongratsMessage.get_by_user(current_user.id)
    return render_template("congrats.html", messages=messages, project="Congrats Messages")
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    print("Home:", current_user)
    return render_template("index.html")



@app.route('/users/table2')
@login_required
def u2table():
    users = User.query.all()
    return render_template("u2table.html", user_data=users, role_options=current_user.grantable_roles())

@app.route('/sections/')
@login_required
def sections():
    sections = Section.query.all()
    return render_template("sections.html", sections=sections)

@app.route('/persona/')
@login_required
def persona():
    personas = Persona.query.all()
    return render_template("persona.html", personas=personas)

# Helper function to extract uploads for a user (ie PFP image)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
 
@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        blocker = user.deletion_blocker(current_user)
        if blocker:
            return jsonify({'error': blocker[1]}), blocker[0]
        user.delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Set the new password
    if user.update({"password": app.config['DEFAULT_PASSWORD']}):
        return jsonify({'message': 'Password reset successfully'}), 200
    return jsonify({'error': 'Password reset failed'}), 500

@app.route('/update_user/<string:uid>', methods=['PUT'])
def update_user(uid):
    # Authorization check
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403

    # Get the JSON data from the request
    data = request.get_json()
    print(f"Request Data: {data}")  # Log the incoming data

    # Find the user in the database
    user = User.query.filter_by(_uid=uid).first()
    if user:
        print(f"Found user: {user.uid}")  # Log the found user's UID
        
        # Update the user using the provided data
        user.update(data)  # Assuming `user.update(data)` is a method on your User model
        
        # Save changes to the database
        return jsonify({"message": "User updated successfully."}), 200
    else:
        print("User not found.")  # Log when user is not found
        return jsonify({"message": "User not found."}), 404



    
@app.route('/login')
def fopl_login_page():
    next_url = request.args.get('next', '')
    return render_template('fopl_login.html', next=next_url, error=None)


@app.route('/fopl/admin')
def fopl_admin_dashboard():
    """FOPL admin dashboard — server-rendered."""
    import jwt as pyjwt
    from model.fopl_user import FoplUser
    from model.fopl_book import FoplBook
    from model.fopl_event import FoplEvent
    from model.fopl_puzzle import FoplPuzzleStat

    token = request.cookies.get('fopl_token')
    if not token:
        return redirect('/login?next=/fopl/admin')
    try:
        data = pyjwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = FoplUser.query.get(data.get('fopl_id'))
        if not user or not user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
    except Exception:
        return redirect('/login?next=/fopl/admin')

    users = FoplUser.query.order_by(FoplUser.created_at.desc()).all()
    books = FoplBook.query.all()
    game_stats = FoplPuzzleStat.query.all()

    by_age = {}
    by_condition = {}
    for b in books:
        by_age[b._age_group]       = by_age.get(b._age_group, 0) + b._quantity
        by_condition[b._condition] = by_condition.get(b._condition, 0) + b._quantity

    by_game = {}
    for s in game_stats:
        if s._game not in by_game:
            by_game[s._game] = {'sessions': 0, 'wins': 0}
        by_game[s._game]['sessions'] += s._games_played
        by_game[s._game]['wins']     += s._games_won

    stats = {
        'users': {
            'total':   len(users),
            'admins':  sum(1 for u in users if u.is_admin()),
            'members': sum(1 for u in users if not u.is_admin()),
            'list':    [u.read() for u in users],
        },
        'books': {
            'total_titles':    len(books),
            'total_inventory': sum(b._quantity for b in books),
            'total_value':     round(sum(b._price * b._quantity for b in books), 2),
            'by_age_group':    by_age,
            'by_condition':    by_condition,
        },
        'games': {
            'total_sessions': sum(s._games_played for s in game_stats),
            'total_wins':     sum(s._games_won for s in game_stats),
            'by_game':        by_game,
        },
        'events': {
            'total': FoplEvent.query.count(),
        },
    }
    return render_template('fopl_admin.html', stats=stats)


@app.route('/fopl/db')
def fopl_db_viewer():
    """FOPL database viewer — FOPL Admin only."""
    import sqlite3
    import jwt as pyjwt

    # Verify FOPL admin token
    token = request.cookies.get('fopl_token')
    if not token:
        return redirect('/login?next=/fopl/db')
    try:
        data = pyjwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        from model.fopl_user import FoplUser
        user = FoplUser.query.get(data.get('fopl_id'))
        if not user or not user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
    except Exception:
        return redirect('/login')

    db_path = os.path.join(current_app.instance_path, 'volumes', 'user_management.db')
    if not os.path.exists(db_path):
        db_path = os.path.join(current_app.instance_path, 'user_management.db')

    selected_table = request.args.get('table')
    tables, columns, rows, schema = [], [], [], []
    row_count, row_counts = 0, {}

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [r[0] for r in cursor.fetchall()]
        for t in tables:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM "{t}"')
                row_counts[t] = cursor.fetchone()[0]
            except Exception:
                row_counts[t] = None
        if selected_table and selected_table in tables:
            cursor.execute(f'PRAGMA table_info("{selected_table}")')
            schema = [{'cid': r[0], 'name': r[1], 'type': r[2], 'notnull': r[3], 'dflt_value': r[4], 'pk': r[5]}
                      for r in cursor.fetchall()]
            columns = [s['name'] for s in schema]
            cursor.execute(f'SELECT * FROM "{selected_table}" LIMIT 1000')
            rows = [list(r) for r in cursor.fetchall()]
            row_count = row_counts.get(selected_table, len(rows))
        conn.close()
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    return render_template('fopl_db_viewer.html',
                           tables=tables,
                           selected_table=selected_table,
                           columns=columns,
                           rows=rows,
                           schema=schema,
                           row_count=row_count,
                           row_counts=row_counts)


app.add_url_rule("/ocslogin", endpoint="ocs_login", view_func=login, methods=["GET", "POST"])

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to run the data generation functions
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initMicroblogs()
    initPersonas()
    initPersonaUsers()
    seed_schedules()  # presence schedules from model/presence_schedules.json

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the flask application on the development server
if __name__ == "__main__":
    host = "0.0.0.0"
    port = app.config['FLASK_PORT']
    print(f"** Server running: http://localhost:{port}")  # Pretty link
    app.run(debug=True, host=host, port=port, use_reloader=False)
