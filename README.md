# 使用技術
全部pythonでかいた

# 概要
ローカルLLMとvoicevoxを用いて，テキストベースの会話ができるChatBotを作った．

ローカルLLMのベースモデルはllama3を使用する．
Modelfileで少し調教している．

voicevoxの話者はずんだもんで設定している．

# 環境の構築

## 必要なパッケージ
- 

- 

- 

## 構築手順
- git clone 

`git clone git@github.com:Fuuya1102668/ConversationWithAI.git`

- モデルの調教

`ollama create znd -f Modelfile`

- 実行

`python3 main.py`
