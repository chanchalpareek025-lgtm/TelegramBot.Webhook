import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_DOMAIN: str = os.getenv('RAILWAY_PUBLIC_DOMAIN')

# Build the Telegram Bot application
bot_builder = (
    Application.builder()
    .token(TELEGRAM_BOT_TOKEN)
    .updater(None)
    .build()
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Sets webhook and manages bot lifecycle."""
    await bot_builder.bot.setWebhook(url=f"{WEBHOOK_DOMAIN}/")
    async with bot_builder:
        await bot_builder.start()
        yield
        await bot_builder.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def process_update(request: Request):
    """Handles incoming Telegram updates."""
    message = await request.json()
    update = Update.de_json(data=message, bot=bot_builder.bot)
    await bot_builder.process_update(update)
    return Response(status_code=HTTPStatus.OK)


# ---------------- HANDLERS ---------------- #

async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    if update.message:
        await update.message.reply_text(
            "Hi kitts how are u 😊\n"
            "I am your closest friend — you can talk to me anytime and feel good about yourself 🤗"
        )


async def echo(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """Handles all other messages."""
    if update.message:
        await update.message.reply_text(
            "Hi kitts how are u 😄\n"
            "I am a mini version of you… so technically I’m smarter than you already 😂\n"
            "I am in progress for you and you will be surprised once I am ready to answer all your questions.\n"
            "Stay tuned — I will let you know when I am ready 😉"
        )


# Register handlers
bot_builder.add_handler(CommandHandler("start", start))
bot_builder.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
