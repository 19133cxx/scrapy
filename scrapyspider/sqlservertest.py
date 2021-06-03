# import pymssql
# conn = pymssql.connect("127.0.0.1", database="Test", user="sa", password="123456")
# cursor = conn.cursor()
# insert_sql="""insert into Test_Code(id,name)
# values(%d, %s)
# """""
# params=list()
# params.append(123)
# params.append('NULL')
# cursor.execute(insert_sql,tuple(params))
# conn.commit()
list=[]
if list:
    print(1);
else:
    print(2)