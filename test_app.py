import unittest
import app



##This was my attempt of unit testing the code without using app.py
#class TestTotalCost(unittest.TestCase):

    #def test_cost(self):#total cost for 4 knobbly tyres,
        #3 units of wind, no backup power, wood armour and 2 units of biohazard
        #self.assertEqual(sum([(4*15),(3*20),(0*0),(1*40),(2*30)]), 220, "Should be 220")

##Unit testing with app.py
class TestApp(unittest.TestCase):

    def test_total_cost(self):
        tyrecost = 200
        powercost = 20
        auxpowercost = 16
        armourcost = 100
        attackcost = 112
        self.assertEqual(app.total_cost(tyrecost,powercost,auxpowercost,hamstercost,armourcost,attackcost), 448)
##        parent_dict = {'petrol': 4, 'fusion': 400, 'steam': 3, 'bio': 5, 'electric': 20, 'rocket': 16, 'hamster': 3,
##                       'thermo': 300, 'solar': 40, 'wind': 20}
##        option = 'petrol'
##        qty = 5
##        self.assertEqual(app.get_cost(parent_dict, option, qty), 20)
        
if __name__ == '__main__':
    unittest.main()
