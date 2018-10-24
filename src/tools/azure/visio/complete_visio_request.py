import os.path
import requests


class CompleteVisioRequest:
    """
    Enumerator com os recursos atualmente disponiveis para consulta na API Visio
    """
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

    def __init__(self, key: str = None, url: str = None, img: str = None, recursos: list = None):
        """
        Construtoro
        :param key: Chave da api azure
        :param url: Url para a api azure
        :param img: diretorio da imagem analizada
        :param recursos: Recursos que serao solicitados a api, devem ser rescursos que existem na lista_recursos desta classe
        """
        self.__recursos__ = list()
        self.__img_path__ = str()
        self.__vision_url__ = str()
        self.__key__ = str()
        self.__retorno__ = dict()
        self.isRunning = bool()
        self.processado = False

        self.__key__ = key
        self.__vision_url__ = url
        self.img_path = img
        self.recursos = recursos
        self.retorno = dict()

    @property
    def recursos(self):
        return self.__recursos__

    @recursos.setter
    def recursos(self, args: list = list('all')):
        """
        setter, por padrao, adiciona todos os recursos para a consulta
        :param args: lista dos recursos que deseja consultar na API
        :return:
        :except: TypeError
        """
        if args is None:
            self.__recursos__ = list()
        else:
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
        """

        :param value: Diretorio para a imagem
        :return:
        :raise FileNotFoundError
        """
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
        """
        Metodo para realiza a consulta na API visio da Azure, ela reune todas as configurações definidas anteriormente
        em uma unica chamada a API, esta chamada se bem sucedida ira retornar um dicionario com os resultados da consulta
        cada elemento desse dicionario é o correspondente a um dos recursos solicitados, salva essa resposta no objeto retorno
        :return:
        :except: Exception
        """
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
        """
        Se um dos recursos selecionados para a consulta foi o de tags, retorna as tags do resultado
        :return:
        """
        if self.recursos.count('Tags') > 0:
            tags = self.retorno.get('tags')
            return tags
        else:
            raise ValueError('Não foi realizada a consulta com o recurso de tags.')

    def get_descricao(self):
        """
        Se um dos recursos selecionados para a consulta foi o de descrição, retorna a descrição do resultado
        :return:
        """
        if self.recursos.count('Description') > 0:
            tags = self.retorno.get('description').get('captions')
            return tags
        else:
            raise ValueError('Não foi realizada a consulta com o recurso de Description.')

    def get_categorias(self):
        """
        Retorna as categorias resultantes da consulta
        :return:
        """
        if self.recursos.count('Categories') > 0:
            tags = self.retorno.get('categories')
            return tags
        else:
            raise ValueError('Não foi realizada a consulta com o recurso de Categories.')
