#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
import os, json, time

#############################################################################################################

def ConectarSe():

    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)

        clientHost = "127.0.0.1"
        clientPort = 800

        clientSocket.connect((clientHost, clientPort))

        return clientSocket

    except:
        input("\n\n\n► ► ► Não foi possivel conectar-se. ◄ ◄ ◄\n\n" +
              "Verifique se o servidor foi inicializado corretamente.")



#############################################################################################################



def CabecalhoUI(nomeMenu, usuarioLogado = ""):

    print("\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ %s | CIn DRIVE ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n" %nomeMenu.upper())


    if usuarioLogado != "":
        print("▌ Usuário: %s" %usuarioLogado)
        
    else:
        print("▌ Usuário: DESCONECTADO")

        
    print("▌ Conexão estabelecida")


##############################################################################################################    



def LerString(textoComando):

    while True:
        stringUsuario = input("\n" + textoComando + "\n")

        if (stringUsuario != ""): break

    return stringUsuario



##############################################################################################################



def LerStringDecisao(textoComando):

    while True:
        escolhaUsuario = input(textoComando + "\n")
        if escolhaUsuario == "S" or escolhaUsuario == "N": break

    return escolhaUsuario



##############################################################################################################



def LerInteiro(textoComando, valorMinimo, valorMaximo):

    while True:
        try:
            entradaUsuario = int(input(textoComando + "\n"))

            while (valorMinimo > entradaUsuario) or (entradaUsuario > valorMaximo):
                print("\n\n► ► ► Ops! O número digitado deve estar entre %d e %d. ◄ ◄ ◄\n" %(valorMinimo, valorMaximo))
                entradaUsuario = int(input(textoComando + "\n"))

            break

        except ValueError:
            print("\n\n► ► ► Hmm... Você realmente digitou? Perceba também que são permitidos apenas números inteiros. ◄ ◄ ◄\n")

    return entradaUsuario



##################################################################################################################
clientSocket = ConectarSe()  


def ChamarServidor(solicitacao, clientSocket):

    clientSocket.send(solicitacao.encode("utf-8"))


               

def MenuInicial(clientSocket):

    CabecalhoUI("Menu Inicial")
     
    

    print("\n\n► Olá! Para começar, escolha uma opção:\n\n" +
          "1) Acessar Conta\n" +
          "2) Criar uma Conta\n" +
          "3) Sobre o CIn Drive")
          
    opcaoEscolhida = LerInteiro("\nDigite o número respectivo à sua escolha:", 1, 3)

    if opcaoEscolhida == 1:
        ChamarServidor("AcessarConta()", clientSocket)       
        AcessarConta(clientSocket)

    elif opcaoEscolhida == 2:
        ChamarServidor("CriarConta()", clientSocket) 
        CriarConta(clientSocket)

    else:
        Sobre(clientSocket)



##############################################################################################################


def MenuPrincipal(nomeCliente, clientSocket):

    CabecalhoUI("Menu Principal", nomeCliente)

    print("\n\n► Bem-vindo(a), %s! Sua autenticação foi feita com sucesso.\n\n" %nomeCliente +
          "Para onde você gostaria de ir agora? \n\n" +
          "1) Meu Drive\n" +
          "2) Compartilhados Comigo")

    opcaoEscolhida = LerInteiro("\nDigite o número respectivo à sua escolha:", 1, 2)

    if opcaoEscolhida == 1:
        ChamarServidor("MeuDrive()", clientSocket)
        MeuDrive(nomeCliente, clientSocket)

    else:
        ChamarServidor("CompartilhadosComigo()", clientSocket)
        CompartilhadosComigo(nomeCliente, clientSocket)



##############################################################################################################


