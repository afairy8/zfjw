import os
import time
import datetime


##cmd exp gzdx_jw_user/Likai2010@127.0.0.1:1521/orcl full=y, file=E:\\202.dmp
def getFileName(basePath, suffix):
    '''获取备份的文件名'''
    file = os.path.join(basePath, datetime.datetime.now().strftime('%Y-%m-%d') + suffix)
    return file


def bakMain(connectString, basePath, suffix='.dmp'):
    file = getFileName(basePath, suffix)
    logfile = getFileName(basePath, suffix='.log')
    if not os.path.exists(file):
        if os.path.exists(logfile):
            os.remove(logfile)
        cmd = 'exp ' + connectString + ' owner=(gzdx_jw_user)  file=' + file + ' log=' + logfile
        print(cmd)
        os.system(cmd)
        return 1
    else:
        return None


def getfileInfo(file):
    creatTime = time.strftime('%Y-%m-%d', time.gmtime(os.path.getctime(file)))
    return {'createTime': creatTime}


def pathCommon(path, type='1'):
    '''返回根目录下的子目录与文件集合{'dirs':resdirs,'files':resfiles}'''
    resdirs, resfiles = [], []
    if path:
        if type == '1':
            for root, dirs, files in os.walk(path):
                for file in files:
                    resfiles.append(os.path.join(root, file))
                for dir in dirs:
                    resdirs.append(os.path.join(root, dir))
                    # pathCommon(os.path.join(path,dir),resdirs,resfiles)
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    resfiles.append(os.path.join(path, file))
                break
            resdirs = path
        return {'dirs': resdirs, 'files': resfiles}


def clearbak(basePath, jgDays=20):
    res = '清理的备份文件有：'
    files = pathCommon(basePath)['files']
    for file in files:
        createtime = datetime.datetime.strptime(getfileInfo(file)['createTime'], '%Y-%m-%d')
        if createtime + datetime.timedelta(days=jgDays) <= \
                datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d'):
            res = res + file + '\n'
            os.remove(file)
    return res


if __name__ == '__main__':
    start = time.perf_counter()
    basePath = 'F:\\bf'
    conString='gzdx_jw_user/Gzhu2018!!@172.17.100.30:1521/gzdx'
    #'gzdx_jw_user/Likai2010@127.0.0.1:1521/orcl'
    if not os.path.exists(basePath):
        os.mkdir(basePath)
    if bakMain(basePath=basePath,connectString=conString):
        res = clearbak(basePath=basePath)
        end = time.perf_counter()
        with open(os.path.join(basePath, getFileName(basePath, suffix='.log')), 'a') as f:
            f.write(res)
            f.write('*' * 30 + '\n' + '共耗时{}秒'.format(str(end - start)))
            f.close()
    else:
        print('----')
