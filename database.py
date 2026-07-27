import mysql.connector

db = mysql.connector.connect(

    host="localhost",
    user="root",
    password="Ari@12345",
    database="guardrail_monitor"

)

cursor = db.cursor()
print("Connected to SQL")