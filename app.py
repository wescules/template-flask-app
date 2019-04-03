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
        privelege = request.form.get('priv') 
        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            flash('Username is already in use', 'danger')
            return redirect(url_for('register'))
        # Execute query
        cur.execute("INSERT INTO users(username, password, type) VALUES(%s, %s, %s)", (username, password, privelege))

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
                session['type'] = data['type']

                flash('You are now logged in', 'success')
                return redirect(url_for('about')) if data['type'] == 0 else redirect(url_for('companydashboard'))
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


# Quote History
@app.route('/history', methods=['GET'])
@is_logged_in
def dashboard():
    # Create cursors
    cur = mysql.connection.cursor()

    # Get quotes
    result = cur.execute("select * from fuelquote where userid = %s" % str(session['userid1']))
    
    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)

    # Close connection
    cur.close()

class ChangePriceForm(Form):
    pricechange = IntegerField('Change Price: ', [validators.NumberRange(min=1, max=10000)])

# About
@app.route('/companydashboard', methods=['GET', 'POST'])
def companydashboard():
    form = ChangePriceForm(request.form)

    # Create cursors
    cur = mysql.connection.cursor()
    result = cur.execute("select * from currentPrice;")
    article = cur.fetchone()
    form.pricechange.data = article['price']
    # Get quotes
    result = cur.execute(" select users.fullname,fuelquote.gallonsrequested, fuelquote.amountdue, fuelquote.date from users right join fuelquote on users.id=fuelquote.userid where fullname is not null;")
    
    articles = cur.fetchall()
    if request.method == 'POST':
        price = request.form['pricechange']
        result = cur.execute("update currentPrice set price=%s where id=1" %  (price))
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash("Price Updated", "success")
        return render_template('companydashboard.html', form=form, articles=articles)
        
    return render_template('companydashboard.html', form=form, articles=articles)


@app.route('/deleteuser', methods=['GET'])
def deleteUser():
    cur = mysql.connection.cursor()
    cur.execute("delete from users where username='hiepLy'")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('register'))

@app.route('/deletehistory', methods=['GET'])
def deleteHistory():
    cur = mysql.connection.cursor()
    cur.execute("delete from fuelquote where gallonsrequested=1236")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('quotes'))

class FuelForm(Form):
    gallons_requested = IntegerField('Gallons Requested: ', [validators.NumberRange(min=1, max=10000), validators.Required()])
    dt = DateField('Delivery Date',[validators.Required()], format="%m/%d/%Y")

# Fuel quotes
@app.route('/quotes', methods=['GET', 'POST', 'PUT'])
@is_logged_in
def quotes():
    form = FuelForm(request.form)

    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM users WHERE id = %s" % str(session['userid1']))

    article = cur.fetchone()
    cur.close()
    PricePerGallon=0
    Transportation=0
    clientratehistory=0
    SeasonFluctuation=0
    profitMargin=0
    FuelPrice=0
    gallonsrequested=0
    ppgalon =0
    GallonsRequestedFactor=0
    SuggestedPrice=0

    if request.method == 'POST':
        gallonsrequested = request.form['gallons_requested']
        if not gallonsrequested.isdigit():
            flash('Gallons Requested needs to be a numeric value', 'danger')
            return render_template('fuelquoteform.html',SuggestedPrice=SuggestedPrice, form=form,Transportation=Transportation, article=article, PricePerGallon=PricePerGallon, FuelPrice=FuelPrice, profitMargin=profitMargin, SeasonFluctuation=SeasonFluctuation, clientratehistory=clientratehistory, gallonsrequested=gallonsrequested, ppgalon=ppgalon, GallonsRequestedFactor=GallonsRequestedFactor) 

        dt = request.form['dt']
        date = datetime.datetime.strptime(dt, '%m/%d/%Y').strftime('%Y/%m/%d')
        FuelPrice, PricePerGallon, Transportation, clientratehistory, SeasonFluctuation, profitMargin, GallonsRequestedFactor,SuggestedPrice = pricingModule(gallonsrequested, dt)
        ppgalon = float(gallonsrequested) * float(PricePerGallon)
        if request.form['action'] == 'SubmitQuote':
            # Create Cursor
            cur = mysql.connection.cursor()

            cur.execute ("insert into fuelquote(userid, gallonsrequested, suggestedprice, amountdue, date) values(%s, %s, %s, %s, %s);",(str(session['userid1']), gallonsrequested, SuggestedPrice, FuelPrice, date))
            # Commit to DB
            mysql.connection.commit()
            flash ("Quote Saved", 'success')
            #Close connection
            cur.close()

        return render_template('fuelquoteform.html',SuggestedPrice=SuggestedPrice, form=form,Transportation=Transportation, article=article, PricePerGallon=PricePerGallon, FuelPrice=FuelPrice, profitMargin=profitMargin, SeasonFluctuation=SeasonFluctuation, clientratehistory=clientratehistory, gallonsrequested=gallonsrequested, ppgalon=ppgalon, GallonsRequestedFactor=GallonsRequestedFactor) 

    return render_template('fuelquoteform.html',SuggestedPrice=SuggestedPrice, form=form,Transportation=Transportation, article=article, PricePerGallon=PricePerGallon, FuelPrice=FuelPrice, profitMargin=profitMargin, SeasonFluctuation=SeasonFluctuation, clientratehistory=clientratehistory, gallonsrequested=gallonsrequested, ppgalon=ppgalon, GallonsRequestedFactor=GallonsRequestedFactor) 