def Sobre(clientSocket):

    CabecalhoUI("Sobre")

    print("► Este programa é parte de um projeto da disciplina Redes de Computadores ministrada no Centro " +
          "de Informática pela Universidade Federal de Pernambuco (CIn, UFPE). A ideia é implementar um sistema " +
          "com funções semelhantes as dos serviços na nuvem, tais como autenticação do usuário, download e upload "+
          "de pastas e arquivos, compartilhamento destes e criação de pastas.\n\n" +
          "► Apesar de recente, nosso sistema é concorrente do Google Drive e a empresa nos ofereceu uma oferta de " +
          "US$ 5.000.000.000,02 (cinco bilhões de dólares e dois centavos). Porém, estamos em dúvida se vamos vender.\n\n" +
            "▌ PROFESSOR: Kelvin Lopes Dias.\n\n" +
            "▌ MONITOR: Guthemberg da Silva Sampaio.\n\n" +
            "▌ INTEGRANTES DA EQUIPE:\n\n" +
            "  • Bernardo Gomes de Melo;\n" +
            "  • Davy de Andrade Mota;\n" +
            "  • Eduardo Santos de Moura;\n" +
            "  • Mayara Gomes de Oliveira Pina;\n" +
            "  • Moizés Gabriel Mendes Macêdo.\n\n")

    print("CIn Drive, onde os seus dados estão 100% protegidos. Só que não.\n\n") 

    input("Pressione 'enter' para retornar ao Menu Inicial.")

    MenuInicial(clientSocket)



##############################################################################################################
       


def DownloadArquivo(nomeCliente, nomeArquivoEscolhido, clientSocket):

    CabecalhoUI("Download de Arquivo", nomeCliente)

    print("\n\n► Tem certeza que deseja fazer o download do arquivo '%s'?" %nomeArquivoEscolhido)

    escolhaUsuario = LerStringDecisao("\n(Digite 'S' para afirmativo, ou 'N', caso contrário:)")

    if escolhaUsuario == "S":

        clientSocket.send(escolhaUsuario.encode("utf-8")) # ENVIA "S" OU "N"

        arquivoRequisitado = open("./Disco Local/Downloads/" + nomeArquivoEscolhido, "wb")

        bytesRecebidos = clientSocket.recv(1024)
        while bytesRecebidos:
            arquivoRequisitado.write(bytesRecebidos)
            bytesRecebidos = clientSocket.recv(1024)
        arquivoRequisitado.close()
        
        input("\nDownload do arquivo '%s' completo! Você pode encontrá-lo em sua pasta 'Downloads'.\n" %nomeArquivoEscolhido +
              "Pressione 'enter' para retornar ao Meu Drive.")

        

    else: print("Desistiu do download.")
        

    
#############################################################################################################



def CriarConta(clientSocket):

    CabecalhoUI("Criar Conta")
    #clientSocket = ConectarSe()
    
    print("\n\n► Para criar uma conta, informe seus dados abaixo.")

    while True:
        nomeUsuario = LerString("Digite um nome de usuário:")

        while True:
            senhaUsuario = LerString("Crie uma senha:")
            confirmacaoSenha = LerString("Digite a mesma senha para confirmá-la:")

            if senhaUsuario != confirmacaoSenha:
                print("\nAs senhas digitadas são distintas. Tente cadastrá-la novamente.")

            else: break

        dictDadosAutenticacao = {nomeUsuario: senhaUsuario}

        # ENVIA DICIONARIO PARA SERVIDOR:
        dictDAJson = json.dumps(dictDadosAutenticacao)
        clientSocket.send(dictDAJson.encode("utf-8"))
        # ENVIADO - OK.

        # RECEBE INFORMAÇAO SE O USUARIO JA EXISTE:
        statusExistencia = clientSocket.recv(1024).decode("utf-8")
        # OK.

        if statusExistencia == "EXISTENTE":
            print("\nO nome de usuario já existe. Tente cadastrá-lo novamente.")

        elif statusExistencia == "INEXISTENTE": break
        
    # APENAS DEPOIS DE TER SAIDO DO LOOP, RECEBE INFORMAÇÃO SE O CADASTRO FOI FEITO OU NAO:
    statusCadastro = clientSocket.recv(1024).decode("utf-8")
    if statusCadastro == "SUCESSO":
        input("\n\nConta cadastrada com sucesso! Tecle 'enter' para acessar a tela de login.")

        ChamarServidor("AcessarConta()", clientSocket)       
        AcessarConta(clientSocket)

    elif statusCadastro == "ERRO":
        print("\n\nErro de cadastro. Reinicialize o programa.")
    # OK.


        
