import mysql.connector as dbc
db = dbc.connect(user='user', password='password',
                                              host='host',
                                              database='dbname')
