from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
from colour import Color
app = Flask(__name__)
import unittest
import app
import sqlite3



##This was my attempt of unit testing the code without using app.py
class TestTotalCost(unittest.TestCase):

    def test_cost(self):#total cost for 4 knobbly tyres,
        #3 units of wind, no backup power, wood armour and 2 units of biohazard
        self.assertEqual(sum([(4*15),(3*20),(0*0),(1*40),(2*30)]), 220, "Should be 220")

##Unit testing with app.py
class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('')
    @classmethod
    def tearDownClass(cls):
        print()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_cost(self):
        parent_dict = {'petrol': 4, 'fusion': 400, 'steam': 3, 'bio': 5, 'electric': 20, 'rocket': 16, 'hamster': 3,
                       'thermo': 300, 'solar': 40, 'wind': 20}
        option = 'petrol'
        qty = 5
        self.assertEqual(app.get_cost(parent_dict, option, qty), 20)

    def test_get_armour_cost(self):
        parent_dict = {'wood': 40, 'aluminium': 200, 'thinsteel': 100, 'thicksteel': 200, 'titanium': 290}
        option = 'thinsteel'
        qty = 4
        self.assertEqual(app.get_armour_cost(parent_dict, option, qty), 400)

    def test_create_buggy(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
