##################################################################################################################################################################################################
from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request, flash
from hello_app import app
from flask_wtf import FlaskForm
from wtforms import Form, StringField, DateField, DecimalField, IntegerField
import pyodbc
##################################################################################################################################################################################################
# Initialize PYODBC connection
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:jtilabview.database.windows.net,1433;Database=JTISQL;Uid=LAB;Pwd=450032923Aa!1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()
##################################################################################################################################################################################################
# defines route to send to home page ********handles erros in flash********
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
##################################################################################################################################################################################################
# defines route to send to about page ********need to add scope of cal (maybe table in SQl and check within range)********
@app.route("/about/")
def about():
    return render_template("about.html")
##################################################################################################################################################################################################
# defines route to send to contact page ********sorta complete********
@app.route("/contact/")
def contact():
    return render_template("contact.html")
##################################################################################################################################################################################################
@app.route('/master_search', methods=['GET', 'POST'])
def master_search():
    if request.method == 'POST':
        # Get the AN and SN entered by user
        an = request.form['an']
        sn = request.form['sn']
        if 'TID_search' in request.form:  # if Test button clicked
            cursor.execute(
                'SELECT ID FROM MASTER WHERE AN = ? AND SN = ?', (an, sn))
            master_id = cursor.fetchone()
            if master_id:
                # if MasterID exists, render test result page with MasterID passed as parameter
                master_id = master_id[0]
                return redirect(url_for('test_results', master_id=master_id))
            else:  # if MasterID does not exist, render home page with error message passed as parameter
                flash("No test results found!", "danger")  # show pop-up alert
                return render_template('home.html',)
        elif 'MID_search' in request.form:  # if Data button clicked
            cursor.execute(
                'SELECT ID FROM MASTER WHERE AN = ? AND SN = ?', (an, sn))
            master_id = cursor.fetchone()
            if master_id:
                # if MasterID exists, render data result page with MasterID passed as parameter
                master_id = master_id[0]
                return redirect(url_for('data_results', master_id=master_id))
            else:  # if MasterID does not exist, render home page with error message passed as parameter
                flash("No Equipment found!", "danger")  # show pop-up alert
                return render_template('home.html',)
    else:  # if GET request, render master search form
        cursor.execute('SELECT * FROM MASTER')
        master_results = cursor.fetchall()
        return render_template('master_search.html',master_results=master_results)
##################################################################################################################################################################################################
# defines route for test results page
@app.route('/test_results/<int:master_id>', methods=['GET', 'POST'])
def test_results(master_id):  # add the test data entered by user or retrieve with Master_ID
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
    else:  # if test results do not exist, render home results page with message passed as parameter
        flash("test results dont exist", "danger")  # show pop-up alert
        return render_template('home.html',)  
##################################################################################################################################################################################################
@app.route('/data_results/<int:master_id>', methods=['GET', 'POST'])
def data_results(master_id): # add the data entered by user or retrieve with Master_ID
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
            "SELECT * FROM MASTER WHERE AN = ? AND SN = ?", (an, sn))
        if cursor.fetchone():
            # item already exists, redirect to home page
            flash("Item with AN & SN already exists", "danger")  # show pop-up alert
            return redirect(url_for("home"))
        else:  # item does not exist, insert into database
            cursor.execute("INSERT INTO MASTER ([AN],[Model],[SN],[NOM],[LOC],[CAL DATE],[DUE],[CYCLE],[MANUFACTURE],[PROC],[SPECIAL CAL],[NOTE],[COST],[STANDARD],[Facility]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (an, model, sn, nom, location, cal_date, due, cycle, manufacture, procedure, cert_note, tech_note, cost, standard, facility))
            connection.commit()
            flash("New entry added successfully!", "success")  # show pop-up alert
            # redirect to home page
            return redirect(url_for("home"))
    else:  # request method is GET Retrieve the data results from the database
        cursor.execute('SELECT * FROM MASTER WHERE ID = ?', (master_id,))
        results = cursor.fetchall()
        if results:  # if data results exist
            results = [dict(zip([column[0] for column in cursor.description], row)) for row in results]
            return render_template('data_results.html', results=results, master_id=master_id)
        else:  # if data results do not exist
            flash("No data results found!", "danger")
            return redirect(url_for("home"))
##################################################################################################################################################################################################
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        # Extract the field name and value from the query parameters
        field = request.args.get('field')
        value = request.args.get('value')
        
        # Render a form with the current value of the field
        return render_template('edit.html', field=field, value=value)
    
    elif request.method == 'POST':
        # Extract the field name and new value from the form submission
        field = request.form.get('field')
        new_value = request.form.get('new_value')
        cursor.execute("UPDATE MASTER SET {field} = ? WHERE id = ?", (new_value, id))
        connection.commit()
        return redirect(request.referrer)
##################################################################################################################################################################################################
# run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