#############################################################################################################            

    

def AcessarConta(clientSocket):

    CabecalhoUI("Acessar Conta")
    #clientSocket = ConectarSe()

    print("\n\n► Para acessar sua conta, informe seus dados abaixo.")

    while True:
        nomeUsuario = LerString("Usuário:")
        senhaUsuario = LerString("Senha:")

        dictDadosAutenticacao = {nomeUsuario: senhaUsuario}

        # ENVIA DICIONARIO PARA SERVIDOR:
        dictDAJson = json.dumps(dictDadosAutenticacao)
        clientSocket.send(dictDAJson.encode("utf-8"))
        # ENVIADO - OK.

        # RECEBE INFORMAÇAO SE DADOS DO LOGIN ESTÃO CORRETOS OU NÃO:
        statusLogin = clientSocket.recv(1024).decode("utf-8")
        # OK.

        if statusLogin == "FALHA":
            print("\n\n► ► ► Usuário ou senha incorretos. Tente acessar novamente. ◄ ◄ ◄ \n")

        elif statusLogin == "LOGADO": break

    MenuPrincipal(nomeUsuario, clientSocket)



##############################################################################################################



def EnumerarLista(lista, textoIntroducao, textoComando):

    print("\n\n► " + textoIntroducao + "\n")

    for x in range(len(lista)):
        print(str(x + 1) + ") " + lista[x])

    numeroEscolhido = LerInteiro("\n" + textoComando, 1, len(lista))
    numeroPosicaoLista = (numeroEscolhido - 1)
    nomeConteudoEscolhido = lista[numeroPosicaoLista]
    

    return nomeConteudoEscolhido, numeroPosicaoLista



##############################################################################################################



def ExploradorDiretorio(diretorio):
    
    listaConteudoDir = (os.listdir("./" + diretorio))

    print("\n► Explorando o conteúdo do diretório local '%s'.\n" %diretorio.upper())

    for x in range(len(listaConteudoDir)):
        print(str(x + 1) + ") " + listaConteudoDir[x])

    return listaConteudoDir



##############################################################################################################



def UploadArquivo(nomeCliente, nomeDiretorio, nomePastaDestino, clientSocket):

    CabecalhoUI("Upload de Arquivo", nomeCliente)

    listaConteudoDir = ExploradorDiretorio("Disco Local") # Explora o root, inicialmente.
    historicoAcessoPasta = ""

    while True:
        escolhaUsuario = LerInteiro("\nSelecione a pasta ou o arquivo pelo seu respectivo número:", 1, len(listaConteudoDir))
        nomeConteudoEscolhido = listaConteudoDir[escolhaUsuario - 1]

        if os.path.isdir("./Disco Local/" + historicoAcessoPasta + nomeConteudoEscolhido) == True:
            listaConteudoDir = ExploradorDiretorio("Disco Local/" + historicoAcessoPasta + nomeConteudoEscolhido)
            historicoAcessoPasta += (nomeConteudoEscolhido + "/")

        else:
            input("\nDeseja fazer o upload do arquivo '%s' para a pasta '%s'?" %(nomeConteudoEscolhido, nomePastaDestino))
            break
    
    nomeDirCompleto = nomeDiretorio + "/" + nomePastaDestino
    clientSocket.send(nomeDirCompleto.encode("utf-8"))
    time.sleep(1)
    clientSocket.send(nomeConteudoEscolhido.encode("utf-8"))

    arquivoEnvio = open("./Disco Local/" + historicoAcessoPasta + nomeConteudoEscolhido, "rb")

    arquivoPronto = arquivoEnvio.read(1024)
    while arquivoPronto:
        clientSocket.send(arquivoPronto)
        arquivoPronto = arquivoEnvio.read(1024)

    arquivoEnvio.close()
    #clientSocket.close()

    input("\nUpload do arquivo '%s' feito com sucesso! Pressione 'enter' para retornar ao Menu Principal." %nomeConteudoEscolhido)

    #MenuPrincipal(nomeCliente)



