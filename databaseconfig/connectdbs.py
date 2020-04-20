import cx_Oracle
from databaseconfig import connectString as cs
from datetime import datetime
import pymssql
import os
import poplib
import smtplib

class connect:
    def __init__(self, dbType='oracle',
                 connectString=cs.appJwglxt,
                 mailServer=cs.mailpop['mailserver'],mailPort=cs.mailpop['mailport'],
                 mailUser=cs.mailuser['username'],mailPassWord=cs.mailuser['password'],
                 smtpServer=cs.mailsmtp['mailserver'],smtpPort=cs.mailsmtp['mailport']):
        '''
        创建连接类
        :param connectString:连接字符串,默认连接教务系统的数据库
        '''
        self.type = dbType.strip().lower()
        if self.type == 'oracle':
            if connectString==cs.appJwglxt or connectString==cs.localJwglxt:
                try:
                    self.con = cx_Oracle.connect(connectString,encoding='utf-8')
                except:
                    self.con=cx_Oracle.connect(cs.localJwglxt,encoding='utf-8')
                self.cur = self.con.cursor()
                #print('''select zc,xqj from jw_pk_rcmxb where rq='{}' and 1=1'''.format(datetime.now().strftime('%Y-%m-%d')))
                try:
                    self.currentZcXqj = self.execute(
                        '''select zc,xqj from jw_pk_rcmxb where rq='{}' and 1=1'''.format(datetime.now().strftime('%Y-%m-%d')))[0]
                except:
                    self.currentZcXqj=(0,0)
            else:
                self.con = cx_Oracle.connect(connectString, encoding='utf-8')
                self.cur = self.con.cursor()
                self.currentZcXqj=None
        elif self.type == 'mssql':
            self.con = pymssql.connect(**cs.appSyjxxt)
            self.cur = self.con.cursor()
            self.currentZcXqj = None
        elif self.type=='mailpop':
            try:
                self.con=poplib.POP3_SSL(mailServer,mailPort)
                self.con.user(mailUser)
                self.con.pass_(mailPassWord)
                self.cur=None
                self.currentZcXqj=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
            except:
                self.con=None
                self.cur=None
                self.currentZcXqj=None
        elif self.type=='mailsmtp':
            try:
                self.con=smtplib.SMTP_SSL(smtpServer,smtpPort)
                self.con.login(mailUser,mailPassWord)
                self.cur=None
                self.currentZcXqj=None
            except:
                self.con=None
                self.cur=None
                self.currentZcXqj=None
        else:
            self.con = None
            self.cur = None
            self.currentZcXqj = None

    def close(self):
        '''
        关闭连接
        :return:
        '''

        self.cur.close()
        self.con.close()

    def commits(self):
        '''
        提交变更
        :return:
        '''
        self.con.commit()

    def executeSelect(self, queryString=''):
        '''执行select查询'''
        if self.type == 'oracle':
            return self.cur.execute(queryString.replace(';', '')).fetchall()
        else:
            self.cur.execute(queryString)
            return self.cur.fetchall()

    def executeDelAndUp(self, queryString=''):
        '''执行delete,update,不带参数的语句'''

        if self.type == 'oracle':
            self.cur.execute(queryString.replace(';', ''))
        else:
            self.cur.execute(queryString)
        return 1

    def callProcOrFuntion(self, queryString='', paras=[], isFunRetuType='varchar2',dbms_output=cs.oracle_dbms_output):
        '''
        :param queryString: 函数或过程的对象名
        :param paras: 传入函数或过程的参数
        :param isFunRetuType: 函数对象的返回值类型，默认为varchar2
        :return: 如果过程执行成功，则返回1，如果函数执行成功，则返回函数的返回值
        '''
        # if self.objectExists(queryString):
        #print(queryString,paras)
        if not paras:
            paras = [0]
        try:
            # print(1)
            if dbms_output:
                self.cur.callproc("dbms_output.enable")
            self.cur.callproc(queryString, paras)

            if dbms_output:
                textVar = self.cur.var(str)
                statusVar = self.cur.var(int)
                while True:
                    self.cur.callproc("dbms_output.get_line", (textVar, statusVar))
                    if statusVar.getvalue() != 0:
                        break
                    print(textVar.getvalue())
            return 1
        except:
            # print(2)
            return self.cur.callfunc(queryString, isFunRetuType, paras)

    def objectExists(self, queryString=''):
        '''判断对象是否存在'''
        if self.type == 'oracle':
            objCount = '''
            select count(1) from all_objects where lower(object_name)=lower('{}')
            and lower(owner)='gzdx_jw_user' and 1=1
            '''.format(queryString.replace(';', ':'))
            return self.executeSelect(objCount)
        elif self.type == 'mssql':
            objCount = '''select object_id('{}')'''.format(queryString)
            return self.executeSelect(objCount)

    def executeIn(self, queryString='', L=[]):
        '''执行更新操作
        :param L的格式为[(),()]'''
        if self.type == 'oracle':
            self.cur.executemany(queryString.replace(';', ''), L)
        else:
            self.cur.executemany(queryString, L)
        return 1


    def executeRestore(self, queryString=''):
        '''mssql 的数据库恢复
        :param queryString format is sqlcmd - i "file_path"'''
        if self.type == 'mssql':
            os.system(queryString)
            return 1

    def execute(self, queryString='', L=[], isFunRetuType='varchar2'):
        '''执行简单sql语句'''
        res = None
        if self.type == 'oracle':
            isQuery = queryString.strip().lower()
            if isQuery.startswith('select'):
                res = self.executeSelect(queryString)
            elif isQuery.startswith('delete')  or isQuery.startswith('drop') or isQuery.startswith('create')\
                    or isQuery.startswith('analyze'):
                res = self.executeDelAndUp(queryString)
            elif isQuery.startswith('update'):
                if L:
                    res = self.executeIn(queryString, L)  ##带参数的插入
                else:
                    res = self.executeDelAndUp(queryString)  ##不带参数的插入
            elif isQuery.startswith('insert'):
                if L:
                    res = self.executeIn(queryString, L)  ##带参数的插入
                else:
                    res = self.executeDelAndUp(queryString)  ##不带参数的插入
            elif isQuery.startswith('begin') or isQuery.startswith('declare'):
                pass  ####执行匿名程序块
            else:
                res=self.callProcOrFuntion(queryString, L, isFunRetuType)
                ##调用存储过程或函数
        elif self.type == 'mssql':
            isQuery = queryString.strip().lower()
            if isQuery.startswith('insert'):
                if L:
                    self.executeIn(queryString, L)
                else:
                    self.executeDelAndUp(queryString)
            elif isQuery.startswith('select'):
                res = self.executeSelect(queryString)
            else:
                self.executeDelAndUp(queryString)
                # print('{}执行成功'.format(queryString))
        self.commits()
        return res


