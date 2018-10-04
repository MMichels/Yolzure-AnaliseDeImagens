# Src Imports
from controle.controle import Controle
from tools.filechooser import FileChooser

# kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Principal(BoxLayout):
    instancia = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__controle__ = Controle()
        Principal.instancia = self

    def clk_btn_procurar(self=Button):
        fl = FileChooser()
        self.__controle__.dir_img = fl.find_file()
        self.ids.campo_diretorio.text = \
            self.__controle__.dir_img

    def clk_btn_carregar(self):
        self.ids.campo_imagem.source = \
            self.__controle__.dir_img
        self.ids.campo_imagem.reload()


class Main(App):
    pass


jRoot = Main()
jRoot.run()
