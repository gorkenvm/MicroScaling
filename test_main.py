import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from main import app



class AppTestCase(unittest.TestCase):

    username = 'VMG UNIT TEST TELEBOT'
    district = 'KONAK'
    neighborhood = 'ALSANCAK'
    StartDate = '01.01.2022'        # ("%d.%m.%Y")
    EndDate = '01.01.2023'
    MainTopic = 'SU / KANALİZASYON'
    SubTopic = 'BRANŞMAN (BİNA KOLU) ARIZALARI'
    Organisation = 'İZBB'
    Messages = 'UNIT TEST PROCESSİNG'
    Persons = {
            "ULAŞIM YATIRIMLARI-VEYSEL MURAT GÖRKEN": "telno",
            "KALİTE VE KURUMSAL GELİŞİM-AHMET KIPKIP": "telno",
            
        }
    
    def setUp(self):
        self.app = app.test_client()

    def test_GetMainTopics(self):
        json = {"district": self.district, "neighborhood" : self.neighborhood}
        response = self.app.post('/Him/MainTopics', json=json)
    
        expected_response = [
            os.environ("expected_response")
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_response)
        print(response.json)



if __name__ == '__main__':
    unittest.main()


