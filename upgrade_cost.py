import sqlite3

connection = sqlite3.connect("./Data/costs.db")
cursor = connection.cursor()
"""
sqlCreateCommand = CREATE TABLE IF NOT EXISTS COSTS(
  dust int,
  gold int
);
cursor.execute(sqlCreateCommand)

with open("./Stats/r1999 costs sorted.txt", "r") as f1:
  for line in f1:
    newline = line.split(" ")
    sqlInsertCommand = fINSERT INTO COSTS VALUES ("{newline[1]}",{newline[2]});
    cursor.execute(sqlInsertCommand)
    connection.commit()
"""

sqlCommand = """SELECT * FROM COSTS
  ORDER BY
  dust ASC,
  gold ASC
;"""
cursor = connection.cursor()
cursor.execute(sqlCommand)
result = cursor.fetchall()

with open("./Stats/r1999 costs high-low.txt", "w") as f1:
  for item in result:
    f1.write(f"{item[0]} {item[1]}\n")
