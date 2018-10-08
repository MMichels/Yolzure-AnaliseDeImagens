# Src Imports
from controle.controle import Controle
from tools.filechooser import FileChooser
from tools.yolo.simple_darknet import SimpleDarknet
from threading import Thread
import cv2

# kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.texture import Texture


class Principal(BoxLayout):
    instancia = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__controle__ = Controle()
#        self.ids.campo_imagem.color.Color = (1, 1, 1, .1)

    def clk_btn_procurar(self):
        fl = FileChooser()
        self.__controle__.dir_img = fl.find_file()
        self.ids.campo_diretorio.text = \
            self.__controle__.dir_img

    def clk_btn_carregar(self):
        self.img = Imagem()
        self.img.source = self.__controle__.dir_img
        self.ids.box_img.add_widget(self.img)
        #
        # self.ids.campo_imagem.source = \
        #     self.__controle__.dir_img
        # self.ids.campo_imagem.reload()
        # self.ids.campo_imagem.color = (1, 1, 1, 1)


    def clk_btn_analizar(self):
        imagem = self.__controle__.dir_img
        cfg = 'D:\\Mateus\\Mega\\Python\\projetos\\visao\\Yolzure-AnaliseDeImagens\\src\\' \
              'tools\\yolo\\cfg\\yolov3.cfg'
        weigth = 'D:\\Mateus\\Mega\Python\\projetos\\visao\\Yolzure-AnaliseDeImagens\\src\\' \
                 'tools\\yolo\\weigths\\yolov3.weights'
        classes = 'D:\\Mateus\\Mega\\Python\\projetos\\visao\\YoloObjDetec\\classes\\yolo.txt'
        spd = SimpleDarknet(imagem, cfg, weigth, classes)
        t = Thread(target=Principal.processar_imagem, args=(self, spd))
        t.start()

    def processar_imagem(self, spd: SimpleDarknet):
        spd.run_deteccao()
        self.ids.box_img.remove_widget(self.img)
        self.img.atualizaImagem(spd.img)
        self.ids.box_img.add_widget(self.img)


class Imagem(Image):
    def build(self):
        return Image()

    def atualizaImagem(self, img):
        imagem = img  # cv2.imread image
        buf1 = cv2.flip(imagem, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(imagem.shape[1], imagem.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture1  # ends with a black image.


class Main(App):
    def build(self):
        pass


jRoot = Main()
jRoot.run()
