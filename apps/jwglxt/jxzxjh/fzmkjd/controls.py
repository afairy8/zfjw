from databaseconfig.connectdbs import connect
from apps.jwglxt.jxzxjh.fzmkjd import vars
import uuid
# insert into JW_JH_JXZXJHXFYQXXB
# (JXZXJHXX_ID,XFYQJD_ID,XFYQJDMC,JDKCSX,ZYFX_ID,YQZDXF,FXFYQJD_ID,px,SFMJD,KCXZDM,XDLX,JCBJ,SFZDJS,xfyqzjdgx)
def t():
    con=connect()
    njdm_id='2016'
    jxzxjhxx_id_s=con.execute(vars.getJxzxjhZyxx.format(njdm_id))
    print(jxzxjhxx_id_s)
    for jxzxjhxx_id in jxzxjhxx_id_s:
        # print(vars.getXfyqjdXx.format(jxzxjhxx_id[0]))
        fxfyqjd_id_s=con.execute(vars.getXfyqjdXx.format(jxzxjhxx_id[0]))###
        ###(xfyqjd_id,xfyqjdmc,yqzdxf,px)
        for fxfyqjd_id in fxfyqjd_id_s:
            jdlist = []
            xfyqjd_id_A=str(uuid.uuid1()).replace('-','')
            xfyqjd_id_B=str(uuid.uuid1()).replace('-','')

            xfyqjd_mc_a = '子模块A'
            xfyqjd_mc_b = fxfyqjd_id[1] + 'B'
            kcxz='16' if fxfyqjd_id[1].find('实践环节')>=0 else None
            zmk_a=(
                jxzxjhxx_id[0],xfyqjd_id_A,xfyqjd_mc_a,'1','wfx','0',fxfyqjd_id[0],int(fxfyqjd_id[3])+1,'1',kcxz,'zx','1','0','1'
            )
            zmk_b=(
                jxzxjhxx_id[0], xfyqjd_id_B, xfyqjd_mc_b, '1', 'wfx', fxfyqjd_id[2], fxfyqjd_id[0], int(fxfyqjd_id[3]) + 2, '1', kcxz,
                'zx', '1', '0', '1'
            )
            jdlist.append(zmk_a)
            jdlist.append(zmk_b)
            if jdlist:
                ##插入节点
                con.execute(vars.insertNodes,jdlist)
                ##更新课程
                con.execute(vars.upJhkc.format(xfyqjd_id_B,fxfyqjd_id[0]))
                ###更新父节点关系
                con.execute(vars.upFjdxx.format(fxfyqjd_id[0]))
                print('jxzxjhxx_id=',jxzxjhxx_id[0],'节点名称=',fxfyqjd_id[1],'子模块Aid=', xfyqjd_id_A, '新模块B=', xfyqjd_id_B)