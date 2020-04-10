import psycopg2
conn = psycopg2.connect('dbname=postgres')
cur = conn.cursor()

"""
cur.execute('DROP TABLE IF EXISTS tb2;')
cur.execute('''
create table tb2(
id serial PRIMARY KEY,
des VARCHAR NOT NULL);
''')

 """
sql = 'insert into tb2(id,des) values(%(id)s, %(des)s);'
data = {
    'id':8,
    'des':'blink'
}
cur.execute(sql, data)
cur.execute('select * from tb2;')
r = cur.fetchall()
print("fetchall: ",r)
conn.commit()
cur.close()
conn.close()
