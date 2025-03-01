## 概要

Discordで指定した時間でボイスチャンネルにいる人を退室させるBOTです。
ボイスチャンネルのIDを指定してそのボイスチャンネル内にいる人を全員退室させます。

## つかったものたち

```
sudo apt install python-is-python3
sudo apt install python3-pip
sudo apt install python3.12-venv

pip install discord.py
pip install python-dotenv
```

## 使い方

BOTの基本設定をしてください。権限はView Channels、Send Messages、Move Menbersが最低限あれば大丈夫です。  
Systemdでも直接でもいいですが、起動させます。  
「!countdown xx」（xxは秒数）と入力するとカウントダウンが始まります。
0になると5秒後に切断します。  