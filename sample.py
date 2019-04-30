import psutil
up_link=psutil.net_io_counters(pernic=True)['wlan0'].bytes_sent
up_link=float(up_link/1024)
print(up_link)
