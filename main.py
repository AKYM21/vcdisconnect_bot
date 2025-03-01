#coding:UTF-8
# インストールした discord.py を読み込む
import discord
from discord.ext import commands
from time import sleep
from dotenv import load_dotenv
import os
import functools
import typing
import asyncio

# .envファイルから環境変数を読み込む
load_dotenv()

# 自分のBotのアクセストークンに置き換えてください
# .envファイルを書き換えるのをおすすめしますが、もし直接書く場合は次のようにしてください
# TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# チャンネルIDを書き換えてください
# テキストチャンネルにはBOT起動のメッセージが飛びます。
TEXT_CHANNEL_ID = "テキストチャンネルのID"
VOICE_CHANNEL_ID = "ボイスチャンネルのID"

# 接続に必要なオブジェクトを生成

Intents = discord.Intents.default()
Intents.members = True
Intents.messages = True
Intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=Intents)

# 起動時の挨拶をする
@bot.event
async def on_ready():
    # 起動したらアクティビティを変更する
    await bot.change_presence(activity=discord.Game(name='Discord'))
    # 挨拶する
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    print(channel)
    await channel.send('VC Disconnect BOTが起動しました。ｺﾝﾁﾊ!')

# ボイスチャンネルに参加した場合の通知
@bot.event
async def on_voice_state_update(user, before, after):
    if before.channel != after.channel:
        channel = bot.get_channel(TEXT_CHANNEL_ID)
        if after.channel is not None:
            await channel.send("**" + after.channel.name + "** に、__" + user.display_name + "__  が入室しました")
        else:
            await channel.send("**" + before.channel.name + "** から、__" + user.display_name + "__  が退室しました")

# ブロッキング回避処理（詳細不明）
def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

# スリープ処理
@to_thread
def blocking_func(a, b, c):
    sleep(a + b + c)

# カウントダウン処理
@bot.command()
async def countdown(ctx, arg):
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    t = int(arg)
    j = t / 60
    await channel.send(f"{int(j)}分カウントダウンします")

    for i in range( t, 0, -1):
        await blocking_func(1,0,0)
        if i == t:
            continue
        if i % 60 == 0:
            m = i / 60
            await channel.send(f"残り{int(m)}分")
        elif i % 30 == 0:
            await channel.send(f"残り{int(i)}秒")
        elif i <=10:
            if i % 5 == 0:
                await channel.send(f"残り{int(i)}秒")
        elif i <= 5:
            await channel.send(f"残り{int(i)}秒")

    await channel.send(f"終了です！5秒後切断します。")
    await blocking_func(5,0,0)
    await channel.send(f"切断します。")

    for voiceChannel in channel.guild.voice_channels:
        if voiceChannel.id == VOICE_CHANNEL_ID:
            for vcMember in voiceChannel.members:
                await vcMember.move_to(None)

# とりあえず切断する処理
@bot.command()
async def disconnect(ctx):
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    for voiceChannel in channel.guild.voice_channels:
        if voiceChannel.id == VOICE_CHANNEL_ID:
            for vcMember in voiceChannel.members:
                await vcMember.move_to(None)

if __name__ == '__main__':
    # Botの起動とDiscordサーバーへの接続
    bot.run(TOKEN)
