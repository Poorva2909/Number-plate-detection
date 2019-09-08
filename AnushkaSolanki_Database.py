import sqlite3
import AnushkaSolanki_Predict
conn=sqlite3.connect('minor.db')
q=conn.cursor()
#for first time creation of DB
#q.execute("""CREATE TABLE minor_database1(
#registration_no text,
#owner_name text,
#contact_no integer,
#address text
#)""")
#for first time insertion into DB
#q.execute("INSERT INTO minor_database1 VALUES ('MP09CX4057','Praveena',9589807327,'Indore')")
b=AnushkaSolanki_Predict.finalPlate_str
print('Data of Recognised Vehicle:\n')
#c.execute("SELECT * FROM minor_database1")
q.execute("SELECT * FROM minor_database1 WHERE registration_no=?",(b,))
print(*q.fetchall())
conn.commit()
conn.close()

