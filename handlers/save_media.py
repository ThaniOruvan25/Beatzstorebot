# (c) @AbirHasan2005

import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64


async def forward_to_channel(bot: Client, message: Message, editable: Message):
    try:
        __SENT = await message.forward(Config.DB_CHANNEL)
        return __SENT
    except FloodWait as sl:
        if sl.value > 45:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#FloodWait #{str(editable.chat.id)}:\nGot FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                    ]
                )
            )
        return await forward_to_channel(bot, message, editable)


async def save_batch_media_in_channel(bot: Client, editable: Message, message_ids: list):
    try:
        message_ids_str = ""
        for message in (await bot.get_messages(chat_id=editable.chat.id, message_ids=message_ids)):
            sent_message = await forward_to_channel(bot, message, editable)
            if sent_message is None:
                continue
            message_ids_str += f"{str(sent_message.id)} "
            await asyncio.sleep(1)
        SaveMessage = await bot.send_message(
            chat_id=Config.DB_CHANNEL,
            text=message_ids_str,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Delete Batch", callback_data="closeMessage")
            ]])
        )
        share_link = f"https://telegram.dog/{Config.BOT_USERNAME}?start=ViralBeatz_{str_to_b64(str(SaveMessage.id))}"
        await editable.edit(
            f"**Your Files Saved in Batch**\n\n Link: <code>{share_link}<\code>\n\n"
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Lɪɴᴋ", url=share_link)]])
            disable_web_page_preview=True
        )
        await bot.send_message(
            chat_id=int(Config.DB_CHANNEL),
            text=f"#NewBatch #{editable.reply_to_message.from_user.first_name} #{editable.reply_to_message.from_user.id}\n\n[{editable.reply_to_message.from_user.first_name}](tg://user?id={editable.reply_to_message.from_user.first_name}) Got Batch Link!",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=share_link)]])
        )
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text=f"#NewBatch #{editable.reply_to_message.from_user.first_name} #{editable.reply_to_message.from_user.id}\n\n[{editable.reply_to_message.from_user.first_name}](tg://user?id={editable.reply_to_message.from_user.first_name}) Got Batch Link!",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=share_link)]])
        )
    except Exception as err:
        await editable.edit(f"#Error - Something Went Wrong!\n\n**Error:** `{err}`")
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text ="**Forwarding This Error Message to Admin.",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Continue ✅", callback_data="continue"),
                        InlineKeyboardButton("Cancel ✖️", callback_data="close_data")
                    ]
                ]
            )
        )


async def save_media_in_channel(bot: Client, editable: Message, message: Message):
    try:
        forwarded_msg = await message.forward(Config.DB_CHANNEL)
        file_er_id = str(forwarded_msg.id)
        await forwarded_msg.reply_text(
            f"#NewFile #{message.from_user.first_name} #{message.from_user.id} :\n\n[{message.from_user.first_name}](tg://user?id={message.from_user.id}) Got File Link!",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=share_link)]])
        )
        share_link = f"https://telegram.dog/{Config.BOT_USERNAME}?start=ViralBeatz_{str_to_b64(file_er_id)}"
        await editable.edit(
            f"**Your File Saved**\n\n"
            f"Link:<code>{share_link}</code> \n\n",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Lɪɴᴋ", url=share_link)]])
            disable_web_page_preview=True
        )
    except FloodWait as sl:
        if sl.value > 45:
            print(f"Sleep of {sl.value}s caused by FloodWait ...")
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text="#FloodWait #{str(editable.chat.id)}:\n"
                     f"Got FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}`!!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                    ]
                )
            )
        await save_media_in_channel(bot, editable, message)
    except Exception as err:
        await editable.edit(f"Something Went Wrong!\n\n**Error:** `{err}`")
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text="#Error #{str(editable.chat.id)}:\n"
                 f"Got Error from `{str(editable.chat.id)}`!!\n\n"
                 f"**Traceback:** `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Ban User", callback_data=f"ban_user_{str(editable.chat.id)}")]
                ]
            )
        )
        await bot.send_message(
            chat_id=editable.from_user.id,
            text ="**Forwarding This Error Message to Admin.**",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Continue ✅", callback_data="continue"),
                        InlineKeyboardButton("Cancel ✖️", callback_data="close_data")
                    ]
                ]
            )
        )
