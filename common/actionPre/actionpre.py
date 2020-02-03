
def unique(actionName):
    '''返回actionName去除空格后的小写'''
    return actionName.strip().replace('\n','').lower()

def actionList(actionName,defaultSeq=';'):
    actionName=unique(actionName)
    return actionName.split(defaultSeq)