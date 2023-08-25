import os
import time
from discord_webhook import DiscordWebhook
import psutil

webhook = DiscordWebhook(
    url='')

while True:
    load1, load5, load15 = psutil.getloadavg()

    cpu_usage = (load15 / os.cpu_count()) * 100
    ram_usage = psutil.virtual_memory()[2]
    webhook.content = f"---------- \n CPU Usage: {round(cpu_usage)}% \n Ram Usage: {round(ram_usage)}% \n"
    print(f"CPU Usage: {round(cpu_usage)}% \n Ram Usage: {round(ram_usage)}%")
    webhook.execute()
    time.sleep(300)
