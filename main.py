import os
import re
import sys
import json
import time
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
import datetime
from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
from core import download_and_send_video
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait, StickerEmojiInvalid

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Environment variables for API credentials
API_ID = os.environ.get("API_ID", "24495656")
API_HASH = os.environ.get("API_HASH", "61afcf68c6429714dd18acd07f246571")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7842202956:AAHgKbWG5FSQhRdcovXmqaEYlPMd-dQu630")

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/sanjaykagra86"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/SSC_Aspirants_7"),
        ],
        [
            InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/SSC_Aspirants_7"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://i.ibb.co/dpRKmmj/file-3957.jpg",
    "https://i.ibb.co/NSbPQ5n/file-3956.jpg",
    "https://i.ibb.co/Z8R4z0g/file-3962.jpg",
    "https://i.ibb.co/LtqjVy7/file-3958.jpg",
    "https://i.ibb.co/bm20zfd/file-3959.jpg",
    "https://i.ibb.co/0V0BngV/file-3960.jpg",
    "https://i.ibb.co/rQMXQjX/file-3961.jpg",
]

# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    loading_message = await bot.send_message(chat_id=message.chat.id, text="Loading... ⏳🔄")
    random_image_url = random.choice(image_urls)
    caption = (
        "**𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫 👋!**\n\n"
        "➠ **𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ♥️**\n"
        "➠ **Can Extract Videos & PDFs From Your Text File and Upload to Telegram!**\n"
        "➠ **For Guide Use Command /guide 📖**\n\n"
        "➠ **Use /moni Command to Download From TXT File** 📄\n\n"
        "➠ **𝐌𝐚𝐝𝐞 𝐁𝐲:** @SanjayKagra86🩷"
    )
    await bot.send_photo(chat_id=message.chat.id, photo=random_image_url, caption=caption, reply_markup=keyboard)
    await loading_message.delete()

# Cookies file path
COOKIES_FILE_PATH = "youtube_cookies.txt"

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, message: Message):
    await message.reply_text("Please upload the cookies file (.txt format).", quote=True)
    try:
        input_message: Message = await client.listen(message.chat.id)
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await message.reply_text("Invalid file type. Please upload a .txt file.")
            return
        downloaded_path = await input_message.download()
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()
        with open(COOKIES_FILE_PATH, "w") as target_file:
            target_file.write(cookies_content)
        await input_message.reply_text("✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`.")
    except Exception as e:
        await message.reply_text(f"⚠️ An error occurred: {str(e)}")

# File paths
SUBSCRIPTION_FILE = "subscription_data.txt"
CHANNELS_FILE = "channels_data.json"
YOUR_ADMIN_ID = 5548106944

def read_subscription_data():
    if not os.path.exists(SUBSCRIPTION_FILE):
        return []
    with open(SUBSCRIPTION_FILE, "r") as f:
        return [line.strip().split(",") for line in f.readlines()]

def read_channels_data():
    if not os.path.exists(CHANNELS_FILE):
        return []
    with open(CHANNELS_FILE, "r") as f:
        return json.load(f)

def write_subscription_data(data):
    with open(SUBSCRIPTION_FILE, "w") as f:
        for user in data:
            f.write(",".join(user) + "\n")

