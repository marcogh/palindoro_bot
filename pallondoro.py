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
    MessageHandler,
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
]

dotenv.load_dotenv()
TOKEN = os.environ.get("TOKEN")


class Dice:
    # dices: list[int] = []

    def __init__(self, definition=None):
        self.dices = []

        if definition is None or len(definition) == 0:
            self.dices = [20]
            return

        temp_dices = re.split(r"\s+", definition)
        for d in temp_dices:
            match_re = re.match(r"([1-9][0-9]*)[dD]([1-9][0-9]*)", d)
            if match_re:
                this_dices = [int(match_re.group(2))] * int(match_re.group(1))
                self.dices.extend(this_dices)

    def roll(self) -> int:
        return sum(map(lambda x: random.randint(1, x), self.dices))


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.debug(f"Update chat_it: {update.effective_chat}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot.")


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
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Tu quoque, mi fili?"
        )
        return

    d = Dice("1d20")
    result = d.roll()

    if result == 20:
        message = PERFECT
    if 19 >= result > 12:
        message = random.choice(GOOD)
    if 12 >= result > 6:
        message = random.choice(BAD)
    else:
        message = random.choice(UGLY)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dices_request = update.effective_message.text[6:]
    d = Dice(dices_request)
    # logging.debug(f"Update: {update}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(d.roll()))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="There's no help for the wyse"
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    pqualcosa_handler = CommandHandler("pqualcosa", pqualcosa)
    application.add_handler(pqualcosa_handler)

    roll_handler = CommandHandler("roll", roll)
    application.add_handler(roll_handler)

    help_handler = CommandHandler("help", help)
    application.add_handler(help_handler)

    application.run_polling()
