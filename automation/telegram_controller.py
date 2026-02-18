# Path: automation/telegram_controller.py
import logging
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from typing import Dict, Any, Optional

class TelegramController:
    """
    LUNA-ULTRA Telegram Controller: Enables remote control via Telegram Bot.
    """
    def __init__(self, config: Dict[str, Any], controller: Any):
        self.config = config.get("telegram", {})
        self.user_config = config.get("user", {})
        self.controller = controller
        self.token = self.config.get("token")
        self.authorized_id = str(self.user_config.get("telegram_id"))
        self.enabled = self.config.get("enabled", False)
        self.application = None
        
        if self.enabled and self.token:
            try:
                self.application = Application.builder().token(self.token).build()
                self.setup_handlers()
                logging.info("TelegramController: Bot initialized.")
            except Exception as e:
                logging.error(f"TelegramController: Failed to initialize bot: {e}")

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update, context):
        user_id = str(update.effective_user.id)
        if user_id == self.authorized_id:
            await update.message.reply_text("🌙 LUNA-ULTRA Remote Access Active. Welcome back, IRFAN.")
        else:
            await update.message.reply_text("Unauthorized access attempt logged.")

    async def status_command(self, update, context):
        if str(update.effective_user.id) != self.authorized_id: return
        status = self.controller.get_status()
        msg = (
            f"📊 LUNA-ULTRA Status:\n"
            f"State: {status['state']}\n"
            f"Mode: {status['mode']}\n"
            f"Permission: {status['permission']}\n"
            f"Provider: {status['provider']}"
        )
        await update.message.reply_text(msg)

    async def handle_message(self, update, context):
        if str(update.effective_user.id) != self.authorized_id: return
        user_input = update.message.text
        await update.message.reply_text(f"Processing command: {user_input}...")
        
        # Delegate to orchestrator
        response_data = await self.controller.orchestrator.handle_task(user_input)
        
        if response_data.get("type") == "chat":
            response = response_data.get("response")
        else:
            results = response_data.get("results", [])
            if results:
                last_res = results[-1].get("result", {})
                response = f"Task completed. Output: {last_res.get('output', 'Success')}"
            else:
                response = "Action executed."
        
        await update.message.reply_text(f"🌙 LUNA: {response}")

    async def send_notification(self, message: str):
        if not self.enabled or not self.token: return
        try:
            bot = Bot(token=self.token)
            await bot.send_message(chat_id=self.authorized_id, text=f"🔔 LUNA Notification: {message}")
        except Exception as e:
            logging.error(f"TelegramController: Failed to send notification: {e}")

    async def run_bot(self):
        if self.application:
            logging.info("TelegramController: Starting bot polling...")
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            
    async def stop_bot(self):
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
