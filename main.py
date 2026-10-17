from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
from datetime import datetime

TARGET_DATE = datetime(2030, 1, 1, 0, 0, 0)

class TimerApp(App):
    def build(self):
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            PythonActivity.mActivity.getWindow().addFlags(128)

        self.state = "ALL" 
        Window.bind(on_keyboard=self.on_keyboard)

        self.root_container = BoxLayout()
        self.main_layout = BoxLayout(orientation='vertical')
        self.labels = {}
        
        metrics = ["SECS", "MINS", "HOURS", "DAYS"]
        for m in metrics:
            btn = Button(text="Loading...", font_size='40sp', background_normal='', 
                         background_color=(0,0,0,1), color=(1,1,1,1))
            btn.bind(on_release=lambda instance, metric=m: self.change_state(metric))
            self.labels[m] = btn
            self.main_layout.add_widget(btn)

        self.fullscreen_btn = Button(text="", font_size='80sp', background_normal='', 
                                     background_color=(0,0,0,1), color=(1,1,1,1), halign="center")
        self.fullscreen_btn.bind(on_release=lambda x: self.change_state("ALL"))

        self.root_container.add_widget(self.main_layout)
        Clock.schedule_interval(self.update_time, 0.1)
        return self.root_container

    def change_state(self, new_state):
        self.state = new_state
        self.root_container.clear_widgets()
        if self.state == "ALL":
            self.root_container.add_widget(self.main_layout)
        else:
            self.root_container.add_widget(self.fullscreen_btn)
        self.update_time(0)

    def update_time(self, dt):
        now = datetime.now()
        diff = TARGET_DATE - now
        total_seconds = int(diff.total_seconds())
        if total_seconds < 0: total_seconds = 0

        days = total_seconds // 86400
        hours = total_seconds // 3600
        mins = total_seconds // 60
        secs = total_seconds

        text_map = {
            "DAYS": f"{days}\nDays" if self.state != "ALL" else f"{days} Days",
            "HOURS": f"{hours}\nHours" if self.state != "ALL" else f"{hours} Hours",
            "MINS": f"{mins}\nMinutes" if self.state != "ALL" else f"{mins} Mins",
            "SECS": f"{secs}\nSeconds" if self.state != "ALL" else f"{secs} Secs",
        }

        if self.state == "ALL":
            for m in ["DAYS", "HOURS", "MINS", "SECS"]:
                self.labels[m].text = text_map[m]
        else:
            self.fullscreen_btn.text = text_map[self.state]

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if self.state != "ALL":
                self.change_state("ALL")
                return True 
            return False 
        return False

if __name__ == '__main__':
    TimerApp().run()
