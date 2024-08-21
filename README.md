# 使用技術
全部pythonでかいた

# 概要
ローカルLLMとvoicevoxを用いて，テキストベースの会話ができるChatBotを作った．

ローカルLLMのベースモデルはllama3を使用する．
Modelfileで少し調教している．

voicevoxの話者はずんだもんで設定している．

# 環境の構築

## 構築手順
- git clone 

```
git clone git@github.com:Fuuya1102668/ConversationWithAI.git`
```

- 仮想環境を作る

```
python3 venv vnev
source venv/bin/activate
``` 

- モジュールのインストール
```
pip install -r requirements.txt
```

動画再生に用いているmpvを使うにはlibmpv-devをインストールする必要がある．

```
sudo apt install libmpv-dev
```

音声再生に用いるsimpleaudioを使うには以下をインストールする．

```
sudo apt install build-essential python3-dev libasound2-dev
```

音声録音に用いるsounddeviceを使うには以下をインストールする．

```
sudo apt install portaudio19-dev
```

- サーバの起動

```
o;asnboan:
```

- 実行

```
python3 character_langchain_RAG_PDF.py
```

