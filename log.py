import datetime


def write_log(text):
    now = datetime.datetime.now()
    f = open("Logs/" + now.strftime("%b-%d-%Y") + ".log", 'a')
    log = str(now) + " " + text
    f.write("{}\n".format(log))
    return


write_log("INV12521: Success")
write_log("INV10001: Error: <error message>")
