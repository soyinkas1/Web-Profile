from email import message
import unittest
from main_app import create_app as create_main_app, db as main_db, mail as main_mail
from main_app.db_models import ContactTable 
from demo_app1.app import create_app as create_demo1_app, db as demo1_db, mail as demo1_mail
from demo_app1.app.db_models import HeartPredictions as Demo1Table
from demo_app1.app.main import demo1_app
from datetime import datetime

class MainAppTestCase(unittest.TestCase):
    
    def setUp(self):
        # Create the main app and demo app
        self.app = create_main_app('testing')
        self.demo_app = create_demo1_app('testing')

         # Register the demo app blueprint in the main app
        self.app.register_blueprint(demo1_app, url_prefix='/demo1')

        # Create the Test client
        self.client = self.app.test_client(use_cookies=True)

        # Push the main app context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create tables for main app
        with self.app.app_context():
            main_db.create_all()

        # Push the demo app context
        self.demo_app_context = self.demo_app.app_context()
        self.demo_app_context.push()

        # Create tables for the demo app database
        with self.demo_app_context:
            demo1_db.create_all()

       
    
    def tearDown(self):
        # Remove and drop tables for both databases
       
    
        with self.demo_app.app_context():
            demo1_db.session.remove()
            demo1_db.drop_all()
        self.demo_app_context.pop()
        
        with self.app.app_context():
                    main_db.session.remove()
                    main_db.drop_all()
               
         # Pop the app context    
        
        self.app_context.pop()
    
    def test_main_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"about", response.data)
    
    def test_portfolio_page(self):
        response = self.client.get('/portfolio')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Portfolio", response.data)
    
    def test_contact_table(self):
        with self.app.app_context():
            new_contact = ContactTable(name='John Doe', email='john@example.com', message="This is a test of the app", date=datetime.now())
            main_db.session.add(new_contact)
            main_db.session.commit()
            contacts = ContactTable.query.all()
            self.assertEqual(len(contacts), 1)
    
    def test_hd_predict_table(self):
        new_preds = Demo1Table(email = "soyinka.sowoolu@gmail.com", 
    age = 30, 
    sex = 1, 
    cp = 34, 
    trestbps = 567, 
    chol = 34, 
    fbs = 24, 
    restecg = 301, 
    thalach = 12, 
    exang = 23, 
    oldpeak = 10.3, 
    slope = 2, 
    ca = 9, 
    thal = 23,
    target = 0
        )
        
        demo1_db.session.add(new_preds)
        demo1_db.session.commit()
        prediction = Demo1Table.query.all()
        self.assertEqual(len(prediction), 1)



if __name__ == '__main__':
    unittest.main()
