from jsslib import JSS

jss = JSS()

jss.Initialize('../../../data/jss/lang/table/table.lst')
print(jss.RunSql("SELECT TOP 10 id, Zi FROM zi WHERE PinYin = 'ding1' and id > 2;"))

jss.Terminate()