def write_channels_data(data):
    with open(CHANNELS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def is_admin(user_id):
    return user_id == YOUR_ADMIN_ID

@bot.on_message(filters.command("guide"))
async def guide_handler(client: Client, message: Message):
    guide_text = (
        "🔑 **How to get started with Premium**:\n\n"
        "1. **First of all**, contact the owner and buy a premium plan. 💰\n"
        "2. **If you are a premium user**, you can check your plan by using `/myplan`. 🔍\n\n"
        "📖 **Usage**:\n\n"
        "1. `/add_channel -100{channel_id}` - Add a channel to the bot.\n"
        "2. `/remove_channel -100{channel_id}` - Remove a channel from the bot.\n"
        "3. `/moni .txt` file command - Process the .txt file.\n"
        "4. `/stop` - Stop the task running in the bot. 🚫\n\n"
        "If you have any questions, feel free to ask! 💬"
    )
    await message.reply_text(guide_text)

@bot.on_message(filters.command("adduser") & filters.private)
@admin_only
async def add_user(client, message: Message):
    try:
        _, user_id, expiration_date = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data.append([user_id, expiration_date])
        write_subscription_data(subscription_data)
        await message.reply_text(f"User {user_id} added with expiration date {expiration_date}.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /adduser <user_id> <expiration_date>")

@bot.on_message(filters.command("removeuser") & filters.private)
@admin_only
async def remove_user(client, message: Message):
    try:
        _, user_id = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data = [user for user in subscription_data if user[0] != user_id]
        write_subscription_data(subscription_data)
        await message.reply_text(f"User {user_id} removed.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /removeuser <user_id>")

@bot.on_message(filters.command("users") & filters.private)
async def show_users(client, message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return
    subscription_data = read_subscription_data()
    if subscription_data:
        users_list = "\n".join([f"{idx + 1}. User ID: `{user[0]}`, Expiration Date: `{user[1]}`" for idx, user in enumerate(subscription_data)])
        await message.reply_text(f"**👥 Current Subscribed Users:**\n\n{users_list}")
    else:
        await message.reply_text("ℹ️ No users found in the subscription data.")

@bot.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()
    if user_id == str(YOUR_ADMIN_ID):
        await message.reply_text("**✨ You have permanent access!**")
    elif any(user[0] == user_id for user in subscription_data):
        expiration_date = next(user[1] for user in subscription_data if user[0] == user_id)
        await message.reply_text(f"**📅 Your Premium Plan Status**\n\n**🆔 User ID**: `{user_id}`\n**⏳ Expiration Date**: `{expiration_date}`\n**🔒 Status**: *Active*")
    else:
        await message.reply_text("**❌ You are not a premium user.**")

@bot.on_message(filters.command("add_channel"))
async def add_channel(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()
    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text("You are not a premium user.")
        return
    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id not in channels:
            channels.append(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"Channel {channel_id} added.")
        else:
            await message.reply_text(f"Channel {channel_id} is already added.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /add_channel <channel_id>")

@bot.on_message(filters.command("remove_channel"))
async def remove_channel(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()
    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text("You are not a premium user.")
        return
    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id in channels:
            channels.remove(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"Channel {channel_id} removed.")
        else:
            await message.reply_text(f"Channel {channel_id} is not in the list.")
    except ValueError:
        await message.reply_text("Invalid command format. Use: /remove_channels <channel_id>")

@bot.on_message(filters.command("allowed_channels"))
async def allowed_channels(client, message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return
    channels = read_channels_data()
    if channels:
        channels_list = "\n".join([f"- {channel}" for channel in channels])
        await message.reply_text(f"**📋 Allowed Channels:**\n\n{channels_list}")
    else:
        await message.reply_text("ℹ️ No channels are currently allowed.")

@bot.on_message(filters.command("remove_all_channels"))
async def remove_all_channels(client, message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return
    write_channels_data([])
    await message.reply_text("✅ **All channels have been removed successfully.**")

@bot.on_message(filters.command("stop"))
async def stop_handler(client, message: Message):
    if message.chat.type == "private":
        user_id = str(message.from_user.id)
        subscription_data = read_subscription_data()
        if not any(user[0] == user_id for user in subscription_data):
            await message.reply_text("😔 You are not a premium user. Please subscribe to get access! 🔒")
            return
    else:
        channels = read_channels_data()
        if str(message.chat.id) not in channels:
            await message.reply_text("🚫 You are not a premium user. Subscribe to unlock all features! ✨")
            return
    await message.reply_text("♦️ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 ♦️", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("moni"))
async def moni_handler(client: Client, message: Message):
    if message.chat.type == "private":
        user_id = str(message.from_user.id)
        subscription_data = read_subscription_data()
        if not any(user[0] == user_id for user in subscription_data):
            await message.reply_text("❌ You are not a premium user. Please upgrade your subscription! 💎")
            return
    else:
        channels = read_channels_data()
        if str(message.chat.id) not in channels:
            await message.reply_text("❗ You are not a premium user. Subscribe now for exclusive access! 🚀")
            return
    editable = await message.reply_text('𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐇𝐞𝐫𝐞 ⏍')
    try:
        input: Message = await client.listen(editable.chat.id)
        if not input.document or not input.document.file_name.endswith('.txt'):
            await message.reply_text("Please send a valid .txt file.")
            return
        x = await input.download()
        await input.delete(True)
        path = f"./downloads/{message.chat.id}"
        file_name = os.path.splitext(os.path.basename(x))[0]
        with open(x, "r") as f:
            content = f.read().strip()
        lines = content.splitlines()
        links = []
        for line in lines:
            line = line.strip()
            if line:
                link = line.split("://", 1)
                if len(link) > 1:
                    links.append(link)
        os.remove(x)
        print(len(links))
    except:
        await message.reply_text("∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.")
        if os.path.exists(x):
            os.remove(x)
    await editable.edit(f"∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 𝐀𝐫𝐞 🔗** **{len(links)}**\n\n𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐈𝐧𝐢𝐭𝐢𝐚𝐥 𝐢𝐬 **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    await editable.edit("**Enter Batch Name or send d for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0
    await editable.edit("∝ 𝐄𝐧𝐭𝐞𝐫 𝐑𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧 🎬\n☞ 144,240,360,480,720,1080\nPlease Choose Quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080"
        else:
            res = "UN"
    except Exception:
        res = "UN"
    await editable.edit("**Enter Your Name or send `de` for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    credit = "️ ⁪⁬⁮⁮⁮"
    if raw_text3
