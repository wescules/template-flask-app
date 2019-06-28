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


# Register Form Class
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
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
        cur.execute("INSERT INTO users(name, email, username, password, privilege) VALUES(%s, %s, %s, %s, %s)", ("user", "email", username, password, 1))

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
    result = cur.execute("select * from records")
    
    articles = cur.fetchall()

    result = cur.execute("SELECT category,COUNT(*) as count FROM records GROUP BY category ORDER BY count DESC")
    
    graphs = cur.fetchall()

    colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    if result > 0:
        return render_template('dashboard.html', articles=articles, max = 800, graphs = graphs, colors = colors)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)


    # Close connection
    cur.close()

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=os.getcwd()+"/files", filename="filename.png")


# Statistics
@app.route('/statistics')
@is_logged_in
def statistics():
    # Create cursors
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT category,COUNT(*) as count FROM records GROUP BY category ORDER BY count DESC")
    
    articles = cur.fetchall()

    if result > 0:
        return render_template('statistics.html', articles=articles, max=2000)


    else:
        msg = 'No Articles Found'
        return render_template('statistics.html', msg=msg)


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
@app.route('/view_reciept/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def view_reciept(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM items WHERE recieptID = %s", [id])

    articles = cur.fetchall()

    result = cur.execute("select sum(price) as sumprice from items where recieptID= %s", [id])
    total = cur.fetchone()

    cur.close()
    # Get form
    form = ArticleForm(request.form)

    return render_template('view_reciept.html', articles=articles, total=total)

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
