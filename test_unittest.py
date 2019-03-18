from app import app        # The code to test
import unittest   # The test framework
from app import deleteUser

class Test_TestIncrementDecrement(unittest.TestCase):
    #*****************************
    #        Setup
    #*****************************
    def setUp(self):
        self.app = app.test_client()
        app.secret_key='secret123'
    

    #*****************************
    #        Unit Tests
    #*****************************
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    def test_login_logout(self):
        rv = self.login("lmao", "lmao")
        assert b'You are now logged in' in rv.data 
        rv = self.logout()
        assert b'You are now logged out' or 'Unauthorized, Please login' in rv.data        

    def test_valid_user_registration(self):
        delete = self.app.get('/deleteuser', content_type="html/text")
        rv = self.register("hiepLy", 'lmao', 'lmao')
        assert b'You are now registered and can log in' in rv.data
        
    def test_username_in_use_registration(self):
        rv = self.register("lmao", 'lmao', 'lmao')
        assert b'Username is already in use' in rv.data
    
    def test_update_user_information(self):
        rv = self.update_user_info("Wescules Andraddy", "124 Streeet St.", "", "Sugar Land", "908243", "TX")
        rv = self.app.get('/profile', content_type="html/text")
        assert b'Wescules Andraddy' in rv.data
        assert b'124 Streeet St.' in rv.data
        assert b'Sugar Land' in rv.data
        assert b'908243' in rv.data
        assert b'TX' in rv.data
        assert b'User Updated' in rv.data

    def test_fail_update_user_information(self):
        rv = self.update_user_info("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqddddddddddddddddd", "124 Streeet St.", "", "Sugar Land", "908243", "TX")
        assert b'Full Name needs to be between 1 and 50 characters' in rv.data
        rv = self.update_user_info("Wescules Andraddy", "124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.", "", "Sugar Land", "908243", "TX")
        assert b'Address 1 needs to be between 1 and 100 characters' in rv.data
        rv = self.update_user_info("Wescules Andraddy", "124 Streeet St.", "", "124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.124 Streeet St.", "908243", "TX")
        assert b'City needs to be between 1 and 100 characters' in rv.data
        rv = self.update_user_info("Wescules Andraddy", "124 Streeet St.", "", "Sugar Land", "902342348243", "TX")
        assert b'Zip Code needs to be between 5 and 9 characters' in rv.data

    def test_check_numeric_gallons_requested(self):
        rv = self.fuel_quote_form_inputs("lmao", "03/09/2019")
        assert b'Gallons Requested needs to be a numeric value' in rv.data

    def test_fuel_quote_form(self):
        rv = self.fuel_quote_form_inputs("1236", "03/09/2019")
        assert b'1236' in rv.data
        assert b'03/09/2019' in rv.data
        delete = self.app.get('/deletehistory', content_type="html/text")

    def test_fuel_history(self):
        self.login("lmao", "lmao")
        rv = self.app.get('/history', content_type="html/text")
        assert b'Your Fuel Quote History:' in rv.data



    #*****************************
    #        Helper Functions
    #*****************************
    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username,password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    
    def register(self, username, password, confirm):
        self.logout()
        return self.app.post('/register', data=dict(username=username, password=password, confirm=confirm), follow_redirects=True)

    def update_user_info(self, fname, add1, add2, city, zipp, state):
        self.login("lmao", "lmao")
        return self.app.post('/profile', data=dict(fullname=fname, address1=add1, address2=add2, city=city, zipcode=zipp, state=state))

    def fuel_quote_form_inputs(self, gallonsrequested, dt):
        self.login("lmao", "lmao")
        return self.app.post('/quotes', data=dict(gallons_requested=gallonsrequested, dt=dt))

    

if __name__ == '__main__':
    unittest.main()