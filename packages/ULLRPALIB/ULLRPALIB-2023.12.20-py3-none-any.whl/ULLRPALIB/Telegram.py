from telegram import Bot
import asyncio

BOT_TOKKEN = '6313787889:AAFxsbrRRH_tALWOwACHY8njYkd4NYo9Uuk'


async def send_telegram_message(message,chat_id):
    # Replace 'YOUR_BOT_TOKEN' with your bot's token
    bot = Bot(token=BOT_TOKKEN)

    # Send the message
    async with bot:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

def send_message(message,chat_id):
    asyncio.run(send_telegram_message(message,chat_id))

"""
if __name__ == "__main__":
    send_message("Hello, world!")
    

"""