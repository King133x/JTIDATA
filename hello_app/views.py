from datetime import datetime as dt
from flask import Flask, render_template, url_for, redirect, request, flash
from hello_app import app
import pyodbc

#################################################################################################
#defines route to send to homepage
@app.route("/")
def home():
    return render_template("home.html")
#################################################################################################
#defines route to send to about page
@app.route("/about/")
def about():
    return render_template("about.html")
#################################################################################################
#defines route to send to contact page
@app.route("/contact/")
def contact():
    return render_template("contact.html")
#################################################################################################
#defines route to send to data page
@app.route("/data")
def get_data():
    # Initialize ODBC connection
    connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:jtilabview.database.windows.net,1433;Database=JTISQL;Uid=LAB;Pwd=450032923Aa!1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    connection = pyodbc.connect(connection_string)
    # create a cursor to execute SQL queries
    cursor = connection.cursor()
    # execute a SELECT query to get the top 100 rows from your table
    cursor.execute("SELECT TOP 100 * FROM MASTER")
     # fetch all the rows from the query result
    rows = cursor.fetchall()
     # close the connection
    connection.close()
    # convert the rows to a list of dictionaries
    data = []
    for row in rows:
     data.append(dict(zip([column[0] for column in cursor.description], row)))
     # render the template with the data
    return render_template("data.html", data=data)
#################################################################################################
#defines route to send to entry page
@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():
 # get form data
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
        connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:jtilabview.database.windows.net,1433;Database=JTISQL;Uid=LAB;Pwd=450032923Aa!1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM MASTER WHERE an = ? AND sn = ?", (an, sn))
        if cursor.fetchone():
     # item already exists, redirect to home page
            flash("Item already exists!", "danger") # show pop-up alert
            connection.close()
            return redirect(url_for("home"))
    # item does not exist, insert into database
        cursor.execute("INSERT INTO MASTER ([AN],[Model],[SN],[NOM],[LOC],[CAL DATE],[DUE],[CYCLE],[MANUFACTURE],[PROC],[SPECIAL CAL],[NOTE],[COST],[STANDARD],[Facility]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        an, model, sn, nom, location, cal_date, due, cycle, manufacture, procedure, cert_note, tech_note, cost, standard, facility)
        connection.commit()
        connection.close()
        flash("New entry added successfully!", "success") # show pop-up alert
        # redirect to home page
        return redirect(url_for("home"))
#################################################################################################
#END OF IF for POST if GET request, render the add entry template




    return render_template("add_entry.html")
#################################################################################################