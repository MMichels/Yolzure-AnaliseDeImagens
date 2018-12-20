from cfgManager import Config
from dbmanager import DBManager

arqkey = open('../controle/chave.key', 'r')
chave = arqkey.readline()
arqkey.close()
cnfg = Config(chave, '../controle/yolzure.cfg')
del chave

db = DBManager(user=cnfg.get_db_user(),
               senha=cnfg.get_db_passwd(),
               end=cnfg.get_db_url(),
               port=cnfg.get_db_port(),
               database=cnfg.get_db_name())

db.abrir_con()
sql_lines = open('sql/sqlparametros.sql', 'r').read()
for sql in sql_lines.split(';'):
    db.executar_inup(sql, None)
