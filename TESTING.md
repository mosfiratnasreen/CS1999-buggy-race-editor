# Testing Total Cost for App.py

Since I come across errors when trying to implement automatic testing using unittest to ensure that the total cost calculated after submitting the form, here is the manual testing instructions to be implemented using the webserver:

## Test 1: Basic Total Cost

### This is to test that total cost is calculated accurately with general information

#### Instructions:

1. Open up http://0.0.0.0:5000
2. Click on 'Make Buggy'
3. Enter these values in order in each respective form:
   1. Number of wheels: 4
   2. Type of Tyres: knobbly
   3. Number of Tyres: 4
   4. Colour of Flag: red
   5. Secondary Colour of Flag: white
   6. Flag Pattern: hstripe
   7. Power Type: petrol
   8. Power Units: 4
   9. Backup Power Type: electric
   10. Backup Power Units: 4
   11. Number of Hamster Boosters: 0
   12. Armour Type: wood
   13. Attack Method: charge
   14. Number of Attacks: 3
   15. Race Algorithm : random
4. Click 'Submit'
5. The 'Cost of Buggy' should be 280. If this is correct, it indicates that this form can calculate the total cost for basic data and the results should be reproducible.

## Test Suite: Specific Circumstances

## Test 2: 10% Tyre Cost

### According to the specification, for every tyre greater than 4, there is an additional cost of 10% per tyre of its tyre type i.e. 6 maglev tyres should create a total tyrecost of 210 since 4 maglev tyres has a cost of 200 but an extra 2 tyres with a cost of 5 each = 210

#### Instructions:

1. Open up http://0.0.0.0:5000
2. Click on 'Make Buggy'
3. Enter these values in order in each respective form:
   1. Number of wheels: 4
   2. Type of Tyres: knobbly
   3. Number of Tyres: 6
   4. Colour of Flag: red
   5. Secondary Colour of Flag: white
   6. Flag Pattern: hstripe
   7. Power Type: petrol
   8. Power Units: 4
   9. Backup Power Type: electric
   10. Backup Power Units: 4
   11. Number of Hamster Boosters: 0
   12. Armour Type: wood
   13. Attack Method: charge
   14. Number of Attacks: 3
   15. Race Algorithm : random
4. Click 'Submit'
5. The 'Cost of Buggy' should be 283. If this is correct, it indicates that this form can calculate the total cost for specific data and the results should be reproducible as the tyrecost adds up to 63 each time for 6 knobbly tyres.

## Test 3: Hamster Booster

### According to the specification, for every hamster booster,  there is a cost of 5. This test tests that the total cost if being calculated accurately with a certain number of hamster boosters.

#### Instructions:

1. Open up http://0.0.0.0:5000
2. Click on 'Make Buggy'
3. Enter these values in order in each respective form:
   1. Number of wheels: 4
   2. Type of Tyres: knobbly
   3. Number of Tyres: 6
   4. Colour of Flag: red
   5. Secondary Colour of Flag: white
   6. Flag Pattern: hstripe
   7. Power Type: petrol
   8. Power Units: 4
   9. Backup Power Type: hamster
   10. Backup Power Units: 4
   11. Number of Hamster Boosters: 2
   12. Armour Type: wood
   13. Attack Method: charge
   14. Number of Attacks: 3
   15. Race Algorithm : random
4. Click 'Submit'
5. The 'Cost of Buggy' should be 225. If this is correct, it indicates that this form can calculate the total cost for specific data and the results should be reproducible as the hamster adds up to 10 each time for 2 hamster boosters with an aux_power_cost of 12 as there are 4 units of hamster back up power.





