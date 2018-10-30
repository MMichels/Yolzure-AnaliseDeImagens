from os.path import isfile

from simple_darknet import SimpleDarknet
from tools.azure.visio.complete_visio_request import CompleteVisioRequest


class Controle:

    @property
    def dir_img(self):
        return self.__dir_img__

    @dir_img.setter
    def dir_img(self, valor: str):
        """
        Setter do diretorio da imagem, responsavel por garantir que é uma imagem valida e existente.
        :param valor: diretorio da imagem
        :return:
        :except TypeError, FileNotFoundError
        """
        if valor is None or valor is '':
            self.__dir_img__ = valor
        else:
            if not isinstance(valor, str):
                raise TypeError(f'{valor} nao é uma string!')
            if not isfile(valor):
                raise FileNotFoundError(f'{valor} nao corresponde a um arquivo')
            if not (valor.endswith('.jpg') or valor.endswith('.png') or valor.endswith('jpeg')):
                raise TypeError(f'O arquivo {valor} nao é um arquivo valido, '
                                f'devem ser imagens .png, .jpg ou .jpeg')
            else:
                self.__dir_img__ = valor

    @property
    def visio(self):
        return self.__visio__

    @property
    def darknet(self):
        return self.__spd__

    def __init__(self):
        """
        Metodo inicial, define os atibutos __dir_img__ = armazena o diretorio da imagem.
        __visio__ = instancia de completeVisioRequest
        __spd__ = instancia de SimpleDarkNet
        """
        self.__dir_img__ = str()
        self.__visio__ = CompleteVisioRequest()
        self.__spd__ = SimpleDarknet()

    def load_visio(self):
        """
        Realiza a pre configuração do objeto visio para a consulta a API
        :return:
        """
        self.__visio__.__key__ = '191e3dde5b204de4a4ebddab6abb6c58'
        self.__visio__.__vision_url__ = 'https://brazilsouth.api.cognitive.microsoft.com/vision/v1.0/'
        self.__visio__.img_path = self.dir_img
        recursos = [CompleteVisioRequest.DESCRICAO, CompleteVisioRequest.TAGS]
        self.__visio__.recursos = recursos

    def new_visio(self):
        self.__visio__ = CompleteVisioRequest()

    def load_spd(self):
        """
        Realiza a pre configuração do objeto spd para consulta a darknet
        :return:
        """
        imagem = self.dir_img
        cfg = 'D:\\Mateus\\Mega\\Python\\util\\visao\\Yolo\\cfg\\yolov3.cfg'
        weigth = 'D:\\Mateus\\Mega\\Python\\util\\visao\\Yolo\\weigths\\yolov3.weights'
        classes = 'D:\\Mateus\\Mega\\Python\\util\\visao\\Yolo\\classes\\yolo.txt'
        self.__spd__ = SimpleDarknet(imagem, cfg, weigth, classes)
        self.__spd__.taxa_min = .5

    def new_spd(self):
        self.__spd__ = SimpleDarknet()
