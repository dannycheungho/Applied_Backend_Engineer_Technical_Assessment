import unittest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app,db
from src.models.models import Doctor, District, DistrictTranslation, Category, db

class DoctorTestCase(unittest.TestCase):

    def init(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_doctor(self):
        with app.app_context():
            doctor1 = Doctor(name='Danny Cheung', email='danny@example.com', phone='55551234')
            district1 = District(district_name='Hong_Kong_Island', address='Robert Robertson, 1234 NW Bobcat Lane, St. Robert, MO ', clinic_phone='98765432', price=500,
                                price_remark="english remark",working_time='9am-5pm')
            district2 = District(district_name='Hong_Kong_Island', address='456 Oak St', clinic_phone='67889998', price=600,
                                price_remark="inclusive 3 Days of Western medicine", working_time='10am-6pm')
            district_2_translation = DistrictTranslation(language_id=1, district_name='Hong_Kong_Island', address='元朗廣恩村5樓05室',
                                                        price_remark="中文備注", district=district2)
            doctor1.districts.extend([district1, district2])
            category1 = Category(category_name='General_Practitioner')
            category2 = Category(category_name='Epidemiologist')
            doctor1.categories.extend([category1, category2])
            db.session.add_all([
                doctor1, district1, district2, district_2_translation, 
                category1, category2
            ])
            db.session.commit()

        response = self.app.get('/doctor/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Danny Cheung')
        self.assertEqual(data['email'], 'danny@example.com')

    def test_create_doctor(self):
        payload = json.dumps({
        "name": "Danny ho",
        "email": "dannycheun1g@example.com",
        "phone": 39874443,
        "districts": [
            {
            "district_name": "Hong_Kong_Island",
            "address": "address english",
            "clinic_phone": 56661234,
            "price": 666,
            "price_remark": "per session",
            "working_time": "9am-5pm",
            "district_translations": [
                {
                "language_id": 1,
                "district_name": "Hong_Kong_Island",
                "address": "地址",
                "price_remark": "per session"
                }
            ]
            },
            {
            "district_name": "Kowloon",
            "address": "Kowloon address english",
            "clinic_phone": 76661234,
            "price": 100,
            "price_remark": "per session",
            "working_time": "9am-5pm",
            "district_translations": [
                {
                "language_id": 1,
                "district_name": "Kowloon",
                "address": "地址九龍",
                "price_remark": "Kowloon備註 session"
                }
            ]
            }
        ],
        "categories": [
            {
            "category_name": "Epidemiologist",
            "category_translations": [
                {
                "language_id": 1,
                "category_name": "Epidemiologist"
                }
            ]
            }
        ],
        "doctor_translations": [
            {
            "language_id": 1,
            "name": "張醫生"
            }
        ]
        })       
        response = self.app.post('/doctor', data=payload, content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Doctor created successfully!')
        
        with app.app_context():
            doctor = Doctor.query.filter_by(name='Danny ho').first()
            self.assertIsNotNone(doctor)
            self.assertIsNotNone(doctor.districts)
            self.assertIsNotNone(doctor.categories)
            self.assertEqual(doctor.districts[0].district_name.name, 'Hong_Kong_Island')
            self.assertEqual(doctor.districts[0].price, 666)
            self.assertEqual(doctor.districts[1].district_name.name, 'Kowloon')
            self.assertEqual(doctor.districts[1].price, 100)
            self.assertEqual(doctor.categories[0].category_name.name, str('Epidemiologist'))

    def test_get_all_doctors(self):
        with app.app_context():
            doctor1 = Doctor(name='Danny Cheung', email='danny@example.com', phone='55551234')
            district1 = District(district_name='Hong_Kong_Island', address='Robert Robertson, 1234 NW Bobcat Lane, St. Robert, MO ', clinic_phone='98765432', price=500,
                                price_remark="english remark",working_time='9am-5pm')
            district2 = District(district_name='Hong_Kong_Island', address='456 Oak St', clinic_phone='67889998', price=600,
                                price_remark="inclusive 3 Days of Western medicine", working_time='10am-6pm')
            district_2_translation = DistrictTranslation(language_id=1, district_name='Hong_Kong_Island', address='元朗廣恩村5樓05室',
                                                        price_remark="中文備注", district=district2)
            doctor1.districts.extend([district1, district2])
            doctor2 = Doctor(name='CK Cheung', email='CK@example.com', phone='65874185')
            doctor2_district = District(district_name='Kowloon', address='19F Tin IU Road', clinic_phone='55551234', price=500,
                                        working_time='11am-5pm')
            doctor2_district_translation = DistrictTranslation(language_id=1, district_name='Kowloon', address='天水圍天恩',
                                                            price_remark="中文2remark", district=doctor2_district)
            doctor2.districts.extend([doctor2_district])

            category1 = Category(category_name='General_Practitioner')
            category2 = Category(category_name='Epidemiologist')
            doctor1.categories.extend([category2])
            doctor2.categories.extend([category1])
            db.session.add_all([
                doctor1, district1, district2, district_2_translation, doctor2,
                doctor2_district, doctor2_district_translation, category1, category2
            ])

            db.session.commit()

        # Test case 1: non filter
        response = self.app.get('/doctor')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertIsNotNone(data)
        self.assertIsNotNone(data[0])
        self.assertIsNotNone(data[1])
        self.assertEqual(data[0]['name'], 'Danny Cheung')
        self.assertEqual(data[0]['phone'], '55551234')
        self.assertEqual(data[0]['districts'][0]['district_name'], 'HONG KONG ISLAND')
        self.assertEqual(data[0]['districts'][0]['price'], 500)
        self.assertEqual(data[0]['districts'][1]['district_name'], 'HONG KONG ISLAND')
        self.assertEqual(data[0]['districts'][1]['price'], 600)
        self.assertEqual(data[0]['categories'][0], 'Epidemiologist')
        self.assertEqual(data[1]['name'], 'CK Cheung')
        self.assertEqual(data[1]['phone'], '65874185')
        self.assertEqual(data[1]['districts'][0]['district_name'], 'KOWLOON')
        self.assertEqual(data[1]['districts'][0]['price'], 500)
        self.assertEqual(data[1]['categories'][0], 'General Practitioner')
        
        # Test case 2: filter by district=Hong_Kong_Island
        response = self.app.get('/doctor?district=Hong_Kong_Island')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertIsNotNone(data)
        self.assertIsNotNone(data[0])
        self.assertEqual(data[0]['name'], 'Danny Cheung')
        self.assertEqual(data[0]['districts'][0]['district_name'], 'HONG KONG ISLAND')
        self.assertEqual(data[0]['districts'][1]['district_name'], 'HONG KONG ISLAND')
  
        # Test case 3: filter by price range 1-1000
        response = self.app.get('/doctor?min_price=1&max_price=1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Danny Cheung')
        self.assertTrue(1 <= data[0]['districts'][0]['price'] <= 1000)
        self.assertTrue(1 <= data[0]['districts'][1]['price'] <= 1000)
        self.assertTrue(1 <= data[1]['districts'][0]['price'] <= 1000)
        
        # Test case 4: filter by category
        response = self.app.get('/doctor?category=Epidemiologist')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['categories'][0], 'Epidemiologist')   
        
        # Test case 5: filter by language
        response = self.app.get('/doctor?language=cht')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['categories'][0], '流行病')     
        self.assertEqual(data[1]['categories'][0], '普通科門診')

        # Test case 6: filter by multiple condition
        response = self.app.get('/doctor?district=Hong_Kong_Island&category=Epidemiologist&min_price=1&max_price=1000&language=cht')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Danny Cheung')
        self.assertEqual(data[0]['phone'], '55551234')
        self.assertEqual(data[0]['districts'][0]['district_name'], '香港島')
        self.assertEqual(data[0]['districts'][1]['district_name'], '香港島')
        self.assertTrue(1 <= data[0]['districts'][0]['price'] <= 1000)
        self.assertTrue(1 <= data[0]['districts'][1]['price'] <= 1000)
        self.assertEqual(data[0]['categories'][0], '流行病')                  
  
if __name__ == '__main__':
    unittest.main()
