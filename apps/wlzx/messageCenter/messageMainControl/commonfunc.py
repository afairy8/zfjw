
###

def uniZxXqOrJc(yzc):
    '''周次拼接'''
    try:
        splityzc1=yzc.split(',')
        splityzc2=[]
        splityzc=[]
        for zc in splityzc1:
            splityzc2.append(int(zc))
        splityzc.sort()
        for zc in splityzc2:
            splityzc.append(str(zc))
        rzc=''
        pos=0
        i=0
        while i <= len(splityzc)-1:
            j=i+1
            while j<=len(splityzc):
                if j<len(splityzc) and int(splityzc[j])-1==int(splityzc[j-1]):
                    pos=pos+1
                    j=j+1
                else:
                    if pos:
                        rzc=rzc+splityzc[i]+'-'+str(int(splityzc[i])+pos)+','
                    else:
                        rzc=rzc+splityzc[i]+','
                    break

            i=i+pos+1
            pos=0
        rzc=rzc[0:len(rzc)-1]
        return rzc
    except:
        return 'Error'

def zwxqj(xq=''):
    pass
    try:
        res=xq.replace('1','一').replace('2','二').replace('3','三').replace('4','四').replace('5','五').replace('6','六').replace('7','七').replace('-','至')
        return res
    except:
        return 'Error'
