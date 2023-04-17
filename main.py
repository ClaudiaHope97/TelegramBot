import logging

from telegram.ext import Application

from handlers import start_handler, help_handler, echo_handler, memo_handler

TOKEN = "123"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""

    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(start_handler())
    application.add_handler(memo_handler())
    application.add_handler(help_handler())
    application.add_handler(echo_handler())

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == '__main__':
    main()

