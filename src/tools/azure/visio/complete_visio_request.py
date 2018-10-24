from typing import Optional, Any, Dict
import os.path
import requests


class CompleteVisioRequest:
    lista_recursos = ['Categories', 'Description',
                      'Color', 'Tags', 'ImageType',
                      'Faces', 'Adult']

    CATEGORIAS = lista_recursos[0]
    DESCRICAO = lista_recursos[1]
    CORES = lista_recursos[2]
    TAGS = lista_recursos[3]
    FORMATO = lista_recursos[4]
    ROSTOS = lista_recursos[5]
    MODERACAO = lista_recursos[6]

    def __init__(self, **kwargs):
        self.__recursos__ = list()
        self.__img_path__ = str()
        self.__vision_url__ = str()
        self.__key__ = str()
        self.__retorno__ = dict()
        self.isRunning = bool()
        self.processado = False

        if len(kwargs) > 0:
            self.__key__ = kwargs.get('key')
            self.__vision_url__ = kwargs.get('url')
            self.img_path = kwargs.get('img')
            self.recursos = kwargs.get('recursos')

    @property
    def recursos(self):
        return self.__recursos__

    @recursos.setter
    def recursos(self, args):
        if args.count('todos') > 0 or args.count('all'):
            self.__recursos__ = CompleteVisioRequest.lista_recursos
        else:
            for rec in args:
                rec = str(rec).capitalize()
                if CompleteVisioRequest.lista_recursos.count(rec) > 0:
                    self.__recursos__.append(rec)
                else:
                    raise TypeError(f'Recurso: {rec} não suportado ou inexistente')

    @property
    def img_path(self):
        return self.__img_path__

    @img_path.setter
    def img_path(self, value: str):
        value = os.path.abspath(value)
        if not os.path.exists(value):
            raise FileNotFoundError(f'Não foi possivel localizar o arquivo {value}')
        self.__img_path__ = value

    @property
    def retorno(self):
        return self.__retorno__

    @retorno.setter
    def retorno(self, valor: dict):
        self.__retorno__ = valor

    def realizar_consulta(self):
        self.isRunning = True
        self.__vision_url__ += "analyze"
        image_data = open(self.img_path, "rb").read()
        cabecalho = {'Ocp-Apim-Subscription-Key': self.__key__,
                     'Content-Type': 'application/octet-stream'}
        params = ''
        for rec in self.recursos:
            if not self.recursos.index(rec) is len(self.recursos) - 1:
                params += str(rec) + ','
            else:
                params += str(rec)

        params = {'visualFeatures': params}
        retorno = ''
        try:
            retorno = requests.post(url=self.__vision_url__,
                                    headers=cabecalho,
                                    params=params,
                                    data=image_data)
            retorno.raise_for_status()
            retorno = retorno.json()
            self.retorno = retorno
            self.processado = True
        except Exception:
            print('Erro ao realizar consulta')
            self.processado = False
        self.isRunning = False

    def get_tags(self):
        if self.recursos.count('Tags') > 0:
            tags = self.retorno.get('tags')
            return tags
        else:
            raise ValueError('Não foi realizada a consulta com o recurso de tags.')

    def get_descricao(self):
        if self.recursos.count('Description') > 0:
            tags = self.retorno.get('description').get('captions')
            return tags
        else:
            raise ValueError('Não foi realizada a consulta com o recurso de Description.')

    def get_categorias(self):
        if self.recursos.count('Categories') > 0:
            tags = self.retorno.get('categories')
            return tags
        else:
            raise ValueError('Não foi realizada a consulta com o recurso de Categories.')
