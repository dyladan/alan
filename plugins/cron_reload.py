import time
event = "CRON"
def cron(con):
	time.sleep(15)
	con.ldplugins(con.plugdir)
	return
