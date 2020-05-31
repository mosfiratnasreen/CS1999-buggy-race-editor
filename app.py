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
    return render_template("buggy-form.html")
  elif request.method == 'POST':
    msg=[]
    qty_wheels = request.form['qty_wheels']
    qty_wheels = qty_wheels.strip()
##    print("FIXME wooah I am here at line 38")
    if qty_wheels == "":
       msg.append("Please enter a number for quantity of wheels.")
    elif not qty_wheels.isdigit():
       msg.append(f"This is not a valid number of wheels: {qty_wheels}")
    elif not int(qty_wheels) >= 4:
       msg.append("Please enter more than 4 wheels.")
         
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
    powertypes = ["petrol","fusion","steam","bio","electric","rocket","hamster","thermo","solar","wind"]
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
    elif not int(qty_wheels) >= 1:
       msg.append("Please enter more than 1 unit.")
       

    if len(msg)>0:
       return render_template("buggy-form.html", list_of_msg=msg)
    try:
      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute("UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, power_units=?  WHERE id=?",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, DEFAULT_BUGGY_ID))
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
