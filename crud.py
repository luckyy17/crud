from dataclasses import replace
import psycopg2 as db
import os

con = None
connected = None
cursor = None

# Nama : Lucky Saputra
# NIM : 200511086
# Kelas : 20-C1C-R2

def connect():
    global connected
    global con
    global cursor
    try:
        con = db.connect(
            host = "localhost",
            database = "toko_mainan",
            port = 5432,
            user = "postgres",
            password = "root"
        )
        cursor = con.cursor()
        connected = True
    except:
        connected = False
    return cursor

def disconnect():
    global connected
    global con
    global cursor
    if(connected==True):
        cursor.close()
        con.close()
    else:
        con = None
    connected = False

def insert_data(db):
  global connected
  global con
  global cursor
  name = input("Masukan Nama: ")
  address = input("Masukan Alamat: ")
  country = input("Masukan Negara : ")
  val = (name, address, country)
  a = connect()
  sql = "INSERT INTO customers (name, address,country) VALUES (%s, %s, %s)"
  a.execute(sql, val)
  con.commit()
  print("{} data berhasil disimpan".format(cursor.rowcount))


def show_data(db):
  global connected
  global con
  global cursor
  a = connect()
  sql = "SELECT * FROM customers"
  a.execute(sql)
  record = a.fetchall()
  a.execute(sql)
  results = a.fetchall()
  
  if a.rowcount < 0:
    print("Tidak ada data")
  else:
    for data in results:
      print(data)


def update_data(db):
  global connected
  global con
  global cursor
  a = connect()
  show_data(db)
  customer_id = input("pilih id customer> ")
  sql = "select * from customers where customer_id = '" + customer_id + "'" 
  a.execute(sql)
  record = a.fetchall()
  print("Data saat ini :")
  print(record)
  row = a.rowcount
  if(row==1):
        print("Silahkan untuk mengubah data...")
        name = input("Nama baru: ")
        address = input("Alamat baru: ")
        country = input("ID Negara : ")
        a = connect()
        sql = "update customers set name ='" + name + "', address='" + address + "', country='" + country + "' where customer_id='" + customer_id + "'"
        a.execute(sql)
        con.commit()
        print("Update is done.")
        sql = "select * from customers where name = '" + name + "'"
        a.execute(sql)
        rec = a.fetchall()
        print("Data setelah diubah :")
        print(rec)
    
  else:
        print("Data tidak ditemukan...")


  sql = "UPDATE customers SET name=%s, address=%s , country=%s WHERE customer_id=%s"
  val = (name, address, country, customer_id)
  a.execute(sql, val)
  con.commit()
  print("{} data berhasil diubah".format(a.rowcount))


def delete_data(db):
  global connected
  global con
  global cursor
  a = connect()
  show_data(db)
  customer_id = input("pilih id customer> ")
  sql = "select * from customers where customer_id = '" + customer_id + "'"
  a.execute(sql)
  record = a.fetchall()
  row = a.rowcount
  if (row==1):
        jwb = input("Apakah ingin menghapus data? (y/t): ")
        if(jwb.upper()=="Y"):
            a = connect()
            sql = "delete from customers where customer_id='" + customer_id + "'"
            val = (customer_id,)
            a.execute(sql,val)
            con.commit()
            print("Delete is done.")
        else:
            print("Data batal untuk dihapus.")
  else:
        print("Data tidak ditemukan...")

def search_data(db):
  global connected
  global con
  global cursor
  keyword = input("Kata kunci: ")
  a = connect()
  sql = "select * from customers where name like %s or address like %s"
  val = ("%{}%".format(keyword), "%{}%".format(keyword))
  a.execute(sql, val)
  results = a.fetchall()
  
  if a.rowcount <= 0:
      print("Tidak ada data")
  else:
    for data in results:
      print(data)


def show_menu(db):
  print("=== APLIKASI DATABASE PYTHON ===")
  print("1. Insert Data")
  print("2. Tampilkan Data")
  print("3. Update Data")
  print("4. Hapus Data")
  print("5. Cari Data")
  print("0. Keluar")
  print("------------------")
  menu = input("Pilih menu> ")

  #clear screen
  os.system("cls")

  if menu == "1":
    insert_data(db)
  elif menu == "2":
    show_data(db)
  elif menu == "3":
    update_data(db)
  elif menu == "4":
    delete_data(db)
  elif menu == "5":
    search_data(db)
  elif menu == "0":
    disconnect()
  else:
    print("Menu salah!")


if __name__ == "__main__":
  while(True):
    show_menu(db)