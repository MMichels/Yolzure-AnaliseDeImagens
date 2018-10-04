from os.path import isfile


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

    def __init__(self):
        self.__dir_img__ = str()
