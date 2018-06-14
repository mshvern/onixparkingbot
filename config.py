import telepot
from const import bot_token, bot_url

bot = telepot.Bot(bot_token)

secret = "/bot" + bot_token

bot.setWebhook(bot_url + secret)
print("Webhook set!")
