from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler


def start_handler():
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends explanation on how to use the bot."""
        user = update.effective_user
        await update.message.reply_markdown_v2(
            fr'Ciao {user.mention_markdown_v2()}\!'
        )
    return CommandHandler("start", start)


def help_handler():
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text('Sono qui per aiutarti!')

    return CommandHandler("help", help_command)


def echo_handler():
    async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Echo the user message."""
        await update.message.reply_text(update.message.text)
    return MessageHandler(filters.TEXT & ~filters.COMMAND, echo)


def memo_handler():
    WHAT, WHEN, DONE = range(3)

    async def memo_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends explanation on how to use the memo."""
        await update.message.reply_text("")
    return ConversationHandler(
        entry_points=[CommandHandler("ricordami", memo_start)],
        states={
            WHAT: [
                MessageHandler(
                    filters.Regex("^(Age|Favourite colour|Number of siblings)$"), regular_choice
                ),
                MessageHandler(filters.Regex("^Something else...$"), custom_choice),
            ],
            WHEN: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice
                )
            ],
            DONE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""

    async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send the alarm message."""
        job = context.job
        await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")

    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

        text = "Timer successfully set!"
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")