def pricingModule(gallonsrequested, date):
    FuelPrice = 0
    Transportation = 0.0
    clientratehistory = 0
    SeasonFluctuation = 0
    PricePerGallon = 0

    # Create cursor
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM users where id=%s" % str(session['userid1']))
    article = cur.fetchone()
    Transportation = 0.02 if article['state'] == 'TX' else 0.04


    result = cur.execute("SELECT * FROM currentPrice;")

    article = cur.fetchone()
    PricePerGallon = article['price']

    month = date[0:2:]
    SeasonFluctuation = 0.03 if month == '09' or month == '10' or month == '11' or month == '12' or month == '01' or month == '02' else 0.04
    
    # Get article by id
    result = cur.execute("SELECT * FROM fuelquote WHERE userid = %s" % str(session['userid1']))
    
    clientratehistory = 0.01 if result >= 1 else 0.0

    cur.close()
    
    profitMargin = 0.10

    GallonsRequestedFactor = 0.02 if gallonsrequested > 1000 else 0.03

    SuggestedPrice = PricePerGallon + (Transportation - clientratehistory + GallonsRequestedFactor + profitMargin + SeasonFluctuation) * PricePerGallon

    FuelPrice = float(gallonsrequested) * float(SuggestedPrice)
    
    return FuelPrice, PricePerGallon, Transportation, clientratehistory, SeasonFluctuation, profitMargin, GallonsRequestedFactor, SuggestedPrice




# Article Form Class
class ProfileManager(Form):
    fullname = StringField('Full Name', [validators.Required(), validators.Length(min=1, max=50)])
    address1 = StringField('Address 1', [validators.Required(), validators.Length(min=1, max=100)])
    address2 = StringField('Address 2', [validators.Length(min=0, max=100)])
    city = StringField('City', [validators.Required(), validators.Length(min=1, max=100)])
    zipcode = StringField('Zip Code', [validators.Required(), validators.Length(min=5, max=9)])



def LengthError(string, minimum, maximum):
    return len(string) < minimum or len(string) > maximum

# Edit Profile
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
    form = ProfileManager(request.form)

    # Populate article form fields
    form.fullname.data = article['fullname']
    form.address1.data = article['address1']
    form.address2.data = article['address2']
    form.city.data = article['city']
    form.zipcode.data = article['zipcode']
    session['state1'] = article['state']
    # Validate profile form and update 
    if request.method == 'POST':
        fname = request.form['fullname']
        if LengthError(fname, 1, 50):
            flash('Full Name needs to be between 1 and 50 characters', 'danger')
            return render_template('profilemanager.html', form=form, article=article)
        add1 = request.form['address1']
        if LengthError(add1, 1, 100):
            flash('Address 1 needs to be between 1 and 100 characters', 'danger')
            return render_template('profilemanager.html', form=form, article=article)
        add2 = request.form['address2']
        cty = request.form['city']
        if LengthError(cty, 1, 100):
            flash('City needs to be between 1 and 100 characters', 'danger')
            return render_template('profilemanager.html', form=form, article=article)
        st = request.form.get('state')
        session['state1'] = st
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