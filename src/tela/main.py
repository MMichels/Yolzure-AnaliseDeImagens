# Src Imports
from controle.controle import Controle
from tools.filechooser import FileChooser
from tools.yolo.simple_darknet import SimpleDarknet
from tools.azure.visio.complete_visio_request import CompleteVisioRequest
from threading import Thread
import cv2

# kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.clock import Clock


class Principal(BoxLayout):
    instancia = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controle = Controle()
        self.timer = Clock
        self.timer.schedule_interval(self.verificar_processamento, 1.0)

    def clk_btn_procurar(self):
        fl = FileChooser()
        self.controle.dir_img = fl.find_file()
        self.ids.campo_diretorio.text = \
            self.controle.dir_img
        self.get_parent_window()

    def clk_btn_carregar(self):
        self.ids.campo_imagem.texture = None
        self.ids.campo_imagem.source = self.controle.dir_img
        self.ids.campo_imagem.color = (1, 1, 1, 1)
        self.ids.campo_imagem.reload()

    def clk_btn_analizar(self):
        if not self.controle.darknet.isRunning:
            box_temp = self.ids.box_btns_img
            self.ids.box_img.remove_widget(self.ids.box_btns_img)
            self.ids.box_img.add_widget(Label(text='Analizando, Aguarde...', id='lblAguarde',
                                              size_hint=(1, .05)))
            self.ids.box_img.add_widget(box_temp)
            self.processar_imagem()

    def clk_btn_limpar(self):
        self.ids.campo_imagem.source = ''
        self.ids.campo_imagem.reload()
        self.ids.lblDescricao.text = '...'
        self.ids.lblObjetos.text = '...'

    def processar_imagem(self):
        """Processamento da imagem no SimpleDarkNet"""
        # Realiza o metodo 'run_deteccao' em uma thread separada
        self.controle.load_spd()
        proc_spd = Thread(target=self.controle.darknet.run_deteccao)
        proc_spd.start()
        """Request da API Visio da Azure"""
        self.controle.load_visio()
        proc_visio = Thread(target=self.controle.visio.realizar_consulta)
        proc_visio.start()

    def verificar_processamento(self, dt):
        if len(self.controle.darknet.img) > 1 is not None:
            if not self.controle.darknet.isRunning:
                self.atualiza_imagem()
                self.atualiza_lblobjs()
                self.controle.new_spd()
        if not self.controle.visio.isRunning:
            if self.controle.visio.processado:
                self.atualiza_descricao()
                self.controle.new_visio()

    def atualiza_imagem(self):
        try:
            imagem = self.controle.darknet.img
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

    def atualiza_lblobjs(self):
        lstobjs = self.controle.darknet.deteccoes
        texto = str()
        for obj in lstobjs:
            nome = obj[0]
            texto += nome + ', '
        texto = texto[0: -2]
        c = 30
        while True:
            part = texto.find(', ', c)
            if part >= c:
                esquerda = texto[0: part]
                direita = texto[part+2::]
                texto = esquerda + '\n' + direita
                c += 33
            else:
                break
        self.ids.lblObjetos.text = texto

    def atualiza_descricao(self):
        texto_descricao = self.controle.visio.get_descricao()[0].get('text')
        self.ids.lblDescricao.text = texto_descricao


class Main(App):
    def build(self):
        self.title = "YolZure - Analise de Imagens"
        pass


jRoot = Main()
jRoot.run()
