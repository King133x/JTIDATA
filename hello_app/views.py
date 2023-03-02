from datetime import datetime
from flask import Flask, render_template
from .. import app
import pyodbc



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

#@app.route("/api/data")
#def get_data():
 #   return app.send_static_file("data.json")


@app.route("/api/data")
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