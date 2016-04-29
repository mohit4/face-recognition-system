#!/usr/bin/python

import sqlite3

#insert and return the last auto incremented id
def sqlite_new_user(name,age,desc):
	#database name is given and connection is established
	database = 'frcg.db'
	conn = sqlite3.connect(database)
	query = "insert into person (name,age,desc) values (\'"+name+"\',"+str(age)+",\'"+desc+"\')"
	#for debugging purpose only
	#print query
	conn.execute(query)
	conn.commit()
	res=conn.execute("select last_insert_rowid()")
	r=res.fetchone()[0]
	#connection closed
	conn.close()
	return r

#will give name,age and desc from a id
def sqlite_get_info(id):
	name_age_desc = ()
	#database name is given and connection is established
	database = 'frcg.db'
	conn = sqlite3.connect(database)
	query = "select name,age,desc from person where id="+str(id)
	#for debugging purpose only
	#print query
	result=conn.execute(query)
	for row in result:
		name_age_desc = (str(row[0]),row[1],str(row[2]))
	#connection closed
	conn.close()
	return name_age_desc

#will give the list of ids
def sqlite_get_ids():
	ids=[]
	#database name is given and connection is established
	database = 'frcg.db'
	conn = sqlite3.connect(database)
	query = "select id from person"
	#for debugging purpose only
	#print query
	result=conn.execute(query)
	for row in result:
		ids.append(row[0])
	#connection closed
	conn.close()
	return ids

#for debugging purposes
#def add_some():
#	l=sqlite_new_user('Mayank',14,'My brother')
#	print l,type(l)
#	m=sqlite_new_user('Rohan',12,'')
#	print m
