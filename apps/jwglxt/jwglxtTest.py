from apps.jwglxt import jwglxtcontrols as jwglxtCon
from databaseconfig.connectdbs import connect
jwcon=connect()
jwglxtCon.jwxtBysh(con=jwcon,actionName='')
jwcon.close()