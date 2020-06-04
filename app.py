from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
from colour import Color
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

def check_color(color):
   try:
      Color(color)
      return True
   except ValueError:
      return False


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
   return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
  if request.method == 'GET':
     con = sql.connect(DATABASE_FILE)
     con.row_factory = sql.Row
     cur = con.cursor()
     cur.execute("SELECT * FROM buggies")
     record = cur.fetchone();
     return render_template("buggy-form.html", buggy=record)
  elif request.method == 'POST': 

    msg=[]
    
    qty_wheels = request.form['qty_wheels']
    qty_wheels = qty_wheels.strip()
    if qty_wheels == "":
       msg.append("Please enter a number for quantity of wheels")
    elif not qty_wheels.isdigit():
       msg.append(f"This is not a valid number of wheels: {qty_wheels}")
    elif not int(qty_wheels) >= 4:
       msg.append("Please enter more than 4 wheels")

    tyres = request.form['tyres']
    tyres = tyres.strip()
    tyres = tyres.lower()
    tyretypes = ["knobbly", "slick", "steelband", "reactive", "maglev"]
    if tyres == "":
       msg.append("Please enter any of the following tyre types: knobbly, slick, steelband, reactive or maglev")
    elif not tyres in tyretypes:
       msg.append (f"This is not a valid type of tyre: {tyres}")
       msg.append("Please enter any of the following tyre types: knobbly, slick, steelband, reactive or maglev")
       
    qty_tyres = request.form['qty_tyres']
    qty_tyres = qty_tyres.strip()
    if tyres == "":
       msg.append("Please enter a number for quantity of tyres including spares.")
    elif not qty_tyres.isdigit():
       msg.append(f"This is not a valid number of tyres: {tyres}")
    elif not int(qty_tyres) >= int(qty_wheels):
       msg.append(f"Please enter more than {qty_wheels} tyres")
       
    flag_color = request.form['flag_color']
    flag_color = flag_color.strip()
    flag_color = flag_color.lower()
    if flag_color == "":
       msg.append("Please enter a colour.")
    elif not check_color(flag_color):
       msg.append(f"This is not a valid flag colour: {flag_color}")

    flag_color_secondary = request.form['flag_color_secondary']
    flag_color_secondary = flag_color_secondary.strip()
    flag_color_secondary = flag_color_secondary.lower()
    if flag_color_secondary == "":
       msg.append("Please enter a secondary colour.")
    elif not check_color(flag_color_secondary):
       msg.append(f"This is not a valid flag colour: {flag_color_secondary}")

    flag_pattern = request.form['flag_pattern']
    flag_pattern = flag_pattern.strip()
    flag_pattern = flag_pattern.lower()
    patterns = ["plain","vstripe","hstripe","dstripe","checker","spot"]
    if flag_pattern == "":
       msg.append("Please enter any of the following patterns: plain, vstripe, hstripe, dstripe, checker or spot")
    elif not flag_pattern in patterns:
       msg.append(f"This is not a valid flag pattern: {flag_pattern}")
       msg.append("Please enter any of the following patterns: plain, vstripe, hstripe, dstripe, checker or spot")

    power_type = request.form['power_type']
    power_type = power_type.strip()
    power_type = power_type.lower()
    powertypes = ["petrol","fusion","steam","bio","electric","rocket","hamster","thermo","solar","wind","none"]
    if power_type == "":
       msg.append("Please enter any of the following types of power: petrol, fusion, steam, bio, electric, rocket, hamster, thermo, solar or wind")
    elif not power_type in powertypes:
       msg.append(f"This is not a valid type of power: {power_type}")
       msg.append("Please enter any of the following types of power: petrol, fusion, steam, bio, electric, rocket, hamster, thermo, solar or wind")

    power_units = request.form['power_units']
    power_units = power_units.strip()
    if power_units == "":
       msg.append("Please enter a number for quantity of power units.")
    elif not power_units.isdigit():
       msg.append(f"This is not a valid unit of power: {power_units}")
    elif not int(power_units) >= 1:
       msg.append("Please enter more than 1 unit.")

    nonconsumable = ["fusion","thermo","solar"]
    if power_type in nonconsumable:
       if int(power_units) >1:
          msg.append("Fusion, thermo and solar cannot have power units of greater than 1 as they are non-consumable power.")

    aux_power_type = request.form['aux_power_type']
    aux_power_type = aux_power_type.strip()
    aux_power_type = aux_power_type.lower()
    if not aux_power_type in powertypes:
       msg.append(f"This is not a valid backup type of power: {aux_power_type}")
       msg.append("If you would like a backup type of power, please enter any of the following types of power: petrol, fusion, steam, bio, electric, rocket, hamster, thermo, solar or wind")
    elif aux_power_type == "none":
       pass

    aux_power_units = request.form['aux_power_units']
    aux_power_units = aux_power_units.strip()
    if aux_power_type == "":
       if not aux_power_units.isdigit():
          msg.append("As you have not selected a backup type of power, you cannot put backup power units")
       elif int(aux_power_units) >0:
          msg.append("As you have not selected a backup type of power, you cannot put backup power units")
    elif aux_power_type == "none":
       if int(aux_power_units) >0:
          msg.append("As you have selected no backup type of power, you cannot have more than 0 units of backup power. Please change this back to 0")
    elif not aux_power_units.isdigit():
       msg.append(f"This is not a valid unit of backup power: {aux_power_units}")
    elif int(aux_power_units) >0:
       msg.append("Please enter more than 1 unit of backup power.")

    hamster_booster = request.form['hamster_booster']
    hamster_booster = hamster_booster.strip()
    if not power_type or aux_power_type == "hamster_booster":
       if int(hamster_booster) >0:
          msg.append ("You cannot have hamster boosters without selecting a power type as 'hamster'")
       if not hamster_booster.isdigit():
          msg.append ("You cannot have hamster boosters without selecting a power type as 'hamster'")
    elif not hamster_booster.isdigit():
       msg.append(f"This is not a valid unit of hamster boosters: {hamster_booster}")

    armour = request.form['armour']
    armour = armour.strip()
    armour = armour.lower()
    armourtypes = ["none", "wood", "aluminium", "thinsteel", "thicksteel", "titanium"]
    if armour == "":
       msg.append("Please enter any of the following types of armour: none, wood, aluminium, thinsteel, thicksteel or titanium")
       msg.append("If you would not like armour please type in: none")
    elif not armour in armourtypes:
       msg.append(f"This is not a valid type of armour: {armour}")
       msg.append("Please enter any of the following types of armour: none, wood, aluminium, thinsteel, thicksteel or titanium")
       
    attack = request.form['attack']
    attack = attack.strip()
    attack = attack.lower()
    attacktypes = ["none","spike","flame","charge","biohazard"]
    if attack == "":
       msg.append("Please enter any of the following attack methods: none, spike, flame, charge, biohazard")
       msg.append("If you would not like an attack method please type in: none")
    elif not attack in attacktypes:
       msg.append(f"This is not a valid method of attack: {attack}")
       msg.append("Please enter any of the following attack methods: none, spike, flame, charge, biohazard")
       
    qty_attacks = request.form['qty_attacks']
    qty_attacks = qty_attacks.strip()
    if qty_attacks == "":
       msg.append("Please enter a number for quantity of attacks.")
    elif not qty_attacks.isdigit():
       msg.append(f"This is not a valid number of attacks: {qty_attacks}")
    elif attack == "none":
       if qty_attacks == "0":
          pass
    elif not int(qty_attacks) >0:
       msg.append("Please enter more than 0 number of attacks.")

    algo = request.form['algo']
    algo = algo.strip()
    algo = algo.lower()
    algotypes = ["defensive","steady","offensive","titfortat","random","buggy"]
    if algo == "":
       msg.append("Please enter any of the following algorithms: defensive, steady, offensive, titfortat, random or buggy")
    elif not algo in algotypes:
       msg.append(f"This is not a valid method of algorithm: {algo}")
       msg.append("Please enter any of the following algorithms: defensive, steady, offensive, titfortat, random or buggy")
    
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();
       
    if len(msg)>0:
       return render_template("buggy-form.html", list_of_msg=msg, buggy=record)
    try:
      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute("UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, algo=?  WHERE id=?",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, DEFAULT_BUGGY_ID))
        con.commit()
        msg = "Record successfully saved"
    except:
      con.rollback()
      msg = "error in update operation"
    finally:
      con.close()
      return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone(); 
  return render_template("buggy.html", buggy = record)

