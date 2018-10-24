import cv2
import numpy
from random import randint
from os.path import *

class SimpleDarknet:

    @property
    def img(self):
        """
            Getter img
        :return: numpy.ndarray correspondente a imagem retornado pelo metodo cv2.imread('diretorio/da/imagem')
        """
        return self._img

    @img.setter
    def img(self, imagem):
        """
            Setter imagem.
            Verifica que o parametro é do tipo String, se nao for string ira levantar uma exessao TypeError.
            Se for string, ira executar o metodo cv2.imread(parametro) e salvar o retorno na variavel.
        :param imagem: string com o diretorio correspondente a imagem com a extensao, EX: '/diretorio/da/imagem/imagem.jpg'
        :return: None
        """
        if not isinstance(imagem, str):
            raise TypeError('Img deve ser uma string contendo o diretorio da imagem')
        self._img = cv2.imread(imagem)

    @property
    def altura(self):
        """
            getter altura
        :return: int
        """
        return self._altura

    @altura.setter
    def altura(self, altura):
        """
            Setter altura
        :param altura: valor inteiro correspondente a altura calculada pelo metodo calc_metricas
        :return: None
        """
        self._altura = altura

    @property
    def largura(self):
        """
            Getter largura
        :return: int correspondente a largura da imagem
        """
        return self._largura

    @largura.setter
    def largura(self, valor):
        """
            Setter largura
        :param valor: int calculado por calc_metricas()
        :return: None
        """
        self._largura = valor

    @property
    def modelo(self):
        """
            Getter modelo
        :return: str contendo diretorio completo ou parcial do modelo
        """
        return self._modelo

    @modelo.setter
    def modelo(self, mod):
        """
            Setter modelo
        :param mod: str contendo o diretorio completo ou parcial do modelo, Ex: '/diretorio/do/modelo/modelo.weigths
        :return: None
        """
        if not isinstance(mod, str):
            raise TypeError('model deve ser uma variavel string contendo o diretorio do modelo')
        self._modelo = mod

    @property
    def config(self):
        """
            Getter config
        :return: str contendo o diretorio completo ou parcial do arquivo.cfg
        """
        return self._config

    @config.setter
    def config(self, config):
        """
            Setter config
        :param config: str contendo o diretorio completo ou parcial do arquivo.cfg
        :return: None
        """
        if not isinstance(config, str):
            raise TypeError('config deve ser uma variavel string contendo o diretorio do arquivo .cfg')
        self._config = config

    @property
    def classes(self):
        """
            Getter classes
        :return: conteudo do arquivo de classes (nomes dos objetos) em forma de string.
        """
        return self._classes

    @classes.setter
    def classes(self, arquivo_classes):
        """
            Setter classes
        :param arquivo_classes: str contendo o diretorio completo ou parcial do arquivo_de_classes.txt
        :return: None
        """
        if not isinstance(arquivo_classes, str):
            raise TypeError('arquivo_classes deve ser uma variavel string '
                            'contendo o diretorio do arquivo  de classes.txt')
        if not exists(arquivo_classes):
            raise FileNotFoundError(f'Não foi possivel encontrar o arquivo {arquivo_classes}')
        arquivo_classes = abspath(arquivo_classes)
        with open(arquivo_classes, 'rt') as f:
            self._classes = f.read().rstrip('\n').split('\n')

    @property
    def blob(self):
        """
            Getter blob
        :return: numpy.ndarray retornado pelo metodo cv2.dnn.blobFromImage()
        """
        return self._blob

    @blob.setter
    def blob(self, img):
        """
            Setter do Blob
            Executa o metodo cv2.dnn.blobFromImage() utilizando parametros padroes
        :param img: numpy.ndarray retornado pelo metodo cv2.imread()
        :return: None
        """
        if isinstance(img, numpy.ndarray):
            self._blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), (0, 0, 0), True, crop=False)
        else:
            raise Exception('img nao é uma instancia cv2.imread')

    @property
    def taxa_min(self):
        """
            Getter taxa_min
            taxa_min corresponde a confiabilidade minima da detecção de objetos na imagem.
            valor padrao = 0.5
        :return: float
        """
        return self._taxa_min

    @taxa_min.setter
    def taxa_min(self, valor):
        """
            Setter taxa_min
            taxa_min corresponde a confiabilidade minima da detecção de objetos na imagem.
            deve ser um valor float entre 0 e 1.
        :param valor: float > 0 ou float < 1
        :return: None
        """
        if isinstance(valor, float) and valor < 1:
            self._taxa_min = valor
        else:
            raise TypeError('Atributo taxa minima deve ser um valor float positivo menor que 1')

    @property
    def previsoes(self):
        """
            Getter previsoes
        :return: numpy.ndArray retornado por _nat.forward() contem os valores correspondentes ao retorno da rede neural
        """
        return self._previsoes

    @previsoes.setter
    def previsoes(self, value):
        """
            Setter previsoes
        :param value: numpy.ndArray retornado por _nat.forward()
        :return: None
        """
        self._previsoes = value

    @property
    def deteccoes(self):
        """
            Getter deteccoes
            Array list contendo as informações relevantes de cada objeto detectado com confiabilidade > taxa_min
            Organizado da seguinte maneira:
                deteccoes[] -> contem os arraylists de cada uma das deteccoes
                deteccoes[][1] -> str da classe correspondente ao objeto detectado
                deteccoes[][2] -> array contendo os valores de [x_centro, y_centro, largura, altura, x1, x2, y1, y2]
                deteccoes[][3] -> cor randomizada pelo metodo desenhar_caixas()
        :return: list(list()) contendo as deteccoes calculadas pelo metodo localizar_deteccoes()
        """
        return self._deteccoes

    @deteccoes.setter
    def deteccoes(self, value):
        """
            Setter deteccoes
        :param value: objeto da classe list()
        :return: None
        :raise: TypeError
        """
        if not isinstance(value, list):
            raise TypeError('deteccoes deve ser um objeto da classe list()')
        self._deteccoes = value

    @property
    def isRunning(self):
        return self._running

    @isRunning.setter
    def isRunning(self, value):
        self._running = value

    def __init__(self, imagem: str = None, config: str = None,
                 modelo: str = None, arquivo_classes: str = None):
        """
            Construtor, Inicializa o objeto e configura os atributos que recebem valores.
        :param imagem: str contendo o diretorio da imagem que sera processada.
        :param config: str contendo o diretorio do arquivo.cfg correspondente ao modelo pré treinado yolo
        :param modelo: str contendo o diretorio do arquivo.weights contendo o modelo pré treinado yolo.
        :param arquivo_classes: str contendo o diretorio do arquivo_de_classes.txt correspondente ao modelo pré treinado Yolo
        """
        # Inicializa as variaveis privadas.
        self._nat = None
        self._previsoes = numpy.ndarray(0)
        self._deteccoes = list(list())
        self._img = numpy.ndarray(0)
        self._altura = int(0)
        self._largura = int(0)
        self._modelo = str('')
        self._config = str('')
        self._classes = str('')
        self._blob = numpy.ndarray(0)
        self._taxa_min = float(0.5)
        self._running = False

        if arquivo_classes is not None:
            self.classes = arquivo_classes

        # se todos os parametros receberam valores, ira instanciar o objeto e configurar a rede neural
        if imagem is not None and config is not None and modelo is not None:
            self.img = imagem
            self.config = config
            self.modelo = modelo

        # se o unico parametro com valor for a imagem, configura a imagem e exibe uma msg de aviso
        elif imagem is not None and config is None and modelo is None and arquivo_classes is None:
            self.img = imagem
            print('**Configure o modelo, o .cfg e o arquivo de classes manualmente**')
        # se todos os atributos forem nulos, exibe uma msg de aviso
        elif imagem is None and config is None and modelo is None and arquivo_classes is None:
            print('**Realize o carregamento da imagem, modelo e configuracoes manualmente antes de executar**')
        else:
            raise Exception('Erro de construtor, informe Imagem, ou imagem e modelo e config, ou imagem e modelo'
                            ' e config e o arquivo de classes')

    def config_nat(self):
        """
            Configura a rede neural com o modelo e o arquivo de configuracoes recebidos!
        :return: None
        :raise Exeption se self.modelo ou self.config is None
        """
        if self.modelo is not None and self.config is not None:
            try:
                """Carrega a rede neural para a biblioteca opencv"""
                self._nat = cv2.dnn.readNetFromDarknet(cfgFile=self.config, darknetModel=self.modelo)
                #self._nat = cv2.dnn.readNet(self.modelo, self.config)
                """Utiliza Backend padrao"""
                self._nat.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
                """Tenta utilizar o processamento da rede com o OPENCL"""
                self._nat.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

            except Exception:
                print('Erro ao configurar o modelo para a rede', Exception.args)
        else:
            raise Exception('modelo e cfg nao encontrados')

    def config_blob(self):
        """
            Configura o blob e realiza o input na rede
        :return: None
        :raise: Exeption("nat nao configurada")
        """
        self.blob = self.img
        if self._nat is not None:
            self._nat.setInput(self.blob)
        else:
            raise Exception("nat inexistente")

    def calc_metricas(self):
        """
            Calcula a largura e a altura da imagem
        :return: None
        ;:raise Exception("img nao existe")
        """
        if self.img is not None:
            self.altura = self.img.shape[0]
            self.largura = self.img.shape[1]
        else:
            raise Exception('img inexistente')

    def calc_previsoes(self):
        """
            inicia a rede neural e salva os resultados na variavel previsoes.
        :return: None
        """
        if self._nat is not None:
            if self.modelo.find('v3') > 0:
                layer_names = self._nat.getLayerNames()
                output_layers = [layer_names[i[0] - 1] for i in self._nat.getUnconnectedOutLayers()]
                self.previsoes = self._nat.forward(output_layers)
            else:
                self.previsoes = self._nat.forward()

    def localizar_deteccoes(self):
        """
            Percorre os dados salvos na variavel previsoes e localiza aqueles que possuem confiabilidade acima da
            taxa_min.
            Cria uma lista com as informações relevantes de cada uma das previsoes que possuem taxa de correspondencia
            aceitavel e salva esta lista na variavel deteccoes.
        :return: None
        """
        deteccoes = list()

        # rotina interna para preenchimento das deteccoes
        def preenche_deteccoes(indice_classe, confiabilidade, detect):
            # cria uma lista para salvar as informaçoes da deteccao
            deteccao = list()
            # salva o 'nome' do objeto detectado
            deteccao.append(self.classes[indice_classe])
            # salva a confiabilidade da detecao
            deteccao.append(confiabilidade)
            # Cria uma lista para salvar as posicoes x, y e a largura e altura
            metricas_detec = list()
            # salva a posicao x correspondente ao centro da figura
            metricas_detec.append(detect[0] * self.largura)
            # salva o y correspondente ao centro da figura
            metricas_detec.append(detect[1] * self.altura)
            # salva o comprimento da figura
            metricas_detec.append(detect[2] * self.largura)
            # salva a altura da figura
            metricas_detec.append(detect[3] * self.altura)
            # salva as metricas na lista do objeto detectado
            deteccao.append(metricas_detec)
            # salva a deteccao na lista de deteccoes do objeto da classe
            deteccoes.append(deteccao)

        # Rotina para o uso de movelos yolov2
        def detec_v2(previsoes):
            for i in range(self.previsoes.shape[0]):
                prob_detec = self.previsoes[i][5:]
                indice_classe = prob_detec.argmax(axis=0)
                confiabilidade = prob_detec[indice_classe]
                if confiabilidade > self.taxa_min:
                    preenche_deteccoes(indice_classe, confiabilidade, previsoes[i])

        # Rotina para o uso dos modelos yolov3
        def detec_v3(previsoes):
            for saidas in previsoes:
                for deteccao in saidas:
                    prob_detec = deteccao[5:]
                    indice_classe = numpy.argmax(prob_detec)
                    confiabilidade = prob_detec[indice_classe]
                    if confiabilidade > self.taxa_min:
                        preenche_deteccoes(indice_classe, confiabilidade, deteccao)

        # Verifica se esta sendo utilizado um modelo v2 ou v3
        if self.modelo.find('v3') > 0:
            detec_v3(self.previsoes)
        else:
            detec_v2(self.previsoes)

        self.deteccoes = deteccoes

    def desenhar_caixas(self):
        """
            Desenha os 'bounding boxes' de cada objeto detectado em localizar_deteccoes.
            este metodo só ira surtir efeito apos a execução do metodo localizar_deteccoes pois ele os valores
            salvos na variavel self.deteccoes.
        :return: None
        """
        if len(self.deteccoes) > 0:
            for i in range(len(self.deteccoes)):
                x_centro = self.deteccoes[i][2][0]
                y_centro = self.deteccoes[i][2][1]
                largura = self.deteccoes[i][2][2]
                altura = self.deteccoes[i][2][3]

                '''
                    calculo dos pontos para desenhar o quadrado com o cv2.rectangle
                    obteve-se o ponto central e as dimencoes da figura detectada
                    para localizar o ponto inferior esquerdo é realizada uma subtracao
                    entre o x central e as larguras e alturas, e para o canto superior
                    direito, é realizada a soma.
                    A multiplicacao por 0.5 se da pelo fato de que o X e Y sao centrais.
                '''
                x1 = int(x_centro - largura * 0.5)
                y1 = int(y_centro - altura * 0.5)
                x2 = int(x_centro + largura * 0.5)
                y2 = int(y_centro + altura * 0.5)

                # Randomiza uma cor RGB
                cor = (randint(0, 255),
                       randint(0, 255),
                       randint(0, 255))

                listTemp = (x1, y1, x2, y2)
                for c in listTemp:
                    self.deteccoes[i][2].append(c)
                self.deteccoes[i].append(cor)

                cv2.rectangle(self.img, (x1, y1), (x2, y2), cor, 2)

        else:
            print('Não existem objetos detectados ou a deteccao nao foi executada')

    def escrever_legendas(self):
        """
            Escreve a 'classe' ou nome de cada objeto detectado na imagem, pode ser utilizado
            antes ou depois do metodo desenhar_caixas().
        :return: None
        """
        if len(self.deteccoes) > 0:
            for i in range(len(self.deteccoes)):
                legenda = self.deteccoes[i][0]
                confiabilidade = self.deteccoes[i][1]
                legenda += ' {:.2f}'.format(confiabilidade)

                if len(self.deteccoes) > 2:
                    x1 = self.deteccoes[i][2][4]
                    y1 = self.deteccoes[i][2][5]
                    cor = self.deteccoes[i][3]

                else:
                    x_centro = self.deteccoes[i][2][0]
                    y_centro = self.deteccoes[i][2][1]
                    largura = self.deteccoes[i][2][2]
                    altura = self.deteccoes[i][2][3]

                    x1 = int(x_centro - largura * 0.5)
                    y1 = int(y_centro - altura * 0.5)

                    # Randomiza uma cor RGB
                    cor = (randint(0, 255),
                           randint(0, 255),
                           randint(0, 255))

                cv2.putText(self.img, legenda, (x1, y1),
                            cv2.FONT_HERSHEY_COMPLEX,
                            1, cor, 2, cv2.LINE_8)

        else:
            print('Não existem objetos detectados ou a deteccao nao foi executada')

    def run_deteccao(self):
        """
            Realiza todos os metodos do processamento da imagem em sequencia
        :return: None
        """
        self.isRunning = True
        self.config_nat()
        self.config_blob()
        self.calc_previsoes()
        self.calc_metricas()
        self.localizar_deteccoes()
        self.desenhar_caixas()
        self.escrever_legendas()
        self.isRunning = False

    def exibir_results(self):
        """
            Exibe resultados apos executar o run_deteccoes().
        :return: None
        """
        print('Altura da imagem:', self.altura)
        print('Largura da imagem:', self.largura)
        print('Num de elementos previstos:', len(self.previsoes))
        print('Num de Objetos detectados:', len(self.deteccoes))
        cv2.imshow('Resultado:', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
