##################################################################################################################################################################################################
from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from hello_app import app
from flask_wtf import FlaskForm
from wtforms import Form, StringField, DateField, DecimalField, IntegerField
import pyodbc
# from azure.storage.blob import BlobServiceClient
##################################################################################################################################################################################################
# Initialize PYODBC connection
connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:jtilabview.database.windows.net,1433;Database=JTISQL;Uid=LAB;Pwd=450032923Aa!1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()
# set up SQL querys to be dictionaries
def query_to_dict(query_results):
    return [dict(zip([column[0] for column in cursor.description], row)) for row in query_results]
##################################################################################################################################################################################################
# defines route to send to home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
##################################################################################################################################################################################################
# handles the data search ajax uses post to get data else sends to search page
@app.route('/master_data/', methods=['GET', 'POST'])
def master_data():
    if request.method == 'POST':
        cursor.execute('SELECT * FROM MASTER')
        master_search = query_to_dict(cursor.fetchall())
        if master_search:
            return jsonify({"data": master_search})
        else:
            flash("No equipment found with this MID!", "danger")
            return redirect(url_for('home'))
    else:
        cursor.execute('SELECT * FROM overdue_table')
        overdue_table = query_to_dict(cursor.fetchall())
        return render_template('master_search.html',overdue_table=overdue_table)
##################################################################################################################################################################################################
# looks up the master and test table


@app.route('/master_record/<int:master_id>', methods=['GET', 'POST', 'PUT'])
def master_record(master_id):
    if request.method == "POST":
        action = request.form.get('action')
        if action == 'update_master':
            # Update master record
            an = request.form['an']
            model = request.form['model']
            sn = request.form['sn']
            nom = request.form['nom']
            loc = request.form['loc']
            cal_date = request.form['cal_date']
            due = request.form['due']
            cycle = request.form['cycle']
            manufacture = request.form['manufacture']
            proc = request.form['proc']
            special_cal = request.form['special_cal']
            note = request.form['note']
            cost = request.form['cost']
            standard = request.form['standard']
            facility = request.form['facility']
            cursor.execute('UPDATE MASTER SET AN = ?, Model = ?, SN = ?, NOM = ?, LOC = ?, [CAL DATE] = ?, DUE = ?, CYCLE = ?, MANUFACTURE = ?, [PROC] = ?, [SPECIAL CAL] = ?, NOTE = ?, COST = ?, STANDARD = ?, Facility = ? WHERE ID = ?',
               (an, model, sn, nom, loc, cal_date, due, cycle, manufacture, proc, special_cal, note, cost, standard, facility, master_id))
            cursor.commit()
            flash("CHANGES added successfully!", "success")
            return redirect(url_for("master_record", master_id=master_id))
        else:
            # Add new test record
            unit = request.form['unit']
            nom = request.form['nom']
            actual = request.form['actual']
            tol = request.form['tol']
            temp = request.form['temp']
            humidity = request.form['humidity']
            tech = request.form['tech']
            cursor.execute('INSERT INTO TEST (Master_ID, unit, nom, actual, tol, temp, humidity, tech) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                           (master_id, unit, nom, actual, tol, temp, humidity, tech))
            cursor.commit()
            flash("Test results added successfully!", "success")
            return redirect(url_for("master_record", master_id=master_id))
    elif request.method == "PUT":
        # This code handles the AJAX PUT request for updating the master record
        # The master record is updated in the if statement above
        pass
    else:
        if 'json' in request.args:
            # Return JSON data for DataTables
            cursor.execute('SELECT * FROM MASTER WHERE ID = ?', (master_id,))
            master_results = query_to_dict(cursor.fetchall())
            cursor.execute(
                'SELECT * FROM TEST WHERE Master_ID = ?', (master_id,))
            test_results = query_to_dict(cursor.fetchall())
            return jsonify({'master': master_results, 'test': test_results})
        else:
            cursor.execute('SELECT * FROM MASTER WHERE ID = ?', (master_id,))
            master_results = query_to_dict(cursor.fetchall())
            if master_results:
                cursor.execute(
                    'SELECT * FROM TEST WHERE Master_ID = ?', (master_id,))
                test_results = query_to_dict(cursor.fetchall())
                if not test_results:
                    flash("No test results found!", "danger")
                return render_template('master_record.html', master_results=master_results, master_id=master_id, test_results=test_results)
            else:
                flash("No master record found!", "danger")
                return redirect(url_for("home"))
##################################################################################################################################################################################################

##################################################################################################################################################################################################


##################################################################################################################################################################################################
# run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
##################################################################################################################################################################################################
