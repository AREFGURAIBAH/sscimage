from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
import requests

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

        for image_url in self.thumbnail_image_urls:
            thumbnail = self.load_image_from_url(image_url)
            thumbnail.bind(on_touch_down=self.open_image_viewer)
            layout.add_widget(thumbnail)

        return layout

    def load_image_from_url(self, image_url):
        response = requests.get(image_url)
        with open('temp_image.jpg', 'wb') as file:
            file.write(response.content)
        return Image(source='temp_image.jpg', size_hint=(0.2, 0.2), allow_stretch=True, keep_ratio=False)

    def open_image_viewer(self, instance, touch):
        if instance.collide_point(*touch.pos):
            image_viewer = Image(source=instance.source, size_hint=(None, None), size=(800, 600))
            self.root.add_widget(image_viewer)

if __name__ == '__main__':
    MainApp().run()
