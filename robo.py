#Instalar o pacote "pip install iqoption" em sua maquina, caso contrario voce não conseguira logar 
from iqoptionapi.stable_api import IQ_Option
import time

#Instalar essa biblioteza "pip install configobj"
from configobj import ConfigObj 
import json, sys

#esta função é uma das formas para voce fazer o login 
#Variavel que recenhece seu e-mail e senha para login
##email = input('\nDigite seu e-mail')
#senha = input('\nDigite sua senha')


#Configuração da conta automatica através do Config.txt que está salvo na pasta
config = ConfigObj('config.txt')
email = config['LOGIN']['email']
senha = config['LOGIN']['senha']

tipo = config['AJUSTES']['tipo']
valor_entrada = config['AJUSTES']['valor_entrada']


print('\n Inicie sua conexão com a IQOption')

#função que conecta seu e-mail e senha através da API
API = IQ_Option(email,senha)


#funçãoo que define se seu login e senha estão correto, caso não, ele retornar a mensagem "E-mail ou senha incorreta"
check, reason = API.connect()
if check:
    print('\nConectado com sucesso')
else: 
    if reason == '{"code":"invalid_credentials","message":"You entered the wrong credentials. Please ensure that your login/password is correct."}':
        print('E-mail ou senha incorreta') 
        sys.exit()
    else: 
        print('\nConexão inválida, tente novamente')
    print(reason)
    sys.exit()    

#função que escolhe o tipo de conta demo ou real que voce deseja operar
while True: 
    escolha = input('\nSelecione a conta que voce deseja usar demo ou real?')
    if escolha == 'demo':
        conta ='PRACTICE' #precisa ser escrito desta forma para que a API consiga reconhecer o tipo que conta que voce deseja
        print('\nParabéns você esta na sua conta Demo, agora é só começar a praticar!')
        break   
    if escolha == 'real':
        conta = 'REAL' #precisa ser escrito desta forma para que a API consiga reconhecer o tipo que conta que voce deseja
        print('\nParabéns agora voce esta na sua conta Real é só começar a lucrar muito')
        break
    else:
        print('\nEscolha incorreta, digite demo ou real! ')

API.change_balance(conta)

#Função para a abertura de ordem 
#tipo - é o tipo de ordem que voce quer abrir não usar espaço nem letra minuscula
#valor - Valor que voce deseja entrar na ordem 
#direcao - É a direção que voce deseja abrir a ordem, call ou put 
#exp - tempo de experição da ordem
#tipo - tipo da ordem, ex: binario, digital 

# Não se esqueça que para criar a ordem Binaria voce precisa alterar a orden da função conforme no comentario abaixo.
# função Binaria a ordem é (valor,ativo,direcao,exp,tipo)
# Função Digital a ordem é (ativo,valor,direcao,exp,tipo)

def compra (ativo,valor_entrada,direcao,exp,tipo):
    if tipo == 'digital' :
        check, id = API.buy_digital_spot_v2(ativo,valor_entrada,direcao,exp)
    else:
        check, id = API.buy(valor_entrada,ativo,direcao,exp)

    if check:
        print('Ordem aberta\nPar: ',ativo,'\nTimeFrame:' ,exp,'\nEntrada de',cifrao,valor_entrada)

        while True:
            time.sleep(0.1)
            status , resultado = API.check_win_digital_v2(id) if tipo =='digital' else API.check_win_v4(id)

            if status:
                if resultado > 0:
                    print('Resultado: Win \nLucro:', round(resultado,2), '\nPar:',ativo)
                elif resultado == 0:
                    print('Resultado: Empate \nLucro:', round(resultado,2), '\nPar:',ativo)
                else:
                    print('Resultado: Loss \nLucro:', round(resultado,2), '\nPar:',ativo)
                break
    else:
        print('Erro na abertura da ordem,', id)


perfil = json.loads(json.dumps(API.get_profile_ansyc()))
cifrao = str(perfil['currency_char'])
nome = str(perfil['name'])

valorconta = float(API.get_balance)()

print('\n\n Olá,', nome, '\nSeja bem vindo ao primeiro meu Robo' )
print('\nSeu saldo na conta é ',escolha, 'é de', cifrao,valorconta)
print('\n Seu Valor de entrada é de ',cifrao,valor_entrada)




#ativo = 'EURUSD'
#valor = 10
#direcao = 'call'
#exp = 1
#tipo = 'digital'

ativo = input('\n Digite qual o ativo que voce deseja? ').upper()
exp = input('\n Qual TimeFrame? ')
direcao = input('\n Qual a direção que voce deseja call ou put ? ')




# chama a função de compra 
compra (ativo,valor_entrada,direcao,exp,tipo)