##############################################################################################################



def CompartilharConteudo(nomeUsuario, nomeDiretorioRespectivo, nomeConteudoEscolhido, clientSocket):

    CabecalhoUI("Compartilhar Conteúdo", nomeUsuario)

    nomeDiretorioRespectivo += "/"

    # RECEBE LISTA DE USUÁRIOS CADASTRADOS E REMOVE DESTA LISTA O NOME DO USUÁRIO LOGADO
    listaUsuariosCadastrados_JS = clientSocket.recv(1024).decode("utf-8")
    listaUsuariosCadastrados = json.loads(listaUsuariosCadastrados_JS)
    listaUsuariosCadastrados.remove(nomeUsuario)
    # OK.

    nomeUsuarioACompartilhar, numeroPosicaoLista = EnumerarLista(listaUsuariosCadastrados,
                                           "Com qual usuário você gostaria de compartilhar o conteúdo '%s'?" %nomeConteudoEscolhido,
                                           "Selecione o nome do usuário pelo seu número correspondente:")
    
    dadosCompartilhamento = []
    dadosCompartilhamento.append(nomeUsuarioACompartilhar)
    dadosCompartilhamento.append(nomeConteudoEscolhido)
    dadosCompartilhamento.append(nomeDiretorioRespectivo)

    dadosCompartilhamento_JS = json.dumps(dadosCompartilhamento)
    clientSocket.send(dadosCompartilhamento_JS.encode("utf-8"))

    input("\nConteúdo '%s' foi compartilhado com sucesso com o usuário %s! " %(nomeConteudoEscolhido, nomeUsuarioACompartilhar) +
          "Tecle 'enter' para voltar ao Meu Drive.")
    
    
    

##############################################################################################################

    

def CriarPasta(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket):

    CabecalhoUI("Criar Pasta", nomeUsuario)

    nomeNovaPasta = LerString("► Digite o nome da nova pasta que deseja criar em '%s'." %nomeConteudoEscolhido)
    print(nomeDiretorio)
    print(nomeConteudoEscolhido)
    nomeDirCompleto = nomeDiretorio + "/" + nomeConteudoEscolhido

    clientSocket.send(nomeDirCompleto.encode("utf-8"))
    time.sleep(0.3)
    clientSocket.send(nomeNovaPasta.encode("utf-8"))

    input("\nPasta '%s' criada com sucesso! Pressione 'enter' para voltar ao Meu Drive." %nomeNovaPasta)



##############################################################################################################




