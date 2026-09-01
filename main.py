from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
import os

ANDROID_ENV = False
try:
    from android import AndroidService
    ANDROID_ENV = True
except ImportError:
    pass


class MainLayout(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 8
        self.padding = 16

        self.add_widget(Label(text="期货行情语音播报 V2", font_size=22))

        self.symbol_input = TextInput(text="IM", hint_text="合约代码", size_hint=(1,0.1))
        self.add_widget(self.symbol_input)

        self.interval_input = TextInput(text="2", hint_text="轮询间隔(秒)", size_hint=(1,0.1))
        self.add_widget(self.interval_input)

        self.log_label = Label(text="等待服务操作……", size_hint=(1,0.65))
        self.add_widget(self.log_label)

        self.btn_start = Button(text="启动后台播报", on_press=self.start_service, size_hint=(1,0.12))
        self.add_widget(self.btn_start)

        self.btn_stop = Button(text="停止播报", on_press=self.stop_service, size_hint=(1,0.12))
        self.add_widget(self.btn_stop)


    def start_service(self, instance):
        if not ANDROID_ENV:
            self.log_label.text = "⚠️仅APK内生效，电脑运行不会启动安卓前台服务"
            return
        AndroidService.start("Service")
        self.log_label.text = "✅前台服务已启动！不要划掉通知栏通知，可以切后台锁屏"

    def stop_service(self, instance):
        if not ANDROID_ENV:
            return
        AndroidService.stop("Service")
        self.log_label.text = "🛑后台服务已经停止"


class VoiceFutureApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    VoiceFutureApp().run()