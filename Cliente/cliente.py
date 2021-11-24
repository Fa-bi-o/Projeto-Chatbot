from zeep import Client
import requests
import json
import os

# FALTA:
# SUBTRAIR OS PEDIDOS ENQUANTO ESTÃO SENDO FEITOS DA QUANTIDADE TOTAL EM ESTOQUE
# DEVOLVER CASO AO PEDIDO SEJA CANCELADO


# CRIAÇÃO DO CLIENTE E ACESSANDO O LINK DO SERVIDOR
client = Client('http://localhost:9090/servidorAplicacaoPort?wsdl')

# CRIAÇÃO DE DICIONÁRIOS COM OS ALIMENTOS
comida = {'1': ['Sanduiche', '15,00'], '2': ['Hamburguer', '23,00'], '3': ['Batata Frita', '6,00']}
bebida = {'1': ['Refrigerante', '8,00'], '2': ['Suco', '6,00']}


# FUNÇÕES QUE SERÃO UTILIZADAS NA IMPRESSÃO (RETURN) PARA O USUÁRIO
def comidas():
    return f'''1 - Sanduiche - R$15,00{os.linesep}2 - Hamburguer - R$23,00{os.linesep}3 - Batata Frita - R$6,00'''


def bebidas():
    return f'''1 - Refrigerante - R$8,00{os.linesep}2 - Suco - R$6,00'''


# CLASSE PRINCIPAL
class ChatBot:

    # INICIALIZAÇÃO, COM O TOKEN DO BOT, CRIADO PREVIAMENTE COM O BOTFATHER + URL DO TELEGRAM E A FASE INICIAL
    def __init__(self):

        token = '2122431700:AAFUAnL4ZOILIMIu_xcVrriE4Cw6laU9Zms'
        self.url = f'https://api.telegram.org/bot{token}/'
        self.fase = 1
        self.pedido = []

    # CRIAÇÃO DO LAÇO QUE VAI VERIFICAR SE EXISTE UMA MENSAGEM NOVA E RESPONDER ESSA MENSAGEM
    def iniciar(self):

        nova_mensagem = None

        while True:

            atualizar_id = self.mensagem_usuario(nova_mensagem)
            mensagens = atualizar_id['result']

            if mensagens:
                for mensagem in mensagens:
                    nova_mensagem = mensagem['update_id']
                    id_usuario = mensagem['message']['from']['id']
                    resposta = self.resposta_usuario(mensagem, self.fase)
                    self.enviar_resposta_usuario(resposta, id_usuario)

    # CAPTURA DAS MENSAGENS DO USUÁRIO
    def mensagem_usuario(self, nova_mensagem):

        mensagem_capturada = f'{self.url}getUpdates?timeout=50'

        if nova_mensagem:
            mensagem_capturada = f'{mensagem_capturada}&offset={nova_mensagem + 1}'

        resultado = requests.get(mensagem_capturada)

        return json.loads(resultado.content)

    # CRIAÇÃO DAS RESPOSTAS POSSÍVEIS AO USUÁRIO + REQUISIÇÕES AO SERVIDOR
    def resposta_usuario(self, mensagem, fase):

        mensagem = mensagem['message']['text']

        if fase == 1:

            self.fase = 2

            return f''' Seja bem vindo ao chatBot. Digite o número correspondente a opção desejada{os.linesep}{os.linesep}1 - Lanches{os.linesep}2 - Bebidas{os.linesep}3 - Sair '''

        elif fase == 2:

            if mensagem == '1':

                self.fase = 3

                return f'''{comidas()}{os.linesep}4 - Voltar'''

            elif mensagem == '2':

                self.fase = 4

                return f'''{bebidas()}{os.linesep}4 - Voltar'''

            elif mensagem == '3':

                self.fase = 1
                self.pedido.clear()

                return f'''Agradecemos seu contato, volte sempre{os.linesep}'''

            else:
                return 'Opção inválida'

        elif fase == 3:

            if mensagem == '1' or mensagem == '2' or mensagem == '3':

                estoque = client.service.verificarEstoque(comida[mensagem][0])

                if estoque > 0:

                    self.pedido.append(comida[mensagem][0])

                    return f'''{comida[mensagem][0]} adicionado(a) ao carrinho{os.linesep}{os.linesep}{comidas()}{os.linesep}4 - Fechar Pedido{os.linesep}5 - Voltar'''

                else:
                    return f'''Nosso estoque de {comida[mensagem][0]} acabou por hoje :c{os.linesep}{comidas()}{os.linesep}4 - Fechar Pedido{os.linesep}5 - Voltar'''

            elif mensagem == '4':

                self.fase = 5
                total = client.service.calcularPreco(self.pedido)

                return f'''Seu pedido deu um total de : R$ {total}, confirme para fechamendo do pedido (s/n)'''

            elif mensagem == '5':

                self.fase = 2

                return f'''1 - Lanches{os.linesep}2 - Bebidas{os.linesep}3 - Sair '''

            else:
                return 'Opção inválida'

        elif fase == 4:

            if mensagem == '1' or mensagem == '2':

                estoque = client.service.verificarEstoque(comida[mensagem][0])

                if estoque > 0:

                    self.pedido.append(bebida[mensagem][0])

                    return f'''{bebida[mensagem][0]} adicionado(a) ao carrinho{os.linesep}{os.linesep}{bebidas()}{os.linesep}3 - Fechar Pedido{os.linesep}4 - Voltar'''

                else:
                    return f'''Nosso estoque de {bebida[mensagem][0]} acabou por hoje :c{os.linesep}{bebidas()}{os.linesep}3 - Fechar Pedido{os.linesep}4 - Voltar'''

            elif mensagem == '3':

                self.fase = 5
                total = client.service.calcularPreco(self.pedido)

                return f'''Seu pedido deu um total de : R$ {total}, confirme para fechamendo do pedido (s/n)'''

            elif mensagem == '4':

                self.fase = 2

                return f'''1 - Lanches{os.linesep}2 - Bebidas{os.linesep}3 - Sair '''

            else:
                return 'Opção inválida'

        elif fase == 5:

            if mensagem.lower() in ('s', 'sim'):

                self.fase = 6

                return f'''Pedido Fechado!{os.linesep}Informe o endereço de entrega'''

            else:

                self.fase = 1
                self.pedido.clear()

                return f'''Pedido Cancelado!{os.linesep}Agradecemos seu contato, volte sempre{os.linesep}'''

        elif fase == 6:

            self.fase = 7

            return f'''Confirma o endereço de entrega (s/n)?{os.linesep}{mensagem}'''

        elif fase == 7:

            if mensagem.lower() in ('s', 'sim'):

                return f'''Endereço confirmado. Em breve receberá seu pedido{os.linesep}Agradecemos a preferência'''

            else:

                self.fase = 1
                self.pedido.clear()

                return f'''Pedido Cancelado!{os.linesep}Agradecemos seu contato, volte sempre{os.linesep}'''

    def enviar_resposta_usuario(self, resposta, id_usuario):

        resposta_usuario = f'{self.url}sendMessage?chat_id={id_usuario}&text={resposta}'
        requests.get(resposta_usuario)


bot = ChatBot()
bot.iniciar()
