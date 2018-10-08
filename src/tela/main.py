# Src Imports
from kivy.uix.label import Label

from controle.controle import Controle
from tools.filechooser import FileChooser
from tools.yolo.simple_darknet import SimpleDarknet
from threading import Thread
import cv2

# kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock


class Principal(BoxLayout):
    instancia = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spd = SimpleDarknet()
        self.__controle__ = Controle()
        self.timer = Clock
        self.timer.schedule_interval(self.verificar_processamento, 1.0)
        #self.ids.campo_imagem.color.Color = (1, 1, 1, .1)

    def clk_btn_procurar(self):
        fl = FileChooser()
        self.__controle__.dir_img = fl.find_file()
        self.ids.campo_diretorio.text = \
            self.__controle__.dir_img

    def clk_btn_carregar(self):
        self.ids.campo_imagem.texture = None
        self.ids.campo_imagem.source = \
             self.__controle__.dir_img
        self.ids.campo_imagem.color = (1, 1, 1, 1)
        self.ids.campo_imagem.reload()

    def clk_btn_analizar(self):
        imagem = self.__controle__.dir_img
        cfg = 'D:\\Mateus\\Mega\\Python\\projetos\\visao\\Yolzure-AnaliseDeImagens\\src\\' \
              'tools\\yolo\\cfg\\yolov3.cfg'
        weigth = 'D:\\Mateus\\Mega\Python\\projetos\\visao\\Yolzure-AnaliseDeImagens\\src\\' \
                 'tools\\yolo\\weigths\\yolov3.weights'
        classes = 'D:\\Mateus\\Mega\\Python\\projetos\\visao\\YoloObjDetec\\classes\\yolo.txt'
        self.spd = SimpleDarknet(imagem, cfg, weigth, classes)
        self.spd.taxa_min = .5
        t = Thread(target=Principal.processar_imagem, args=self)
        t.start()
        box_temp = self.ids.box_btns_img
        self.ids.box_img.remove_widget(self.ids.box_btns_img)
        self.ids.box_img.add_widget(Label(text='Analizando, Aguarde...', id='lblAguarde',
                                          size_hint=(1, .05)))
        self.ids.box_img.add_widget(box_temp)
        del box_temp

    def clk_btn_limpar(self):
        self.ids.campo_imagem.source = ''
        self.ids.campo_imagem.reload()

    def processar_imagem(self):
        self.spd.run_deteccao()

    def verificar_processamento(self, dt):
        if len(self.spd.img) > 1 is not None:
            if not self.spd.isRunning:
                    self.atualiza_imagem()
                    self.spd = SimpleDarknet()

    def atualiza_imagem(self):
        try:
            imagem = self.spd.img
            buf1 = cv2.flip(imagem, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(imagem.shape[1], imagem.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.campo_imagem.texture = texture1
            # Remoção do widget de loading.
            lista = self.ids.box_img.children
            for widget in lista:
                if isinstance(widget, Label):
                    if widget.id is 'lblAguarde':
                        self.ids.box_img.remove_widget(widget)


        except AttributeError:
            pass


class Main(App):
    def build(self):
        self.title = "YolZure - Analise de Imagens"
        pass


jRoot = Main()
jRoot.run()
