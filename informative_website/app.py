from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from forum_db import ForumDB
import password_util
import email_util
import uuid
import sqlite3
from datetime import datetime, timezone
from random import randint
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = '14806762'

_forum_db = ForumDB()
_admin_code = '14806762' # given to super user by administrator

conn = sqlite3.connect("data/track.db", check_same_thread=False)
cur = conn.cursor()


NOBODY_EMAIL = 'nobody@nobody'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/facts')
def facts():
    return render_template("facts.html")

@app.route("/solutions")
def solutions():
    return render_template("solutions.html")

@app.route("/community", methods=('GET',))
def community():
    forums = _forum_db.get_all_forums()
    comments = _forum_db.get_all_comments()
    users = _forum_db.get_all_users()
    return render_template('community.html', forums=forums, comments=comments, users=users, find_comments_by_forum_id=find_comments_by_forum_id, find_user_by_email=find_user_by_email)

def find_comments_by_forum_id(forum, all_comments):
    forum_comments = list()
    for comment in all_comments:
        if comment['forum_id'] == forum['id']:
            forum_comments.append(comment)
    return forum_comments

def find_user_by_email(users, email):
    for user in users:
        if user['email'] == email:
            return user
    return None


@app.route('/community/create_forum', methods=('GET', 'POST'))
def create_forum():
    if request.method == 'POST':
        topic = request.form['topic']
        user_email = session['email']
        if not topic:
            flash('Topic is required')
        else:
            _forum_db.create_forum(topic, user_email)
            return redirect(url_for('community'))
    return render_template('create_forum.html')

@app.route('/community/<int:forum_id>/create_comment', methods=('GET', 'POST'))
def create_comment(forum_id):
    if request.method == 'POST':
        comment = request.form['comment']
        user_email = session['email']
        if not comment:
            flash('Comment is required')
        else:
            _forum_db.create_comment(comment, forum_id, user_email)
            return redirect(url_for('community'))
    return render_template('create_comment.html')

@app.route('/community/<int:forum_id>/delete_forum', methods=('POST',))
def delete_forum(forum_id):
    _forum_db.delete_forum(forum_id)
    return redirect(url_for('community'))

@app.route('/community/<int:comment_id>/delete_comment', methods=('POST',))
def delete_comment(comment_id):
    _forum_db.delete_comment(comment_id)
    return redirect(url_for('community'))

@app.route("/about")
def about():
    if "id" not in session:
        return

    session_id = session.get("id")
    cur.execute(
        "INSERT INTO Button (session_id, button) VALUES (?, ?)", (session_id, 1)
    )
    conn.commit()
    
    return render_template("about.html")

@app.route("/login", methods=('GET','POST'))
def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            if not email or not password:
                if not email:
                    flash('Email is required')
                if not password:
                    flash('Password is required')
            else:
                user = _forum_db.select_user(email)
                if not user:
                    flash('Account does not exist, to register?')
                else:
                    if not password:
                        flash('Password is required')
                    else:
                        salt = user['salt']
                        stored_password_hash = user['password_hash']
                        is_correct_password = password_util.check_password(
                            salt,
                            stored_password_hash,
                            password
                        )
                        if not is_correct_password:
                            flash('Wrong email or password, try again')
                        else:
                            session['login'] = True
                            session['is_admin'] = user['is_admin'] == 1
                            session['email'] = user['email']
                            return redirect(url_for('index'))
    
        return render_template("login.html")
    
@app.route('/signout', methods=('GET',))
def signout():
    session['login'] = False
    session['is_admin'] = False
    session['email'] = NOBODY_EMAIL
    return render_template('index.html')


@app.route('/forgot_password_1', methods=('GET', 'POST'))
def forgot_password_1():
    if request.method == 'POST':
        email = request.form['email']
        user = _forum_db.select_user(email)
        if not user:
            flash("'" + email + "' not found")
            return render_template('forgot_password_1.html')
        token = uuid.uuid4().hex
        session['token'] = token
        try:
            email_util.send(email, token)
        except ConnectionRefusedError:
            abort(404)
        message = 'Please follow email instruction (at ' + email  + ') to get the temporary password.'
        flash(message)
        return redirect(url_for('forgot_password_2', email=email))
    return render_template('forgot_password_1.html')


@app.route('/forgot_password_2', methods=('GET', 'POST'))
def forgot_password_2():
 
        if request.method == 'POST':
            email = request.args.get('email')
            temp_password = request.form['temp_password']
            if temp_password != session['token']:
                message = 'Please follow email instruction (at ' + email  + ') to get the temporary password.'
                flash(message)
                return render_template('forgot_password_2.html', email=email)
            return redirect(url_for('reset_password', email=email))
        return render_template('forgot_password_2.html')


@app.route('/reset_password', methods=('GET', 'POST'))
def reset_password():
    if request.method == 'POST':
        email = request.args.get('email')
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        if password != repeat_password:
            flash("Password and Repeat Password must be same.")
            return render_template('reset_password.html', email=email)
        user = _forum_db.select_user(email)
        salt = user['salt']
        new_password_hash = password_util.hash_password(password, salt)
        _forum_db.update_password(email, new_password_hash)
        return redirect(url_for('login'))
    return render_template('reset_password.html')


@app.route("/register", methods=('GET','POST'))
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        # global _admin_code
        is_admin = 1 if request.form['admin_code'] == _admin_code else 0
        if not email or not password:
            if not email:
                flash('Email is required')
            if not password:
                flash('Password is required')
        else:
            user = _forum_db.select_user(email)
            if user:
                flash('Account exists.  Login in?')
            else:
                salt, password_hash = password_util.hash_new_password(password)
                _forum_db.create_user(first_name, last_name, email, salt, password_hash, is_admin)
                return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.before_request
def assign_id():
    if "id" not in session:
        session["id"] = randint(1_000_000, 9_999_999)


def log_data():
    if not all([key in session for key in ("id", "start_time", "previous_path")]):
        return

    session_id = session.get("id")
    start_time = session.get("start_time")
    previous_path = session.get("previous_path")

    
    time_spent = (datetime.now(timezone.utc) - start_time).total_seconds()
    
    cur.execute(
        "INSERT INTO PageView (session_id, page, time_spent, start_time) VALUES (?, ?, ?, ?)",
        (session_id, previous_path, time_spent, start_time),
    )
    conn.commit()


@app.after_request
def track_time(response):

    if request.path == "/":
        log_data()
        # Update start_time and previous_path
        session["start_time"] = datetime.now(timezone.utc)
        session["previous_path"] = "HomePage"


    if request.path == "/facts":
        log_data()
        # Update start_time and previous_path
        session["start_time"] = datetime.now(timezone.utc)
        session["previous_path"] = "Facts"

    if request.path == "/solutions":
        log_data()
        # Update start_time and previous_path
        session["start_time"] = datetime.now(timezone.utc)
        session["previous_path"] = "Solutions"
        
    if request.path == "/community":
        log_data()
        # Update start_time and previous_path
        session["start_time"] = datetime.now()
        session["previous_path"] = "Community"

    return response

if __name__ == '__main__':
    app.run(debug=True, port=5006)