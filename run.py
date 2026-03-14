from app.bot import application
import os
from app.config import TELEGRAM_TOKEN, WEBHOOK_URL
from app import create_app

if __name__ == "__main__":
    USE_POLLING = os.getenv("USE_POLLING", "1") == "1"

    if USE_POLLING:
        print("🔹 Starting bot in polling mode...")
        application.run_polling()
    else:
        print("🔹 Starting Flask + webhook mode...")
        app = create_app()

        # application.run_webhook(
        #     listen="0.0.0.0",
        #     port=5000,
        #     webhook_url=WEBHOOK_URL,
        #     url_path=f"/{TELEGRAM_TOKEN}",
        #     drop_pending_updates=True,
        # )

        app.run(host="127.0.0.1", port=5000, debug=True)
