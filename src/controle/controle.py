from os.path import isfile
from tools.azure.visio.complete_visio_request import CompleteVisioRequest
from tools.yolo.simple_darknet import SimpleDarknet


class Controle:

    @property
    def dir_img(self):
        return self.__dir_img__

    @dir_img.setter
    def dir_img(self, valor):
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
        self.__dir_img__ = str()
        self.__visio__ = CompleteVisioRequest()
        self.__spd__ = SimpleDarknet()

    def load_visio(self):
        self.__visio__.__key__ = '22e69212b68d4215875afd57e3f14da7'
        self.__visio__.__vision_url__ = 'https://brazilsouth.api.cognitive.microsoft.com/vision/v1.0/'
        self.__visio__.img_path = self.dir_img
        recursos = [CompleteVisioRequest.DESCRICAO, CompleteVisioRequest.TAGS]
        self.__visio__.recursos = recursos

    def new_visio(self):
        self.__visio__ = CompleteVisioRequest()

    def load_spd(self):
        imagem = self.dir_img
        cfg = '../tools/yolo/cfg/yolov3.cfg'
        weigth = '../tools/yolo/weigths/yolov3.weights'
        classes = '../tools/yolo/classes/yolo.txt'
        self.__spd__ = SimpleDarknet(imagem, cfg, weigth, classes)
        self.__spd__.taxa_min = .5

    def new_spd(self):
        self.__spd__ = SimpleDarknet()