from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout


class PictureApp(App):
    def build(self):
        tela = BoxLayout()
        img = Image()
        img.source = 'D:\Mateus\Mega\Python\Certificado Mundo 01 Python.jpg'
        tela.add_widget(img)
        return tela


picture = PictureApp()
picture.run()