#def total_cost():
  #con = sql.connect(DATABASE_FILE)
  #con.row_factory = sql.Row
  #cur = con.cursor()
  #cur.execute("SELECT * FROM buggies")
  #record = cur.fetchone();
  #for value in buggies:
     #total = total + value
     #print (total)
  #return render_template("buggy.html", total_cost = total)

import csv
#with open ('costs.csv','w') as csvfile:
   #filewriter = csv.writer(csvfile, delimiter=',',
                           #quotechar='|', quoting=csv.QUOTE_MINIMAL)
   #filewriter.writerow(['json', 'cost'])
   #filewriter.writerow(['petrol', '4'])
   #filewriter.writerow(['fusion', '400'])
   #filewriter.writerow(['steam', '3'])
   #filewriter.writerow(['bio', '5'])
   #filewriter.writerow(['electric', '20'])
   #filewriter.writerow(['rocket', '16'])
   #filewriter.writerow(['hamster', '3'])
   #filewriter.writerow(['thermo', '300'])
   #filewriter.writerow(['solar', '40'])
   #filewriter.writerow(['wind', '20'])
   #filewriter.writerow(['knobbly', '15'])
   #filewriter.writerow(['slick', '10'])
   #filewriter.writerow(['steelband', '20'])
   #filewriter.writerow(['reactive', '40'])
   #filewriter.writerow(['maglev', '50'])
   #filewriter.writerow(['none', '0'])
   #filewriter.writerow(['wood', '40'])
   #filewriter.writerow(['aluminium', '200'])
   #filewriter.writerow(['thinsteel', '100'])
   #filewriter.writerow(['thicksteel', '200'])
   #filewriter.writerow(['titanium', '290'])
   #filewriter.writerow(['spike', '5'])
   #filewriter.writerow(['flame', '20'])
   #filewriter.writerow(['charge', '28'])
   #filewriter.writerow(['biohazard', '30'])
##with open ('costs.csv') as csvfile:
##   reader = csv.DictReader(csvfile)

 


#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/new')
def edit_buggy():
  return render_template("buggy-form.html")


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
  return jsonify(
      {k: v for k, v in dict(zip(
        [column[0] for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
      }
    )

#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete', methods = ['POST'])
def delete_buggy():
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies")
      con.commit()
      msg = "Buggy deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
