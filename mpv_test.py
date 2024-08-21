import mpv
import subprocess
import time

# MPVプレイヤーのインスタンスを2つ作成
player1 = mpv.MPV()
player2 = mpv.MPV()

# 動画ファイルを指定
video1 = 'dottimo.mp4'
video2 = 'kutipaku.mp4'

# 最初の動画を再生
player1.play(video1)
time.sleep(1)  # ウィンドウが生成されるまで待機

# 2つ目の動画を再生
player2.play(video2)
time.sleep(1)  # ウィンドウが生成されるまで待機

# ウィンドウIDを取得する関数
def get_window_id(window_title_part):
    result = subprocess.run(['wmctrl', '-l'], stdout=subprocess.PIPE)
    windows = result.stdout.decode('utf-8').splitlines()
    for window in windows:
        if window_title_part in window:
            return window.split()[0]
    return None

# ウィンドウを最前面に移動する関数
def activate_window(window_id):
    if window_id:
        subprocess.run(['wmctrl', '-i', '-a', window_id])

# ウィンドウIDを取得
window_id1 = get_window_id('mpv')  # 最初のmpvウィンドウ
window_id2 = get_window_id('mpv')  # 2つ目のmpvウィンドウ

if not window_id1 or not window_id2:
    print("ウィンドウIDを取得できませんでした。")
    exit()

# ウィンドウを交互に最前面に切り替える
def toggle_windows():
    while True:
        activate_window(window_id1)  # player1のウィンドウを最前面に
        time.sleep(5)  # 5秒待機
        activate_window(window_id2)  # player2のウィンドウを最前面に
        time.sleep(5)  # 5秒待機

# ウィンドウを交互に最前面に切り替える関数を実行
toggle_windows()

# 再生が終了するまで待機
player1.wait_for_playback()
player2.wait_for_playback()

