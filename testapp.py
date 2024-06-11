from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.core.window import Window
import requests
import traceback

class MainApp(App):
    def build(self):
        layout = GridLayout(cols=3, spacing=10, padding=10)

        self.thumbnail_image_urls = [
            'https://raw.githubusercontent.com/AREFGURAIBAH/sscimage/main/ssc.jpg',
            'https://example.com/image2.jpg',
            'https://example.com/image3.jpg',
            'https://example.com/image4.jpg',
            'https://example.com/image5.jpg'
        ]

        self.video_player = None  # Initialize video player

        for i, image_url in enumerate(self.thumbnail_image_urls):
            if i == 0:
                thumbnail = self.load_image_from_url(image_url)
                thumbnail.bind(on_touch_down=self.open_video_player)
            else:
                thumbnail = self.load_image_from_url(image_url)
                thumbnail.bind(on_touch_down=self.open_image_viewer)
            layout.add_widget(thumbnail)

        return layout

    def load_image_from_url(self, image_url):
        response = requests.get(image_url)
        with open('temp_image.jpg', 'wb') as file:
            file.write(response.content)
        return Image(source='temp_image.jpg', size_hint=(0.2, 0.2), allow_stretch=True, keep_ratio=False)

    def open_video_player(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if self.video_player is None:
                try:
                    self.video_player = Video(source='https://example.com/video.m3u8', size_hint=(None, None), size=(800, 600))
                    self.video_player.bind(on_error=self.on_video_error)
                    self.video_player.state = 'play'
                    self.root.add_widget(self.video_player)
                    Clock.schedule_interval(self.check_video_state, 0.1)
                except Exception as e:
                    print(f"Error opening video player: {e}")
                    traceback.print_exc()
                    self.close_video_player()
            else:
                self.video_player.state = 'play'

    def on_video_error(self, instance, error_message):
        print(f"Video player error: {error_message}")
        self.close_video_player()

    def close_video_player(self):
        if self.video_player is not None:
            self.root.remove_widget(self.video_player)
            self.video_player = None

    def open_image_viewer(self, instance, touch):
        if instance.collide_point(*touch.pos):
            image_viewer = Image(source=instance.source, size_hint=(None, None), size=(800, 600))
            self.root.add_widget(image_viewer)

    def check_video_state(self, dt):
        if self.video_player is not None and self.video_player.state == 'stop':
            self.close_video_player()

if __name__ == '__main__':
    Window.size = (1024, 768)  # Set the window size
    MainApp().run()
