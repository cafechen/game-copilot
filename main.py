import speech_recognition as sr
from queue import Queue
import threading
from tkinter_handler import MessageWindow

# 全局停止标志
stop_flag = False

# 初始化语音识别器和音频队列
recognizer = sr.Recognizer()
audio_queue = Queue()

def capture_audio():
    """实时捕获麦克风音频流"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # 降噪处理[1](@ref)
        while not stop_flag:
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                audio_queue.put(audio)
            except sr.WaitTimeoutError:
                continue

def process_audio():
    """处理音频队列中的语音并转换为文字"""
    while not stop_flag:
        audio = audio_queue.get()
        if audio is None:
            break
        try:
            print("invoke recognize_google ...")
            text = recognizer.recognize_google(audio, language="zh-CN")
            print(f">> 识别结果：{text}")
            MessageWindow(text).show("3000")
        except sr.UnknownValueError:
            print("（无法识别语音内容）")
        except sr.RequestError:
            print("（语音服务连接失败）")

# 启动多线程
capture_thread = threading.Thread(target=capture_audio)
process_thread = threading.Thread(target=process_audio)

capture_thread.start()
process_thread.start()

# 阻塞主线程
try:
    while True:
        pass
except KeyboardInterrupt:
    print("收到中断信号，正在终止...")
    stop_flag = True
finally:
    audio_queue.put(None)
    capture_thread.join()
    print("所有资源已释放")