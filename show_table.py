import sqlite3

def see_table(file,table):
  table = table.upper()
  
  try:
    connection = sqlite3.connect(f"./Data/{file}.db")
    sqlCommand = f"""SELECT * FROM {table};"""
    cursor = connection.cursor()
    cursor.execute(sqlCommand)
    rows = [description[0] for description in cursor.description]
    result = cursor.fetchall()
    print(rows)
    with open("./Stats/Console Log.txt","w") as f1:
      f1.write(str(rows))
      for row in result:
        print(row)
        f1.write(str(row))
  except FileNotFoundError:
    print("Table does not exist.")

def main():
  run = "y"
  while run.lower() == "y" or run.lower() == "yes":
    fileTable = input("Which table would you like to view? ")
    if fileTable == "":
      return
    try:
      file, table = fileTable.split(",")[0], fileTable.split(",")[1]
      see_table(file, table)
    except:
      print("Table does not exist, or has been incorrectly spelt.")
    run = input("Keep running? ")

if __name__ == '__main__':
    main()