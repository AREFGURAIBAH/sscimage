from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
import requests

class ImageViewer(ModalView):
    def __init__(self, image_source, **kwargs):
        super(ImageViewer, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.8)
        self.image = Image(source=image_source)
        self.add_widget(self.image)

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

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
        return Image(source='temp_image.jpg', allow_stretch=True, keep_ratio=False)

    def open_image_viewer(self, instance, touch):
        if instance.collide_point(*touch.pos):
            image_viewer = ImageViewer(image_source=instance.source)
            image_viewer.open()

if __name__ == '__main__':
    MainApp().run()