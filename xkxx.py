# from databaseconfig.connectdbs import connect
# from common.fileAction import controls as file
# import time
# # start=time.perf_counter()
# con=connect()
# # xk=file.fileInfo(r"C:\Users\80662\Desktop\ytk\数据\选课信息0.xlsx")
# # content=xk.getFileContent()
# # insertCode='''insert into xk(jxbmc,xh) values (:1,:2)'''
# # con.execute(insertCode,content)
# # end=time.perf_counter()
# # print('旧的已完成{}'.format(str(end-start)))
# # start=time.perf_counter()
# # xk1=file.fileInfo(r"C:\Users\80662\Desktop\ytk\ytk\选课信息.xlsx")
# # content=xk1.getFileContent()
# # insertCode='''insert into xk1(jxbmc,xh) values(:1,:2)'''
# # con.execute(insertCode,content)
# # end=time.perf_counter()
# # print('新的已完成{}'.format(str(end-start)))
# selectCode='''select * from xk1 where not exists(select 1 from xk where xk1.jxbmc=xk.jxbmc and xk1.xh=xk.xh)'''
# content=con.execute(selectCode)
# res=file.fileInfo('res')
# res.expXlsx(content=content)
# con.close()

# import cx_Oracle
# connectString='XXXXXXXXXXXXX'
# con=cx_Oracle.connect(connectString)
# cur=con.cursor()
# res=cur.callfunc(
#     'likai_getxsxnxqcjpm',
#     str,
#     ['1665700050','2018','2017','cj','2','1']
# )
# con.close()
# print(res)