def TratamentoConteudo(nomeUsuario, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket):

    if tipoConteudo == "PASTA":
        print("\n\n► O que você deseja fazer com a pasta '%s'?\n\n" %nomeConteudoEscolhido +
             "  ║ 1) Explorar\n" +
             "  ║ 2) Enviar arquivo\n" +
             "  ║ 3) Criar pasta\n" +
             "  ║ 4) Compartilhar")

        escolhaUsuario = LerInteiro("\nDigite o número referente à sua opção:", 1, 4)
        clientSocket.send(str(escolhaUsuario).encode("utf-8"))

        if escolhaUsuario == 1:
            pass

        elif escolhaUsuario == 2:
            UploadArquivo(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("MeuDrive()", clientSocket)
            MeuDrive(nomeUsuario, clientSocket)
                
                        
        elif escolhaUsuario == 3:
            CriarPasta(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("MeuDrive()", clientSocket)
            MeuDrive(nomeUsuario, clientSocket)
                
                        
        elif escolhaUsuario == 4:
            CompartilharConteudo(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("MeuDrive()", clientSocket)
            MeuDrive(nomeUsuario, clientSocket)
                


    elif tipoConteudo == "ARQUIVO":
        print("\n\n► O que você deseja fazer com o arquivo '%s'?\n\n" %nomeConteudoEscolhido +
              "  ║ 1) Download\n" +
              "  ║ 2) Compartilhar")

        escolhaUsuario = LerInteiro("\nDigite o número referente à sua opção:", 1, 2)
        clientSocket.send(str(escolhaUsuario).encode("utf-8"))
    
        if escolhaUsuario == 1: 
            DownloadArquivo(nomeUsuario, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("MeuDrive()", clientSocket)
            MeuDrive(nomeUsuario, clientSocket)
                

        if escolhaUsuario == 2:
            CompartilharConteudo(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("MeuDrive()", clientSocket)
            MeuDrive(nomeUsuario, clientSocket)

    

##############################################################################################################            
   


def MeuDrive(nomeUsuario, clientSocket):

    CabecalhoUI("Meu Drive", nomeUsuario)
    #clientSocket = ConectarSe()

    clientSocket.send(nomeUsuario.encode("utf-8"))

    while True:
        nomeDiretorio = clientSocket.recv(1024).decode("utf-8")
        listaConteudoDir_JS = clientSocket.recv(1024).decode("utf-8")
        listaConteudoDir = json.loads(listaConteudoDir_JS)
        

        nomeConteudoEscolhido, numeroPosicaoLista = EnumerarLista(listaConteudoDir,
                                                                  "Explorando o seu diretório online '%s':" %nomeDiretorio.upper(),
                                                                  "Selecione o conteúdo pelo seu respectivo número:")

        clientSocket.send(nomeConteudoEscolhido.encode("utf-8"))
        tipoConteudo = clientSocket.recv(1024).decode("utf-8")

        TratamentoConteudo(nomeUsuario, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
        

    
        


##############################################################################################################
     


def CompartilhadosComigo(nomeUsuario, clientSocket):

    CabecalhoUI("Compartilhados Comigo", nomeUsuario)
    #clientSocket = ConectarSe()

    clientSocket.send(nomeUsuario.encode("utf-8"))

    dadosCompartIndividual_JS = clientSocket.recv(1024).decode("utf-8")
    dadosCompartIndividual = json.loads(dadosCompartIndividual_JS)

    listaConteudoCompartilhado = dadosCompartIndividual[0]
    caminhoReferenteAoConteudo = dadosCompartIndividual[1]
    #nomeProprietario = caminhoReferenteAoConteudo[0].split("/")[0]
    
    
    nomeConteudoEscolhido, numeroPosicaoLista = EnumerarLista(listaConteudoCompartilhado,
                                                              "Conteúdo(s) compartilhado(s) com você:",
                                                              "Selecione o conteúdo pelo seu respectivo número:")

    nomeDirCompleto = caminhoReferenteAoConteudo[numeroPosicaoLista] + listaConteudoCompartilhado[numeroPosicaoLista]
    

    clientSocket.send(nomeDirCompleto.encode("utf-8"))
    tipoConteudo = clientSocket.recv(1024).decode("utf-8")
    
    
    if tipoConteudo == "ARQUIVO":
        nomeDiretorio = caminhoReferenteAoConteudo[numeroPosicaoLista]
        
        
        TratamentoConteudo(nomeUsuario, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
        
        
    else:    
        while True:
            nomeDiretorio = clientSocket.recv(1024).decode("utf-8") + "/"
            listaConteudoDir_JS = clientSocket.recv(1024).decode("utf-8")
            listaConteudoDir = json.loads(listaConteudoDir_JS)
                

            nomeConteudoEscolhido, numeroPosicaoLista = EnumerarLista(listaConteudoDir,
                                                                          "Explorando o diretório online compartilhado com você:",
                                                                          "Selecione o conteúdo pelo seu respectivo número:")

            clientSocket.send(nomeConteudoEscolhido.encode("utf-8"))
            tipoConteudo = clientSocket.recv(1024).decode("utf-8")
    

            TratamentoConteudo(nomeUsuario, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
    

        

      
    
    

    
     
    

MenuInicial(clientSocket)


#CompartilhadosComigo("Gabriel")

#MeuDrive("Gabriel")
#MenuPrincipal("Gabriel")
#Acoes("Gabriel")    
#MenuInicial()    
#AcessarConta()
#UploadArquivo("Folha")
#DownloadArquivo("Folha")
#CriarConta()
#ConectarSe()

