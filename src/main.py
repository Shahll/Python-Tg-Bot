from bot.bot import start, find
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, Updater
import os


def main():

    load_dotenv()
    
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("find", find))

    application.run_polling()


if __name__ == "__main__":
    main()

    