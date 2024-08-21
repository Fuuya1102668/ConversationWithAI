import cv2

# 動画ファイルのパス
video1 = "kutipaku.mp4"
video2 = "dottimo.mp4"

# ウィンドウの名前
window_name1 = 'Video 1'
window_name2 = 'Video 2'

def display_video(video_path, window_name):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(window_name, frame)
        # 固定値でフレームの遅延を設定
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyWindow(window_name)

# 動画を順次再生
display_video(video1, window_name1)
display_video(video2, window_name2)

print("Both videos have finished playing.")
