from flask import Flask, render_template, request, jsonify
import sqlite3 as sql



app = Flask(__name__)


DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


# ------------------------------------------------------------
# the index page
# ------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

# ------------------------------------------------------------
#  init cost
# ------------------------------------------------------------
def get_cost():
    costdict={
        "hamster_booster":5, "fireproof":70,"insulated":100,"antibiotic":90,"banging":42,
        "petrol":4,"fusion":400,"steam":3,"bio":5,"electric":20,"rocket":16,"hamster":3,"thermo":300,"solar":40,"wind":20,
        "knobbly":15,"slick":10,"steelband":20,"reactive":40,"maglev":50,
        "none":0,"wood":40,"aluminium":200,"thinsteel":100,"thicksteel":200,"titanium":290,
        "spike":5,"flame":20,"charge":28,"biohazard":30
    }
    return costdict

# ------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
# ------------------------------------------------------------
@app.route('/new', methods=['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT  * FROM buggies order by ID desc limit 1")
        record = cur.fetchone();
        return render_template("buggy-form.html", buggy=record,new=True)
    elif request.method == 'POST':

        msg = ""
        costs=get_cost()

        qty_wheels=request.form['qty_wheels']
        flag_color = request.form['flag_color'].strip()
        flag_color_secondary = request.form['flag_color_secondary'].strip()
        flag_pattern = request.form['flag_pattern']
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        aux_power_type = request.form['aux_power_type']
        aux_power_units = request.form['aux_power_units']
        hamster_booster = request.form['hamster_booster']
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']
        armour = request.form['armour']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        fireproof = request.form['fireproof']
        insulated = request.form['insulated']
        antibiotic = request.form['antibiotic']
        banging = request.form['banging']
        algo = request.form['algo']

        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone();
        if not qty_wheels.isdigit():
            msg = f"Oh no! This is not a number: {qty_wheels}"
            return render_template("buggy-form.html", msg=msg, buggy=record)
        if (int(qty_wheels) < 4)  or  (int(qty_wheels)%2 ==1):
            msg = f"The number of wheels must be even: {qty_wheels}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not qty_wheels.isdigit():
            msg = f"Oh no! This is not a number: {qty_wheels}"
            return render_template("buggy-form.html", msg=msg, buggy=record)
        if (int(qty_wheels) < 4) or (int(qty_wheels) % 2 == 1):
            msg = f"The number of wheels must be even: {qty_wheels}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if flag_color_secondary.lower() == flag_color.lower():
            msg = f"The second flag colour cannot be the same as the first colour:{flag_color_secondary}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not flag_color.isalpha():
            msg = f"Please enter text for the flag colour!: {flag_color}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not flag_color_secondary.isalpha():
            msg = f"Please enter text for the secondary colour!: {flag_color_secondary}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not qty_tyres.isdigit():
            msg = f"You need to enter a number for the wheels!: {qty_tyres}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not qty_tyres >= qty_wheels:
            msg = f"The number of tyres must be the same or greater than the number of wheels!:{qty_tyres}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not power_units.isdigit():
            msg = f"Please enter a number for the primary power units!: {power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if int(power_units) < 1:
            msg = f"The number of primary power units must be greater than 1: {power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not aux_power_units.isdigit():
            msg = f"Please enter a number for the auxiliary power units!: {aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not hamster_booster.isdigit():
            msg = f"Please enter a number for the Hamster boosters!: {hamster_booster}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not qty_attacks.isdigit():
            msg = f"Please enter a number for the number of attacks!: {qty_attacks}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if power_type == 'fusion' and int(power_units) != 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {power_type, power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if power_type == 'thermo' and int(power_units) != 1:
            msg = f"You can only have one unit for non consumable power!: {power_type, power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if power_type == 'solar' and int(power_units) != 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {power_type, power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if power_type == 'wind' and int(power_units) != 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {power_type, power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if aux_power_type == 'fusion' and int(aux_power_units) > 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {aux_power_type, aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if aux_power_type == 'thermo' and int(aux_power_units) > 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {aux_power_type, aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if aux_power_type == 'solar' and int(aux_power_units) > 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {aux_power_type, aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if aux_power_type == 'wind' and int(aux_power_units) > 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {aux_power_type, aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        total_cost=int(power_units)*costs[power_type.lower()] +int(aux_power_units)*costs[aux_power_type.lower()]+int(hamster_booster)*costs['hamster_booster']+\
                   int(aux_power_units)*costs[tyres.lower()] +costs[armour.lower()]+costs[attack.lower()]+int(fireproof)*costs['fireproof']+int(insulated)*costs['insulated']+int(antibiotic)*costs['antibiotic']


        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
              #  cur.execute(
              #      "UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?,power_units=?,aux_power_type=?,aux_power_units=?, hamster_booster=?, tyres=?, qty_tyres=?, armour=?,  attack=?,  qty_attacks=?, fireproof=?,  insulated=?, antibiotic=?,banging=?, algo=? ,total_cost=? WHERE id=?",
              #      (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type,aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof,insulated, antibiotic, banging, algo,total_cost, DEFAULT_BUGGY_ID)
              #  )
                cur.execute(
                    "INSERT INTO buggies (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type,aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof,insulated, antibiotic, banging, algo,total_cost) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type,aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof,insulated, antibiotic, banging, algo,total_cost)
                )

                con.commit()
                msg = "Record successfully saved"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
            return render_template("updated.html", msg=msg)



# ------------------------------------------------------------
# a page for displaying the buggy
# ------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    records = cur.fetchall();
    return render_template("buggy.html", buggies=records)


# ------------------------------------------------------------
# a page for displaying the buggy
# ------------------------------------------------------------
@app.route('/edit/<buggy_id>', methods=['GET', 'POST'])
def edit_buggy(buggy_id):
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies  WHERE id=?",buggy_id)
        record = cur.fetchone();
        return render_template("buggy-form.html", buggy=record)
    elif request.method == 'POST':
        costs=get_cost()

        qty_wheels=request.form['qty_wheels']

        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone();

        if not qty_wheels.isdigit():
            msg = f"Oh no! This is not a number: {qty_wheels}"
            return render_template("buggy-form.html", msg=msg, buggy=record)
        if (int(qty_wheels) < 4) or (int(qty_wheels) % 2 == 1):
            msg = f"The number of wheels must be even: {qty_wheels}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not qty_wheels.isdigit():
            msg = f"Oh no! This is not a number: {qty_wheels}"
            return render_template("buggy-form.html", msg=msg, buggy=record)
        if (int(qty_wheels) < 4) or (int(qty_wheels) % 2 == 1):
            msg = f"The number of wheels must be even: {qty_wheels}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if flag_color_secondary.lower() == flag_color.lower():
            msg = f"The second flag colour cannot be the same as the first colour:{flag_color_secondary}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not flag_color.isalpha():
            msg = f"Please enter text for the flag colour!: {flag_color}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not flag_color_secondary.isalpha():
            msg = f"Please enter text for the secondary colour!: {flag_color_secondary}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not qty_tyres.isdigit():
            msg = f"You need to enter a number for the wheels!: {qty_tyres}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not qty_tyres >= qty_wheels:
            msg = f"The number of tyres must be the same or greater than the number of wheels!:{qty_tyres}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not power_units.isdigit():
            msg = f"Please enter a number for the primary power units!: {power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if int(power_units) < 1:
            msg = f"The number of primary power units must be greater than 1: {power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not aux_power_units.isdigit():
            msg = f"Please enter a number for the auxiliary power units!: {aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not hamster_booster.isdigit():
            msg = f"Please enter a number for the Hamster boosters!: {hamster_booster}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if not qty_attacks.isdigit():
            msg = f"Please enter a number for the number of attacks!: {qty_attacks}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if power_type == 'fusion' and int(power_units) != 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {power_type, power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if power_type == 'thermo' and int(power_units) != 1:
            msg = f"You can only have one unit for non consumable power!: {power_type, power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if power_type == 'solar' and int(power_units) != 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {power_type, power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if power_type == 'wind' and int(power_units) != 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {power_type, power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if aux_power_type == 'fusion' and int(aux_power_units) > 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {aux_power_type, aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if aux_power_type == 'thermo' and int(aux_power_units) > 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {aux_power_type, aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if aux_power_type == 'solar' and int(aux_power_units) > 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {aux_power_type, aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        if aux_power_type == 'wind' and int(aux_power_units) > 1:
            msg = f"You are only allowed to have one unit for non consumable power!: {aux_power_type, aux_power_units}"
            return render_template("buggy-form.html", msg=msg, buggy=record)

        flag_color = request.form['flag_color'].strip()
        flag_color_secondary = request.form['flag_color_secondary'].strip()
        flag_pattern = request.form['flag_pattern']
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        aux_power_type = request.form['aux_power_type']
        aux_power_units=request.form['aux_power_units']
        hamster_booster = request.form['hamster_booster']
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']
        armour = request.form['armour']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        fireproof = request.form['fireproof']
        insulated = request.form['insulated']
        antibiotic = request.form['antibiotic']
        banging = request.form['banging']
        algo= request.form['algo']



        total_cost=int(power_units)*costs[power_type.lower()] +int(aux_power_units)*costs[aux_power_type.lower()]+int(hamster_booster)*costs['hamster_booster']+\
                   int(aux_power_units)*costs[tyres.lower()] +costs[armour.lower()]+costs[attack.lower()]+int(fireproof)*costs['fireproof']+int(insulated)*costs['insulated']+int(antibiotic)*costs['antibiotic']
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?,power_units=?,aux_power_type=?,aux_power_units=?, hamster_booster=?, tyres=?, qty_tyres=?, armour=?,  attack=?,  qty_attacks=?, fireproof=?,  insulated=?, antibiotic=?,banging=?, algo=? ,total_cost=? WHERE id=?",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type,aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof,insulated, antibiotic, banging, algo,total_cost, buggy_id)
                )
                cur.execute(
                    "INSERT INTO buggies (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type,aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof,insulated, antibiotic, banging, algo,total_cost) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type,aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof,insulated, antibiotic, banging, algo,total_cost)
                )

                con.commit()
                msg = "Record successfully saved"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
            return render_template("updated.html", msg=msg)




# ------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping directly into the
#   database
# ------------------------------------------------------------
@app.route('/json/<buggy_id>')
def summary(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? ", buggy_id)
    return jsonify(
        {k: v for k, v in dict(zip(
            [column[0] for column in cur.description], cur.fetchone())).items()
         if (v != "" and v is not None)
         }
    )


# ------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
# ------------------------------------------------------------
@app.route('/delete/<buggy_id>', methods=['POST', 'GET'])
def delete_buggy(buggy_id):
    try:
        msg = "deleting buggy"
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM buggies  where id=?",buggy_id)
            con.commit()
            msg = "Buggy deleted"
    except:
        con.rollback()
        msg = "error in delete operation"
    finally:
        con.close()
        return render_template("updated.html", msg=msg)


#---------------------------------------------------------------
@app.route('/poster')
def poster():
    return render_template('poster.html')






if __name__ == '__main__':
    #    app = Flask(__name__)
    #    app.config['FLASK_ENV']='production'
    #    app.config['FLASK_ENV']='development'
    app.run(debug=True, host="localhost", port=5000)

