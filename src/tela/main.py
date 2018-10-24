# Src Imports
from controle.controle import Controle
from tools.filechooser import FileChooser
from threading import Thread
import cv2

# kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup


class Principal(BoxLayout):
    """
        Classe da aplicação kivy, é atraves desta classe que a biblioteca kivy e os codigos python conversao
        ela herda de BoxLayout, ou seja, é uma tela "em caixas" definidas
    """

    def __init__(self, **kwargs):
        """
            metodo inicial, é o primeiro metodo executado quando um novo objeto é criado, tambem é aqui onde variaveis
            globais do objeto devem ser definidas
        :param kwargs: Algumentos padroes de inicalização
        """
        super().__init__(**kwargs)
        """Objeto de controle, é a partir desde objeto que as conexões com a API e a darknet acontecem"""
        self.controle = Controle()
        """Objeto clock, é um gatilho de tempo que ira disparar o metodo verificar_processamento a cada 1 segundo
        Existe com o proposito de automatizar e facilitar a maneira de exibir os resultados, ja que os processos 
        acontecem em multithread, evita conflitos ao gravar e ler nos demais objetos.
        """
        self.timer = Clock
        self.timer.schedule_interval(self.verificar_processamento, 1.0)
        """Esvazia o campo de imagem"""
        self.clk_btn_limpar()

    def clk_btn_procurar(self):
        """
        Funcao executada quando o botao procurar é clicado, cria um objeto FileChooser() que permite selecionar um
        arquivo de imagem navegando atraves das pastas do computador, é uma janelinha de procurar pré-montada, esta janela
        retorna o diretorio do arquivo selecionado
        :return:
        """
        fl = FileChooser()
        self.controle.dir_img = fl.find_file()
        self.ids.campo_diretorio.text = \
            self.controle.dir_img

    def clk_btn_carregar(self):
        """
        Apos procurar a imagem e salvar o diretorio da mesma no objeto de controle, é necessario carregar a imagem no
        widget "campo_imagem" da tela, para isso, basta salvar o diretorio da imagem no atributo source e executar o
        metodo reload(), que carrega a imagem para o widget nativamente.
        :return:
        """
        self.ids.campo_imagem.texture = None
        self.ids.campo_imagem.source = self.controle.dir_img
        """Retira a transparencia da imagem..."""
        self.ids.campo_imagem.color = (1, 1, 1, 1)
        self.ids.campo_imagem.reload()

    def clk_btn_analizar(self):
        """
        Metodo invocado ao pressionar o botao "analizar", verifica se ja nao existe uma analise de imagem em andamento,
        para evitar conflitos multithread, e adiciona o label de aviso de analise em andamento na tela principal, e chama
        o metodo processar_imagem(), pois ele é o metodo que processa a imagem propriamente dita
        :return:
        """
        try:
            # Verifica se nao existe uma instancia da darknet em execução
            if not self.controle.darknet.isRunning:
                box_temp = self.ids.box_btns_img
                # realiza um swap para adicionar label de aviso entre a imagem e os botoes
                self.ids.box_img.remove_widget(self.ids.box_btns_img)
                self.ids.box_img.add_widget(Label(text='Analizando, Aguarde...', id='lblAguarde',
                                                  size_hint=(1, .05)))
                self.ids.box_img.add_widget(box_temp)
                # invoca o metodo de analise da imagem
                self.processar_imagem()
        except Exception:
            texto = str(Exception)
            btn = Button("Ok")
            erro = Popup(title='Erro', content=(texto, btn), auto_dismiss=False)
            btn.bind(on_press=erro.dismiss())
            erro.open()

    def clk_btn_limpar(self):
        """
        Realiza um "reset" na interface grafica, retornando a mesma para o estado inicial
        :return:
        """
        self.ids.campo_imagem.source = ''
        self.ids.campo_imagem.reload()
        self.ids.lblDescricao.text = '...'
        self.ids.lblObjetos.text = '...'

    def processar_imagem(self):
        """
        Realiza o preocessamento da imagem, faz o carregamento dos objetos visio e spd no objeto de controle, cria duas
        threads para executar os metodos de processamento da darknet e da api visio, e inicia estas threads
        :return:
        """
        # Configura o objeto spd em controle.
        self.controle.load_spd()
        # cria a thread para executar o metodo run_deteccao
        proc_spd = Thread(target=self.controle.darknet.run_deteccao)
        # inicia a thread
        proc_spd.start()
        # configura o objeto visio em controle
        self.controle.load_visio()
        # cria a thread para executar o metodo realizar_consulta
        proc_visio = Thread(target=self.controle.visio.realizar_consulta)
        # inicia a thread
        proc_visio.start()

    def verificar_processamento(self, dt):
        """
        Verifica se o processamento da imagem ja foi concluido, mais precisamente, verifica qual das etapas do
        processamento foi concluido, ja que se tratam de processos distintos, em threads separadas.
        Processamentos:
            *Darknet: verifica se a darknet esta configurada e se nao esta em execucao, e entao executa os metodos
            atualiza_imagem() - responsavel por exibir o resultado da darknet, e atualiza_lblobjs() - responsavel por
            mostrar a lista de objetos detectados pela darknet, por fim, "reseta" o objeto spd.
            *Visio: Verifica se o processo de consulta do objeto visio nao esta em execucao, e entao, atualiza o campo
            de descrição na tela principal, por fim, "reseta' o objeto visio.
        :param: dt: Necessario para usar com o metodo Clock.schedule_interval
        :return:
        """
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
        """
        Atualiza o campo da imagem na tela principal com o resultado do processamento da darknet, este resultado é
        a imagem contendo as marcações de objetos, bem como suas categorias e probabilidades, e remove o label de
        "Analisando imagem" da tela principal.
        :return:
        """
        try:
            # Salva a intancia da imagem do objeto darknet
            imagem = self.controle.darknet.img
            # processa os buffers
            buf1 = cv2.flip(imagem, 0)
            buf = buf1.tostring()
            # Cria as texturas que sao utilizadas pelo widget Imagem
            texture1 = Texture.create(size=(imagem.shape[1], imagem.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # atualiza a textura do widget campo_imagem
            self.ids.campo_imagem.texture = texture1
            # Remoção do widget de loading.
            lista = self.ids.box_img.children
            for widget in lista:
                if isinstance(widget, Label):
                    if widget.id is 'lblAguarde':
                        self.ids.box_img.remove_widget(widget)
        except Exception:
            texto = str(Exception)
            btn = Button("Ok")
            erro = Popup(title='Erro', content=(texto, btn), auto_dismiss=False)
            btn.bind(on_press=erro.dismiss())
            erro.open()

    def atualiza_lblobjs(self):
        """
        Exibe na tela inicial os objetos que foram detectados pela darknet.
        :return:
        """
        # Salva a lista de objetos detectados
        lstobjs = self.controle.darknet.deteccoes
        texto = str()
        # adiciona o nome de cada objeto em uma linha de texto
        for obj in lstobjs:
            nome = obj[0]
            texto += nome + ', '
        texto = texto[0: -2]
        c = 30
        # realiza as quebras de linha
        while True:
            part = texto.find(', ', c)
            if part >= c:
                esquerda = texto[0: part]
                direita = texto[part + 2::]
                texto = esquerda + '\n' + direita
                c += 33
            else:
                break
        self.ids.lblObjetos.text = texto

    def atualiza_descricao(self):
        """
        Exibe a descrição da imagem retornada atraves da consulta com a APi visio da azure na tela inicial
        :return:
        """
        texto_descricao = self.controle.visio.get_descricao()[0].get('text')
        self.ids.lblDescricao.text = texto_descricao


class Main(App):
    def build(self):
        self.title = "YolZure - Analise de Imagens"
        pass


jRoot = Main()
jRoot.run()
