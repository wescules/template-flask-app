from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

#Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')

# Articles
@app.route('/articles')
def articles():
    # Create cursors
    cur = mysql.connection.cursor()

    # Get articles
    if(session['privilege'] == 1):
        result = cur.execute("select * from articles")
        
        articles = cur.fetchall()

        if result > 0:
            return render_template('articles.html', articles=articles)
        else:
            msg = 'No Articles Found'
            return render_template('articles    .html', msg=msg)

    else:
        result = cur.execute("select id, title, articleid, priv from admin_articles left join articles on (id=articleid and userid=%s) or priv=0 group by id;", str(session['userid1']))

        articles = cur.fetchall()

        if result > 0:
            return render_template('articles.html', articles=articles)
        else:
            msg = 'No Articles Found'
            return render_template('articles.html', msg=msg)

    # Close connection
    cur.close()

#Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('article.html', article=article)


# Register Form Class
class RegisterForm(Form):
    ratehistory = StringField('Rate History', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    location = StringField('Location', [validators.Length(min=1, max=100)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['userid1'] = data['id']

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



class FuelForm(Form):
    competitors_rate = TextAreaField('Competitors Rate', [validators.Length(min=1, max=50)])
    gallons_requested = TextAreaField('Gallons Requested', [validators.Length(min=1, max=50)])
    company_profit = TextAreaField('Company Profit', [validators.Length(min=1, max=50)])
    seasonal_fluc = TextAreaField('Seasonal Fluctuation', [validators.Length(min=1, max=50)])
    predicted_rate = TextAreaField('Predicted Rate', [validators.Length(min=1, max=50)])

# Fuel quotes
@app.route('/quotes', methods=['GET', 'POST'])
@is_logged_in
def quotes():
    form = FuelForm(request.form)
    if request.method == 'POST' and form.validate():

    return render_template('add_article.html', form=form) 







 form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO articles(title, body, author, priv) VALUES(%s, %s, %s, %s)",(title, body, session['username'], 0))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)










# Article Form Class
class ArticleForm(Form):
    oldpassword = TextAreaField('Old Password', [validators.Length(min=1, max=200)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    location = TextAreaField('Location')
    ratehistory = TextAreaField('Rate History')


# Edit Article
@app.route('/profile', methods=['GET', 'POST'])
@is_logged_in
def edit_profile():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM users WHERE id = %s" % str(session['userid1']))

    article = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    actual_password = article['password']
    form.location.data = article['location']
    form.ratehistory.data = article['ratehistory']

    if request.method == 'POST' and form.validate():
        password_candidate = request.form['oldpassword']
        newpass = request.form['password']
        location = request.form['location']
        ratehistory = request.form['ratehistory']
        # Create Cursor
        cur = mysql.connection.cursor()

        if(len(password_candidate) <= 0):
            cur.execute ("UPDATE users SET location=%s, ratehistory=%s WHERE id=%s",(location, ratehistory, str(session['userid1'])))

        if sha256_crypt.verify(password_candidate, actual_password):
            # Execute
            newpass = sha256_crypt.encrypt(str(newpass))
            cur.execute ("UPDATE users SET password=%s, location=%s, ratehistory=%s WHERE id=%s",(newpass, location, ratehistory, str(session['userid1'])))
        else:
            flash('Old password is incorrect', 'danger')
            return render_template('edit_article.html', form=form)

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('User Updated', 'success')

        return render_template('edit_article.html', form=form)

    return render_template('edit_article.html', form=form)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
    
#sudo apt-get install mysql-server
#apt-get install python-dev
#sudo apt-get install libmysqlclient-dev
#pip install flask_mysqldb
#pip install wtforms
#pip install passlib

###################
#***create database***(set password to 'root')
# mysql -u root -p
# create database myflaskapp;
# mysql -u root -proot myflaskapp < admin_backup.sql
