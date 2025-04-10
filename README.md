# 使用技術
全部pythonでかいた

# 概要
LangChainとT2Sを用いて，テキストベースの会話ができるChatBotを作った．

このシステムはmasterとslaveの2つのプログラムから成り立つ．
コンピュータ1台でも実装することができる．

# 環境の構築

## 構築手順
- git clone 
```
git clone git@github.com:Fuuya1102668/ConversationWithAI.git`
```

- 仮想環境を作る
``` shell
python3 venv vnev
source venv/bin/activate
```
---
- ipとportの指定
.envを作成してip addresとportを指定する．

- 必要なモジュールのインストール．
音声再生に用いるsimpleaudioを使うには以下をインストールする．
```
sudo apt install build-essential python3-dev libasound2-dev
```

音声録音に用いるsounddeviceを使うには以下をインストールする．
```
sudo apt install portaudio19-dev
```

python-magicを使うには以下をインストールする．
```
sudo apt-get install libmagic1
sudo apt-get install libmagic-dev
```

- モジュールのインストール
```
pip install -r requirements.txt
```

https://github.com/litagin02/Style-Bert-VITS2

を参考にモデルを構築する．

## master

```
python3 master_TCP.py
```

## slave

```
python3 slave_TCP.py
```

# RAGの使用


# 動かし方

- T2Sサーバの起動
```
python3 server_fastapi.py
```

- 実行

masterで以下を実行する．
```
python3 master_TCP.py
```

slaveで以下を実行する．

masterからsshで接続して，slave_TCP.pyを実行するのがおすすめ．
cv.pyはslaveで実行する．
```
python3 cv.py &
python3 slave_TCP.py
```

### やり残したこと
VADをつかっていい感じに会話できるようにしたけど，APIの出力が遅いため会話にストレスがある．

APIの出力をStreamにして，逐次変換することでストレスのない会話を目指す．
