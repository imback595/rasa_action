import pymssql



def find_scheme(Schemecode):
    sql='''select SubId,TableName FROM [LearnDb].[dbo].[TreatSubRelation] where IndCode like '{}-%' '''.format(Schemecode)
    try:
        cursor.execute(sql)
        data=cursor.fetchall()
        return data
    except Exception as e:
        print(e)



def getsubscheme(SubId,TableName):
    sql=''' select * from  [LearnDb].[dbo].[{}] where Id={}'''.format(TableName,SubId)
    try:
        cursor.execute(sql)
        data=cursor.fetchall()
        return {TableName:data}
    except Exception as e:
        print(e)






def run():
    schemecode='1-180'
    data=find_scheme(schemecode)
    for each in data:
        a=getsubscheme(each[0],each[1])
        print(a)









if __name__=='__main__':
    conn = pymssql.connect(host='192.168.168.250', user='sa', password='123456', database='LearnDb',
                           autocommit=True)
    cursor = conn.cursor()



    run()
    cursor.close()
    conn.close()
















