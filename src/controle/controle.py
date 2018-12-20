import os.path

from cfgManager import Config
from dbmanager import DBManager
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
            if not os.path.isfile(valor):
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
        os.path.curdir = '../'
        self.__dir_img__ = str()
        self.__visio__ = CompleteVisioRequest()
        self.__spd__ = SimpleDarknet()
        self.__cnfg__ = self.carregarCNFG()
        self.__dbman__ = self.carregarDB()

    def load_visio(self):
        """
        Realiza a pre configuração do objeto visio para a consulta a API
        :return:
        """
        visio_params = self.get_visio_params()
        self.__visio__.__key__ = visio_params[0][2]
        self.__visio__.__vision_url__ = visio_params[1][2]
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
        self.__spd__ = SimpleDarknet(imagem, *SimpleDarknet.YOLOV3.values())

    def new_spd(self):
        self.__spd__ = SimpleDarknet()

    def carregarDB(self):
        db = DBManager(user=self.__cnfg__.get_db_user(),
                       senha=self.__cnfg__.get_db_passwd(),
                       end=self.__cnfg__.get_db_url(),
                       port=self.__cnfg__.get_db_port(),
                       database=self.__cnfg__.get_db_name())
        return db

    def carregarCNFG(self):
        arqkey = open('./controle/chave.key', 'r')
        chave = arqkey.readline()
        cfg = Config(chave, './controle/yolzure.cfg')
        return cfg

    def get_visio_params(self):
        if self.__dbman__ is not None:
            sql = "SELECT * FROM parametros WHERE parametro in (%s, %s)"
            self.__dbman__.abrir_con()
            retorno = self.__dbman__.executar_select(sql, ["visiokey", "visiourl"])
            if len(retorno) == 2:
                return retorno
            else:
                raise Exception('Erro ao recuperar parametros da api visio')
        else:
            raise Exception('Objeto DBManager nao configurado ou corrompido')
