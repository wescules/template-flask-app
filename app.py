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
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
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
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        privelege = request.form.get('priv')
        
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password, privilege) VALUES(%s, %s, %s, %s, %s)", (name, email, username, password, int(privelege)))

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
                session['privilege'] = data['privilege']
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



# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursors
    cur = mysql.connection.cursor()

    # Get articles
    if(session['privilege'] == 1):
        result = cur.execute("select * from articles")
        
        articles = cur.fetchall()

        if result > 0:
            return render_template('dashboard.html', articles=articles)
        else:
            msg = 'No Articles Found'
            return render_template('dashboard.html', msg=msg)

    else:
        result = cur.execute("select * from admin_articles left join articles on (id=articleid and userid=%s) or priv=0 group by id;", str(session['userid1']))
        
        articles = cur.fetchall()

        if result > 0:
            return render_template('dashboard.html', articles=articles)
        else:
            msg = 'No Articles Found'
            return render_template('dashboard.html', msg=msg)

    # Close connection
    cur.close()


# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
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


# Add Admin Article
@app.route('/add_admin_article', methods=['GET', 'POST'])
@is_logged_in
def add_admin_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO articles(title, body, author, priv) VALUES(%s, %s, %s, %s)",(title, body, session['username'], 1))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_admin_article.html', form=form)


# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))

# Share Article
@app.route('/share_article/<string:id>', methods=['POST'])
@is_logged_in
def share_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    usersEmail = request.form['userEmail']
    # Execute
    result = cur.execute("SELECT * FROM admin_articles, users where email = '%s' and admin_articles.userid = users.id" % usersEmail)

    if(result >= 1):
        cur.execute("delete from admin_articles where userid in (select id from users where email = '%s')" % usersEmail)
        flash('Article is Unshared', 'success')
    else:
        cur.execute("INSERT INTO admin_articles(articleid, userid) SELECT %s, id FROM users where email = '%s'" % (id, usersEmail))
        flash('Article is Shared', 'success')
    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    return redirect(url_for('dashboard'))

# Unshare Article
@app.route('/share_article/<string:id>', methods=['POST'])
@is_logged_in
def unshare_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    usersEmail = request.form['userEmail']
    # Execute
    cur.execute("delete from admin_articles where userid in (select id from users where email = %s)", usersEmail)


    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Article is shared', 'success')

    return redirect(url_for('dashboard'))


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