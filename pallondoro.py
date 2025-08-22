#!/usr/bin/env python
import logging
import os
import re
import random
import dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

PERFECT = "Palindoro"
GOOD = [
    "Pallindoro",
    "Palinduro",
    "Polindoro",
    "Pilindoro",
    "Palindero",
    "Palindorro",
    "Polindoro",
    "Pailindoro",
    "Paldindoro",
    "Palingdoro",
    "Pallindoro",
    "Paindoro",
]
BAD = [
    "Palindromo",
    "Pallin d'oro",
    "Pollindoro",
    "Pallonzolo",
    "Palindorino",
    "Pallidoro",
    "Pallindoro",
    "Palenodoro",
    "Parindoro",
    "Pralidoro",
    "Pallindor",
    "Padrindoro",
    "Pavindoro",
    "Polindoro",
]
UGLY = [
    "Pandoro",
    "Pandolino",
    "Pangolino",
    "Poliodore",
    "Polident",
    "Poliadoro",
    "Pollo d'oro",
    "Poliedro",
    "Politono",
    "Paliandoro",
    "Polindara",
    "Paldorino",
    "Palarindor",
    "Pelinadora",
    "Pavindura",
    "Paldorina",
    "Piranodora",
    "Pallone d'oro",
]

DRUID_SHAPES = [
    "Human",
    "Baboon",
    "Badger",
    "Cat",
    "Deer",
    "Draft Horse",
    "Elk",
    "Frog",
    "Giant Badger",
    "Giant Frog",
    "Giant Rat",
    "Hyena",
    "Pandoro",
    "Panther",
    "Poisonous Snake",
    "Pollo d'oro",
    "Spider",
    "Wolf",
    "Bear"
]

dotenv.load_dotenv()
TOKEN = os.environ.get("TOKEN")


class Dice:
    def __init__(self, definition=None):
        self.dices = []
        if definition is None or len(definition) == 0:
            self.dices = [20]
            return

        temp_dices = re.split(r"\s+", definition)
        for d in temp_dices:
            match_re = re.match(r"([1-9][0-9]*)[dD]([1-9][0-9]*)", d)
            if match_re:
                dice_faces = int(match_re.group(1))
                dice_qty = int(match_re.group(2))
                if dice_qty == 0:
                    dice_qty = 1
                self.dices.extend([dice_faces] * dice_qty)

        if len(self.dices) == 0:
            self.dices = [20]

    def roll(self) -> int:
        return sum(random.randint(1, x) for x in self.dices)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


# --- Utility per rispondere nel topic corretto ---
async def reply_in_topic(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        message_thread_id=update.effective_message.message_thread_id
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.debug(f"Update chat_id: {update.effective_chat}")
    await reply_in_topic(update, context, "I'm a bot.")


def is_smagni(user):
    if user.id == 128220550:
        return False
    return user.username not in [
        "marcogh",
        "GiovanniSala",
        "giovanni_turra",
        "TheDoctor42",
    ]


async def pqualcosa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_smagni(update.effective_user):
        await reply_in_topic(update, context, "Tu quoque, mi fili?")
        return

    d = Dice("1d20")
    result = d.roll()

    if result == 20:
        message = PERFECT
    elif 19 >= result > 12:
        message = random.choice(GOOD)
    elif 12 >= result > 6:
        message = random.choice(BAD)
    else:
        message = random.choice(UGLY)

    await reply_in_topic(update, context, message)


async def wildshape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = random.choice(DRUID_SHAPES)
    await reply_in_topic(update, context, message)


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dices_request = update.effective_message.text[6:]
    d = Dice(dices_request)
    await reply_in_topic(update, context, str(d.roll()))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_in_topic(update, context, "There's no help for the wyse")


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pqualcosa", pqualcosa))
    application.add_handler(CommandHandler("roll", roll))
    application.add_handler(CommandHandler("zuccaro", wildshape))
    application.add_handler(CommandHandler("help", help))

    application.run_polling()
