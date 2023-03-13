#################################################################################################
from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request, flash
from hello_app import app
import pyodbc
#################################################################################################
# Initialize PYODBC connection
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:jtilabview.database.windows.net,1433;Database=JTISQL;Uid=LAB;Pwd=450032923Aa!1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()
#################################################################################################
# defines route to send to home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
#################################################################################################
# defines route to send to about page
@app.route("/about/")
def about():
    return render_template("about.html")
#################################################################################################
# defines route to send to contact page
@app.route("/contact/")
def contact():
    return render_template("contact.html")
#################################################################################################
# defines route to send to data page
@app.route("/data")
def get_data():
    # execute a SELECT query to get rows from your table
    cursor.execute("SELECT * FROM MASTER")
    # fetch all the rows from the query result
    rows = cursor.fetchall()
    # convert the rows to a list of dictionaries
    data = []
    for row in rows:
        data.append(dict(zip([column[0]
        for column in cursor.description], row)))
        # render the template with the data
    return render_template("data.html", data=data)
#################################################################################################
# defines route to send to entry page
@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():  # get form data and and create entry if none exist
    if request.method == "POST":
        an = request.form.get("an")
        model = request.form.get("model")
        sn = request.form.get("sn")
        nom = request.form.get("nom")
        location = request.form.get("location")
        cal_date = request.form.get("cal_date")
        due = request.form.get("due")
        cycle = 1  # assume 1 year cycle
        manufacture = request.form.get("manufacture")
        procedure = request.form.get("procedure")
        cert_note = request.form.get("cert_note")
        tech_note = request.form.get("tech_note")
        cost = request.form.get("cost")
        standard = request.form.get("standard")
        facility = request.form.get("facility")
        # check if item already exists in the database
        cursor.execute(
            "SELECT * FROM MASTER WHERE an = ? AND sn = ?", (an, sn))
        if cursor.fetchone():
            # item already exists, redirect to home page
            flash("Item already exists!", "danger")  # show pop-up alert
            return redirect(url_for("home"))
        else:  # item does not exist, insert into database
            cursor.execute("INSERT INTO MASTER ([AN],[Model],[SN],[NOM],[LOC],[CAL DATE],[DUE],[CYCLE],[MANUFACTURE],[PROC],[SPECIAL CAL],[NOTE],[COST],[STANDARD],[Facility]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           an, model, sn, nom, location, cal_date, due, cycle, manufacture, procedure, cert_note, tech_note, cost, standard, facility)
            connection.commit()
            flash("New entry added successfully!",
                  "success")  # show pop-up alert
            # redirect to home page
            return redirect(url_for("home"))
    else:  # if GET request, render the add entry template
        return render_template("add_entry.html")
#################################################################################################
# defines route to send to test input
@app.route('/test_request.html', methods=['GET', 'POST'])
def test_request():
    if request.method == 'POST':
        # Get the AN and SN entered by user
        an = request.form['an']
        sn = request.form['sn']
        cursor.execute(
            'SELECT ID FROM MASTER WHERE AN = ? AND SN = ?', (an, sn))
        master_id = cursor.fetchone()
        if master_id:
            # if MasterID exists, render test result page with MasterID passed as parameter
            master_id = master_id[0]
            return redirect(url_for('test_results', master_id=master_id))
        else:  # if MasterID does not exist, render home page with error message passed as parameter
            flash("No test results found!","danger")  # show pop-up alert
        return render_template('home.html',)
    else:  # if GET request, render test request
        return render_template('test_request.html')
#################################################################################################
# defines route for test results page
@app.route('/test_results/<int:master_id>', methods=['GET', 'POST'])
def test_results(master_id):  # Get the test data entered by user or retrieve with Master_ID
    if request.method == 'POST':
        unit = request.form['unit']
        nom = request.form['nom']
        actual = request.form['actual']
        tol = request.form['tol']
        # Insert the test data into the database
        cursor.execute('INSERT INTO TEST (Master_ID, unit, nom, actual, tol) VALUES (?, ?, ?, ?, ?)',
                       (master_id, unit, nom, actual, tol))
        cursor.commit()
        cursor.execute('SELECT * FROM TEST WHERE Master_ID = ?', (master_id,))
        results = cursor.fetchall()
        return render_template('test_results.html', results=results, master_id=master_id)
    else:  # Retrieve the test results from the database
        cursor.execute('SELECT * FROM TEST WHERE Master_ID = ?', (master_id,))
        results = cursor.fetchall()
    if results:  # if test results exist, render test results page with results and master_id passed as parameters
        results = [dict(zip([column[0] for column in cursor.description], row))
                   for row in results]
        return render_template('test_results.html', results=results, master_id=master_id)
    else:  # if test results do not exist, render test results page with message passed as parameter
        flash("get test results dont exist", "danger")  # show pop-up alert
        return render_template('home.html',)
#################################################################################################
