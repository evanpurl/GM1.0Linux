import os
import time
from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/960753448469540904/BfECmeWQaOnkPuPb437hZRKYd6y1r0dEh9_vLRaAIwgF5gtO5avK8NHC--r7AJ6-skVB',
    content='Ping')

while True:
    webhook.execute()
    time.sleep(14400)
