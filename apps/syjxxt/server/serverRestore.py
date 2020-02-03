import os
sourcePath='D:\\local'
dbStorePath='D:\\LIP\\LIP_DATA'
restoreCode='''
restore database {} from disk='{}'
with replace,
move '{}' to '{}',
move '{}_log' to '{}'
'''
filelist=os.listdir(sourcePath)
for file in filelist:
    L=[]
    dbs=('lip_assets','lip_baseinfo','lip_custom','lip_teaching')
    files=os.listdir(sourcePath)
    for file in files:
        fi=file.strip().lower()
        for db in dbs:
            if fi.find(db)>=0:
                restorCode=restoreCode.format(
                    db,
                    os.path.join(sourcePath,file),
                    db,
                    os.path.join(dbStorePath,db)+'.mdf',
                    db,
                    os.path.join(dbStorePath, db) + '.ldf',
                )
                L.append(restorCode)
    ####�����ָ��ű��ļ�####
    if os.path.exists(os.path.join(os.getcwd(),'serverresore.sql')):
        os.remove(os.path.join(os.getcwd(),'serverresore.sql'))
    f=open(os.path.join(os.getcwd(),'serverresore.sql'),'w')
    f.write(';\n'.join(L))
    # f.write(addlink+'\n'+readJgZyBjXj+'\n'+insertbj)
    f.close()