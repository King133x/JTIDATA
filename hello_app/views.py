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
@app.route('/master_search/', methods=['GET', 'POST'])
def master_search():
    if request.method == 'POST': # Get the MID by user
        master_id = request.form['master_id']
        cursor.execute('SELECT * FROM MASTER WHERE ID = ?', (master_id,))
        master_result = cursor.fetchone()
        if master_result: # if MasterID exists, send MasterID to master_result page
            return redirect(url_for('master_results', master_id=master_id,))
        else:  # if MasterID does not exist, render home page with error message passed as parameter
            flash("No equipment found with this MID!",
                  "danger")  # show pop-up alert
            return render_template('home.html',)
    else:  # if GET request, render master search form
        cursor.execute('SELECT * FROM MASTER')
        master_search = cursor.fetchall()
        return render_template('master_search.html', master_search=master_search)
##################################################################################################################################################################################################
@app.route('/master_results/<int:master_id>', methods=['GET', 'POST'])
def master_results(master_id):  # add the data entered by user or retrieve with Master_ID
    if request.method == "POST":
        flash("No master POST!", "danger")
        return redirect(url_for("home"))
    else:  # request method is GET Retrieve the data results from the database
        cursor.execute('SELECT * FROM MASTER WHERE ID = ?', (master_id,))
        master_results = cursor.fetchall()
        if master_results:  # if data results exist
            master_results = [
                dict(zip([column[0] for column in cursor.description], row)) for row in master_results]
            cursor.execute(
                'SELECT * FROM TEST WHERE Master_ID = ?', (master_id,))
            results = cursor.fetchall()
            if results:  # if test results exist, render test results page with results and master_id passed as parameters
                results = [dict(zip([column[0] for column in cursor.description], row))
                           for row in results]
            else:  # if test results do not exist, render message passed as parameter
                flash("test results dont exist", "danger")  # show pop-up alert
            return render_template('data_results.html', master_results=master_results, master_id=master_id,results=results)
        else:  # if data results do not exist
            flash("No data results found!", "danger")
            return redirect(url_for("home"))
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
        return redirect(url_for('master_results', master_id=master_id,))
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
# run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
##################################################################################################################################################################################################