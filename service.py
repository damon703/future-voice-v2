from android import AndroidService
from android import tts
import requests
import time
import datetime

# =========配置区，UI会覆盖，这里是默认值========
POLL_INTERVAL = 2
SYMBOL = "IM"
MAX_RETRY_SLEEP = 8
# ==============================================

def speak(text):
    try:
        tts.speak(text)
    except Exception as e:
        print(f"[TTS_ERR] {e}")


def write_log(msg):
    t = datetime.datetime.now().strftime("%Y‑%m‑%d %H:%M:%S")
    line = f"[{t}] {msg}\n"
    print(line)
    try:
        with open("/sdcard/future_voice_log.txt","a",encoding="utf‑8") as f:
            f.write(line)
    except Exception:
        pass


def get_price():
    # =========【必须替换为你的行情接口】=========
    url = "填入行情接口地址"
    resp = requests.get(url, timeout=6)
    j = resp.json()
    return j["last"]


def service_loop():
    write_log(f"服务启动，监听合约:{SYMBOL}，轮询:{POLL_INTERVAL}s")
    speak(f"开始监听 {SYMBOL}")
    error_sleep = 1

    while True:
        try:
            price = get_price()
            write_log(f"当前价格 {price}")

            # ----------------在这里写你的播报触发逻辑----------------
            # example: if price > x: speak("价格到达"+str(price))

            error_sleep = 1
            time.sleep(POLL_INTERVAL)

        except Exception as err:
            write_log(f"循环异常:{err}")
            error_sleep = min(error_sleep*2, MAX_RETRY_SLEEP)
            time.sleep(error_sleep)


# 创建高优先级前台服务
service = AndroidService("Service")
# 设置前台通知，提高保活优先级
service.set_foreground(
    title="期货行情播报",
    message="后台监听行情，请勿清除通知",
    notification_priority="high"
)

if __name__ == "__main__":
    try:
        service_loop()
    except Exception as fatal:
        write_log(f"服务致命异常 {fatal}")
        speak("播报服务异常退出")
    finally:
        service.stop()