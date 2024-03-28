import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Simply send /find followed by the name of the book you're searching for")


async def menu(book, update: Update, context: ContextTypes.DEFAULT_TYPE):

    preview_link = book["volumeInfo"]["previewLink"]
    title = book["volumeInfo"]["title"] 
    authors = ", ".join(book["volumeInfo"]["authors"])
    pages = book["volumeInfo"]["pageCount"]
    categories = ", ".join(book["volumeInfo"]["categories"])
    language = book["volumeInfo"]["language"]
    isbn = book["volumeInfo"]["industryIdentifiers"][1]["identifier"]
    volume_info = book["volumeInfo"]["infoLink"]

    keyboard = [
        [InlineKeyboardButton("Read pdf", url=preview_link if preview_link else "")],
        [InlineKeyboardButton("Info", url=volume_info if volume_info else "")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    

    caption = f"*Title:* {title}\n"
    caption += f"*Author:* {authors}\n" if authors else ""
    caption += f"*Pages:* {pages}\n" if pages else ""
    caption += f"*Categories:* {categories}\n" if categories else ""
    caption += f"*Language:* {language}\n" if language else ""
    caption += f"`ISBN:` {isbn}\n" if isbn else ""



    await update.message.reply_photo(
        photo=preview_link, 
        caption=caption, 
        reply_markup=reply_markup, parse_mode="Markdown")


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    message = update.message
    if len(message.text) < 6:
        await update.message.reply_text("You didn't enter the name of the book")
    else:
        url = f'https://www.googleapis.com/books/v1/volumes?q={message.text.split(maxsplit=1)[1]}'
        response = requests.get(url)
        if response.status_code == 200:

            data = response.json()
            
            if 'items' in data:
                first_book = data['items'][0]
                await menu(first_book, update, context)
            else:
                await update.message.reply_text("We couldn't find your book")
        else:
            await update.message.reply_text("We couldn't connect to the server, try one more time later")

    
