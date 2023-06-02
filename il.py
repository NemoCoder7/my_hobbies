import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pytube
import instaloader
import tiktok_scraper as ts
import facebook_scraper as fs

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define your Telegram bot token
TOKEN = "6077529400:AAFebhvB4OLWMhmDeQYBmBiLSVvU-gUnRAc"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define conversation states
class DownloadStates(StatesGroup):
    PLATFORM = State()
    URL = State()

# Handler for the /start command
@dp.message_handler(Command("start"))
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("YouTube", callback_data='youtube'))
    keyboard.row(InlineKeyboardButton("Instagram", callback_data='instagram'))
    keyboard.row(InlineKeyboardButton("TikTok", callback_data='tiktok'))
    keyboard.row(InlineKeyboardButton("Facebook", callback_data='facebook'))

    await bot.send_message(message.chat.id, "Welcome to the media downloader bot! "
                            "Please select a platform:", reply_markup=keyboard)

# Handler for platform selection
@dp.callback_query_handler(lambda query: query.data in ['youtube', 'instagram', 'tiktok', 'facebook'])
async def platform_selection(query: types.CallbackQuery, state: FSMContext):
    platform = query.data
    await state.update_data(platform=platform)

    await query.message.edit_text(f"You selected {platform}. Please provide the URL:")

    await DownloadStates.URL.set()

# Handler for URL input
@dp.message_handler(state=DownloadStates.URL)
async def download(message: types.Message, state: FSMContext):
    url = message.text
    platform = (await state.get_data())['platform']

    await bot.send_message(message.chat.id, f"Downloading from {platform}...")

    if platform == 'instagram':
        try:
            loader = instaloader.Instaloader()
            loader.download_profile(url, profile_pic_only=False)
            await bot.send_message(message.chat.id, "Download complete.")
        except Exception as e:
            await bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

    elif platform == 'tiktok':
        try:
            ts.scrape(url, user_agent=None, custom_verifyfp=None, download_videos=True)
            await bot.send_message(message.chat.id, "Download complete.")
        except Exception as e:
            await bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

    elif platform == 'facebook':
        try:
            fs.download(url)
            await bot.send_message(message.chat.id, "Download complete.")
        except Exception as e:
            await bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

    elif platform == 'youtube':
        try:
            video = pytube.YouTube(url)
            video.streams.get_highest_resolution().download()
            await bot.send_message(message.chat.id, "Download complete.")
        except Exception as e:
            await bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

    await state.finish()

# Cancel the conversation
@dp.message_handler(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, "Download canceled.")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
