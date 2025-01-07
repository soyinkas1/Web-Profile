import unittest
from main_app import create_app as create_main_app, db as main_db, mail as main_mail
from main_app.db_models import ContactTable 

class MainAppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_main_app('testing')
        self.client = self.app.test_client(use_cookies=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        main_db.create_all()
    
    def tearDown(self):
        main_db.session.remove()
        main_db.drop_all()
        self.app_context.pop()
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"about", response.data)
    
    def test_portfolio_page(self):
        response = self.client.get('/portfolio')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Portfolio", response.data)
    
    def test_contact_table(self):
        new_contact = ContactTable(name='John Doe', email='john@example.com')
        main_db.session.add(new_contact)
        main_db.session.commit()
        contacts = ContactTable.query.all()
        self.assertEqual(len(contacts), 1)

if __name__ == '__main__':
    unittest.main()
