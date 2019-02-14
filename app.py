from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_wtf import Form, FlaskForm
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
import datetime

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

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            flash('Username is already in use', 'danger')
            return redirect(url_for('register'))
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
                return redirect(url_for('about'))
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
    gallons_requested = IntegerField('Gallons Requested: ', [validators.NumberRange(min=1, max=10000), validators.Required()])
    dt = DateField('Delivery Date',[validators.Required()], format="%m/%d/%Y")

# Fuel quotes
@app.route('/quotes', methods=['GET', 'POST'])
@is_logged_in
def quotes():
    form = FuelForm(request.form)

    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM users WHERE id = %s" % str(session['userid1']))

    article = cur.fetchone()
    cur.close()
    suggestedprice = 0
    due = 0
    if request.method == 'POST':
        gallonsrequested = request.form['gallons_requested']
        dt = request.form['dt']
        date = datetime.datetime.strptime(dt, '%m/%d/%Y').strftime('%Y/%m/%d')
        suggestedprice = 5
        due = suggestedprice * int(gallonsrequested)
        # Create Cursor
        cur = mysql.connection.cursor()

        cur.execute ("insert into fuelquote(userid, gallonsrequested, suggestedprice, amountdue, date) values(%s, %s, %s, %s, %s);",(str(session['userid1']), gallonsrequested, suggestedprice, due, date))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        return render_template('fuelquoteform.html', form=form, article=article, suggestedprice=suggestedprice, due=due) 


    return render_template('fuelquoteform.html', form=form, article=article, suggestedprice=suggestedprice, due=due) 


# Article Form Class
class ArticleForm(Form):
    fullname = StringField('Full Name', [validators.Required()])
    address1 = StringField('Address 1', [validators.Required()])
    address2 = StringField('Address 2', [validators.Length(min=0, max=100)])
    city = StringField('City', [validators.Required()])
    zipcode = StringField('Zip Code', [validators.Required()])



def LengthError(string, minimum, maximum):
    return len(string) < minimum or len(string) > maximum

# Edit Article
@app.route('/profile', methods=['GET', 'POST'])
@is_logged_in
def profileManager():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM users WHERE id = %s" % str(session['userid1']))

    article = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.fullname.data = article['fullname']
    form.address1.data = article['address1']
    form.address2.data = article['address2']
    form.city.data = article['city']
    form.zipcode.data = article['zipcode']
    #state = article['state']
    # Validate profile form and update 
    if request.method == 'POST':
        fname = request.form['fullname']
        if LengthError(fname, 1, 50):
            flash('Full Name needs to be between 1 and 50 characters', 'danger')
            return render_template('profilemanager.html', form=form)
        add1 = request.form['address1']
        if LengthError(add1, 1, 100):
            flash('Address 1 needs to be between 1 and 100 characters', 'danger')
            return render_template('profilemanager.html', form=form)
        add2 = request.form['address2']
        cty = request.form['city']
        if LengthError(cty, 1, 100):
            flash('City needs to be between 1 and 100 characters', 'danger')
            return render_template('profilemanager.html', form=form)
        st = request.form.get('state')
        zp = request.form['zipcode']
        if LengthError(zp, 5, 9):
            flash('Zip Code needs to be between 5 and 9 characters', 'danger')
            return render_template('profilemanager.html', form=form, article=article)

        # Create Cursor
        cur = mysql.connection.cursor()

        cur.execute ("UPDATE users SET fullname=%s, address1=%s, address2=%s, city=%s, state=%s, zipcode=%s WHERE id=%s",(fname, add1, add2,cty, st,zp,  str(session['userid1'])))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('User Updated', 'success')

        return redirect(url_for('profileManager'))


    return render_template('profilemanager.html', form=form, article=article)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)