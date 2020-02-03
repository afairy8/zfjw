from apps.jyxt.pyfa import controls


def jyxt(con,actionName=''):
    '''
    :param con:
    :param actionName:if actionName='pyfa' then sys rcpyfa,if actionName='jxdg' then sys jxdg
    :return:
    '''
    return controls.jyxtInterface(con, actionName)