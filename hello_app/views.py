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
# Azure Storage account details
STORAGE_ACCOUNT_NAME = "<storage-account-name>"
STORAGE_ACCOUNT_KEY = "<storage-account-key>"
CONTAINER_NAME = "<container-name>"
# Create a BlobServiceClient object
# blob_service_client = BlobServiceClient.from_connection_string(
#     f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net")
##################################################################################################################################################################################################

##################################################################################################################################################################################################
# defines route to send to home page ********handles erros in flash********


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
    # def get_image(filename):
    #     try:
    #         # Get a BlobClient object for the image file
    #         blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=filename)

    #         # Download the image data
    #         image_data = blob_client.download_blob().content_as_bytes()

    #         # Create a Flask response with the image data and return it
    #         return Response(image_data, mimetype='image/jpeg')

    #     except Exception as e:
    #         print(e)
    #         return Response(status=404)
##################################################################################################################################################################################################
# defines route to send to about page ********need to add scope of cal (maybe table in SQl and check within range)********


@app.route("/about/")
def about():
    return render_template("about.html")
##################################################################################################################################################################################################
# defines route to send to contact page ********need to add some basic contact********


@app.route("/contact/")
def contact():
    return render_template("contact.html")
##################################################################################################################################################################################################
# handles the data search ajax uses post to get data


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
        return render_template('master_search.html')
##################################################################################################################################################################################################
# looks up the master and test table


@app.route('/master_record/<int:master_id>', methods=['GET', 'POST'])
def master_record(master_id):
    if request.method == "POST":
        unit = request.form['unit']
        nom = request.form['nom']
        actual = request.form['actual']
        tol = request.form['tol']
        cursor.execute('INSERT INTO TEST (Master_ID, unit, nom, actual, tol) VALUES (?, ?, ?, ?, ?)',
                       (master_id, unit, nom, actual, tol))
        cursor.commit()
        flash("Test results added successfully!", "success")
        return redirect(url_for("master_record", master_id=master_id))
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
