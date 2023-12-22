import sqlite3
import os

def get_max_storages(th):
  if os.path.exists("./Data/storage_data.db"):
    connection = sqlite3.connect("./Data/storage_data.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM STORAGES WHERE th = {th};"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]
