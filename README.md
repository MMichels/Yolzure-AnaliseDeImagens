# Yolzure-AnaliseDeImagens
Este é um pequeno projeto pessoal, fruto dos meus primeiros estudos envolvendo inteligencia artificial <br>

Essa aplicação tem como funcionalidades:
  1. Analizar uma imagem e detectar objetos (pessoas, veiculos, animais, copos, mesas..);
  2. Gerar uma descrição em texto da imagem;
  3. Traduzir a descrição para portugues;
  4. Gerar um audio a partir da descrição da imagem.

As técnologias utilizadas nestas funcionalidades:

1. [YOLO](https://pjreddie.com/darknet/yolo/): Real-Time Object Detection
2. Azure [Vision](https://azure.microsoft.com/pt-br/services/cognitive-services/computer-vision/)
3. [GoogleTrans](https://pypi.org/project/googletrans/)
4. Azure [Text to speech](https://azure.microsoft.com/pt-br/services/cognitive-services/text-to-speech/)

A motivação para esse projeto surgiu durante um projeto da faculdade, a criação de um robô que seria capaz de ver, andar, ouvir e falar com as pessoas ao seu redor, no inicio do projeto eu me voluntariei para pesquisar e implementar uma rede neural para a visão do robô, aonde acabei encontrando e estudando a YoLo, após algum tempo o projeto perdeu força, porém minha paixão pela IA cresceu.
Desenvolvi uma simples aplicação desktop para fazer Uso da YoLo nas minhas fotos, descobri o Azure Vision, que tem a capacidade de gerar descrição para foto e pensei "Humm por quê não?".

*E por fim eis aqui a (até então) versão do porquê não.*

Como entusiasta e pesquisador de IA pretendo expandir esse projeto aos poucos, migrando os serviços da Azure e da Google para redes neurais de NLP OpenSource, porém, existe a barreira do idioma português.

Meu objetivo com a disponibilização desse projeto é que ele seja livre para a comunidade, para que outros estudantes possam contribuir em seu desenvolvimento, meu sonho é que se torne uma aplicação util para o publico geral (seria imensamente gratificante saber que deficientes visuais podem ouvir as fotos graças a esta aplicação que será desenvolvida por todos nós).

Até o momento é necessario executar o projeto manualmente, ele está sendo desenvolvido com a IDE PyCharm, uma versão distribuivel será disponibilizada no futuro, quando no minimo o sistema de tradução for alterado para uma rede de NLP OpenSource.

É necessario criar uma conta no Azure Vision e Azure Speech e alterar o arquivo src/yolzure.cfg com suas Chaves e Link's
  

#Dependences:\
Python 3.6 +\
OpenCV 3.4.2+\
kivy 1.10+\
Requests 2.4+\

#Info and sugest:\
michels09@hotmail.com

Este repositório será atualizado até que todos os objetivos sejam concluidos, tutoriais e manuais de melhor qualidade serão disponibilizados a cada fase.
