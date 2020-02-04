import os
import time
import win32com.client as win32
import zipfile
import uuid
from common.fileAction import vars
import openpyxl as opl
from common.actionPre import actionpre
class fileInfo:
    def __init__(self, fileName):
        self.fileName = fileName
        self._defaultPath=self.setDefaultPath()#defaultPath()
    def setDefaultPath(self):
        '''默认保存路径'''
        if not os.path.exists(vars.defaultPath):
            os.mkdir(vars.defaultPath)
        return vars.defaultPath
    def isExists(self):
        path,name=os.path.split(self.fileName)
        if not name:
            sign=0
        else:
            if not path:
                path=self._defaultPath
            sign=os.path.exists(os.path.join(path,name))
        return sign

    def getFileInfo(self):
        '''文件的创建时间'''
        if self.isExists():
            creatTime = time.strftime('%Y-%m-%d', time.gmtime(os.path.getctime(self.fileName)))
            return {'createTime': creatTime}

    def removeFile(self):
        '''删除文件'''
        if self.isExists():
            os.remove(self.fileName)
            return 1

    def xlsToXlsx(self, mode='new'):
        '''从xls文件转换为xlsx文件'''
        if self.isExists() and self.fileName.lower().strip().endswith('xls'):
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            wb = excel.Workbooks.Open(self.fileName)
            if os.path.exists(self.fileName + 'x'):
                if mode.lower().strip() == 'new':
                    os.remove(self.fileName + 'x')
                    wb.SaveAs(self.fileName+'x', FileFormat=51)
                    wb.Close()
                    excel.Application.Quit()
            else:
                wb.SaveAs(self.fileName + 'x', FileFormat=51)
                wb.Close()
                excel.Application.Quit()
        else:
            pass
    def unzip(self,mode='new'):
        '''如果是压缩文件，则解压该文件'''
        if self.isExists() and zipfile.is_zipfile(self.fileName):
            zip=zipfile.ZipFile(self.fileName,'r')
            ziplist=zip.namelist()
            for z in ziplist:
                if os.path.exists(os.path.join(os.getcwd(),z)):
                    if mode=='new':
                        os.remove(os.path.join(os.getcwd(),z))
                        zip.extract(z)
                else:
                    zip.extract(z)
    def expFilename(self,suffix='.xlsx'):
        '''处理文件名
        :param filename:如果不包含路径，则默认路径，如果不指定文件名，则只用默认文件名，如果两者都不指定，那么都是默认
        :param content: 写入xls的内容，为二级嵌套格式，如[[]],或[()]
        :return:filename
        '''
        base = os.path.split(self.fileName)
        if base[0] and base[1]:
            path = base[0]
            if not base[1].endswith(suffix):
                name = base[1] + suffix
            else:
                name = base[1]
        elif base[0] and not base[1]:
            path = base[0]
            name = str(uuid.uuid1()).replace('-', '') + suffix
        elif not base[0] and base[1]:
            path = self._defaultPath
            if not base[1].endswith(suffix):
                name = base[1] + suffix
            else:
                name = base[1]
        else:
            path = self._defaultPath
            name = str(uuid.uuid1()).replace('-', '') + suffix
        pathname = os.path.join(path, name)
        return pathname
    def expXlsx(self, content=[], mode='new',suffix='.xlsx'):
        '''
        :param filename:如果不包含路径，则默认路径，如果不指定文件名，则只用默认文件名，如果两者都不指定，那么都是默认
        :param content: 写入xls的内容，为二级嵌套格式，如[[]],或[()]
        :return:filename
    '''
        xlsxFileName=self.expFilename(suffix)
        if suffix=='.xlsx':
            if os.path.exists(xlsxFileName):
                if mode=='new':
                    xlsxFileName=xlsxFileName+str(uuid.uuid1()).replace('-', '') + suffix
                    wb=opl.Workbook()
                else:
                    wb=opl.load_workbook(xlsxFileName)
            else:
                wb=opl.Workbook()
            ws=wb.active
            for data in content:
                ws.append(data)
            wb.save(xlsxFileName)
        elif suffix=='.txt':
            if os.path.exists(xlsxFileName):
                if mode=='new':
                    xlsxFileName=xlsxFileName+str(uuid.uuid1()).replace('-', '') + suffix
                    wb=open(xlsxFileName,'w',encoding='utf-8')
                else:
                    wb=open(xlsxFileName,'a',encoding='utf-8')
            else:
                wb=open(xlsxFileName,'w',encoding='utf-8')
            wb.write(';\n'.join(content))
            wb.close()
        return 1
    def removeXlsxWs(self,sheetName='Sheet1'):
        '''self本身必须是xlsx格式,且存在'''
        if self.isExists() and self.fileName.endswith('.xlsx'):
            wb=opl.load_workbook(self.fileName)
            for name in wb.get_sheet_names:
                wb.remove(name)
            wb.create_sheet(sheetName)

    def getFileContent(self,sheetName='Sheet1'):
        '''获取xlsx文件的内容,sheetName 为模糊搜索词'''
        if self.isExists():
            if self.fileName.endswith('.xlsx'):
                L=[]
                wb=opl.load_workbook(filename=self.fileName)
                wslist=wb.get_sheet_names()
                ws=None
                for sheet in wslist:
                    if sheet.lower().find(sheetName.lower())>=0:
                        ws=wb.get_sheet_by_name(sheet)
                if not ws:
                    ws=wb.active
                for row in ws.iter_rows(min_row=2,max_row=ws.max_row,min_col=1,max_col=ws.max_column):
                    rowL=[]
                    for cell in row:
                        rowL.append(cell.value)
                    L.append(tuple(rowL))
            elif self.fileName.endswith('xls'):
                pass
            else:
                pass
            return L
        else:
            return None

class pathInfo:
    '''路径类'''
    def __init__(self,path):
        self._path=path
        self._L=[]
    def isExists(self):
        return os.path.exists(self._path)
    def getFilesPath(self,path,suffix='',level=0):
        '''返回该目录下存在文件的目录集合列表'''
        if self.isExists():
            L=self._L
            dirs=os.listdir(path)
            for dir in dirs:
                dirFiles=os.path.join(path,dir)
                if os.path.isdir(dirFiles):
                    self.getFilesPath(path=dirFiles,suffix=suffix,level=level+1)
                else:
                    pathname=os.path.split(dirFiles)
                    if actionpre.unique(pathname[1].split('.')[-1]) in actionpre.actionList(suffix) and pathname[0] not in L:
                        L.append(pathname[0])
            self._L=L
            return self._L

