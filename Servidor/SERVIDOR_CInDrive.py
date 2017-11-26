#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
import os, json, time

serverSocket = socket(AF_INET, SOCK_STREAM)

serverHost = ""
serverPort = 800

serverSocket.bind((serverHost, serverPort))

print("\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ SERVIDOR | CIn DRIVE ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n")
print("▌ Servidor inicializado. Aguardando conexão...\n")

serverSocket.listen(20)

client, address = serverSocket.accept()

print("▌ O servidor está conectado a", address, "\n\n")
print("▌ Log de ocorrências internas:\n\n")

###############################################################################



def SERVIDOR_LinhaStatus(status):

    print("  ► %s \n" %status.upper())


def EscutaCliente():
   
    while True:
        
        solicitacaoCliente = client.recv(1024).decode("utf-8")

        SERVIDOR_LinhaStatus("Solicitação Cliente: %s" %solicitacaoCliente)

        if solicitacaoCliente == "CriarConta()":
            SERVIDOR_CriarConta()

        elif solicitacaoCliente == "AcessarConta()":
            SERVIDOR_AcessarConta()

        elif solicitacaoCliente == "MeuDrive()":
            SERVIDOR_MeuDrive()

        elif solicitacaoCliente == "CompartilhadosComigo()":
            SERVIDOR_CompartilhadosComigo()

        elif solicitacaoCliente == "Finalizar": break


    client.close()    


def SERVIDOR_CriarConta():
    
    arquivoSegurancaLeitura = open("./Sistema/Seguranca.json", "rb")
    leituraString = arquivoSegurancaLeitura.readline()
    leituraStringDecode = leituraString.decode() # PRECISA DECODAR PRA QUE A BIBLIOTECA JSON CONSIGA LER
    dictDadosUsuario = json.loads(leituraStringDecode) 
    arquivoSegurancaLeitura.close()

    arquivoPermissoesLeitura = open("./Sistema/Permissoes.json", "rb")
    arquivoPermissoesLeitura_STRING = arquivoPermissoesLeitura.readline()
    arquivoPermissoesLeitura_DECODE = arquivoPermissoesLeitura_STRING.decode()
    dictPermissoesUsuario = json.loads(arquivoPermissoesLeitura_DECODE) 
    arquivoPermissoesLeitura.close()


    while True: 
        dictDadosAutenticacao_JS = client.recv(1024).decode("utf-8")
        dictDadosAutenticacao = json.loads(dictDadosAutenticacao_JS)
            
        for x in dictDadosAutenticacao: # COLETA APENAS O NOME DO USUARIO QUE ESTA NO DICIONARIO
            nomeUsuario = x

        if nomeUsuario in dictDadosUsuario:
            statusExistencia = "EXISTENTE"
            client.send(statusExistencia.encode("utf-8"))

        else: break
                        

    try:
        statusExistencia = "INEXISTENTE" # TEM COMO ENVIAR UM BOOL AO INVÉS DE STR?
        client.send(statusExistencia.encode("utf-8"))
                    
        arquivoSegurancaEscrita = open("./Sistema/Seguranca.json", "wb")
        dictDadosUsuario.update(dictDadosAutenticacao)
        dictAtualizado = json.dumps(dictDadosUsuario, ensure_ascii = False)
        arquivoSegurancaEscrita.write(dictAtualizado.encode())
        arquivoSegurancaEscrita.close()

        pastaPadroes = ["Documentos", "Imagens", "Músicas", "Atividades", "Quaisquer"]

        for nomePasta in pastaPadroes:
            diretorio = ""
            diretorio += nomeUsuario + "/" + nomePasta

            os.makedirs("./Usuários/" + diretorio)

        arquivoPermissoesEscrita = open("./Sistema/Permissoes.json", "wb")
        dictConteudoPermitido = {nomeUsuario : [[], []]}
        dictPermissoesUsuario.update(dictConteudoPermitido)
        dictConteudoPermitido_JS = json.dumps(dictPermissoesUsuario, ensure_ascii = False)
        arquivoPermissoesEscrita.write(dictConteudoPermitido_JS.encode())
        arquivoPermissoesEscrita.close()

        SERVIDOR_LinhaStatus("Novo usuário '%s' cadastrado" %nomeUsuario)
        statusCadastro = "SUCESSO"
        client.send(statusCadastro.encode("utf-8"))

        EscutaCliente()
    
    except:
        SERVIDOR_LinhaStatus("Erro inesperado")
        statusCadastro = "ERRO"
        client.send(statusCadastro.encode("utf-8"))
        

###############################################################################


def SERVIDOR_AcessarConta():

    arquivoSegurancaLeitura = open("./Sistema/Seguranca.json", "rb")
    leituraString = arquivoSegurancaLeitura.readline()
    leituraStringDecode = leituraString.decode()
    dictDadosUsuario = json.loads(leituraStringDecode) 
    arquivoSegurancaLeitura.close()

    while True:
        dadosAutenticacaoJS = client.recv(1024).decode("utf-8") # RECEBE OS DADOS DE AUTENTICAÇÃO DO CLIENTE {NOME: SENHA}
        dictDadosAutenticacao = json.loads(dadosAutenticacaoJS)

        for x in dictDadosAutenticacao:
            nomeUsuario = x

        senhaUsuario = dictDadosAutenticacao[nomeUsuario]

        if (nomeUsuario in dictDadosUsuario) and (senhaUsuario == dictDadosUsuario[nomeUsuario]):
            SERVIDOR_LinhaStatus("Usuário '%s' logado" %nomeUsuario)
            statusLogin = "LOGADO"
            client.send(statusLogin.encode("utf-8"))
            break
            
        else:
            SERVIDOR_LinhaStatus("Falha na autenticação — dados incorretos")
            statusLogin = "FALHA"
            client.send(statusLogin.encode("utf-8"))
            
    
            
            

def SERVIDOR_UploadArquivo():


    nomeDirCompleto = client.recv(1024).decode("utf-8") # RECEBE O NOME COMPLETO DO DIRETORIO PRA ONDE VAI O ARQUIVO
    nomeArquivo = client.recv(1024).decode("utf-8")

    arquivoBaixadoServidor = open("./Usuários/" + nomeDirCompleto + "/" + nomeArquivo, "wb")

    bytesRecebidos = client.recv(1024)
    while bytesRecebidos:
        arquivoBaixadoServidor.write(bytesRecebidos)
        bytesRecebidos = client.recv(1024)
    arquivoBaixadoServidor.close()

    SERVIDOR_LinhaStatus("Arquivo '%s' recebido com sucesso" %nomeArquivo)

    


def SERVIDOR_DownloadArquivo(nomeDiretorio):

    confirmacaoDownload = client.recv(1024).decode("utf-8") # RECEBE "S" OU "N".

    if confirmacaoDownload == "S":

        arquivoRequisitado = open("./Usuários/" + nomeDiretorio, "rb")

        bytesEnviados = arquivoRequisitado.read(1024)
        while bytesEnviados:
            client.send(bytesEnviados)
            bytesEnviados = arquivoRequisitado.read(1024)
        arquivoRequisitado.close()

        SERVIDOR_LinhaStatus("Arquivo enviado com sucesso")

    else: SERVIDOR_LinhaStatus("Envio cancelado pelo usuário")
    


def SERVIDOR_CompartilharConteudo(): # DAVY, VOU OTIMIZAR ESSA FUNÇÃO, MAS ELA COLETA O DICIONARIO {NOME : []}, ONDE A LISTA
                                     # COLETA O CONTEUDO QUE O USUÁRIO PODE ACESSAR/BAIXAR/ETC

    arquivoPermissoesLeitura = open("./Sistema/Permissoes.json", "rb")
    arquivoPermissoesLeitura_STRING = arquivoPermissoesLeitura.readline()
    arquivoPermissoesLeitura_DECODE = arquivoPermissoesLeitura_STRING.decode()
    dictPermissoesUsuario = json.loads(arquivoPermissoesLeitura_DECODE) 
    arquivoPermissoesLeitura.close()

    listaUsuariosCadastrados = []

    for usuariosCadastrados in dictPermissoesUsuario:
        listaUsuariosCadastrados.append(usuariosCadastrados)

    # ENVIA LISTA DE USUÁRIOS CADASTRADOS:    
    listaUsuariosCadastrados_JS = json.dumps(listaUsuariosCadastrados)
    client.send(listaUsuariosCadastrados_JS.encode("utf-8"))
    # OK.

    dadosCompartilhamento_JS = client.recv(1024).decode("utf-8")
    dadosCompartilhamento = json.loads(dadosCompartilhamento_JS)

    nomeUsuarioACompartilhar = dadosCompartilhamento[0]
    nomeConteudoEscolhido = dadosCompartilhamento[1]
    nomeDiretorioRespectivo = dadosCompartilhamento[2]

    listaConteudoEscolhido = dictPermissoesUsuario[nomeUsuarioACompartilhar][0]
    listaDiretorioRespectivo = dictPermissoesUsuario[nomeUsuarioACompartilhar][1]


    if (nomeConteudoEscolhido not in listaConteudoEscolhido) and (listaDiretorioRespectivo not in listaDiretorioRespectivo):
        listaConteudoEscolhido.append(nomeConteudoEscolhido)
        listaDiretorioRespectivo.append(nomeDiretorioRespectivo)

    listaDadosCompartilhamento = []
    listaDadosCompartilhamento.append(listaConteudoEscolhido)
    listaDadosCompartilhamento.append(listaDiretorioRespectivo)
    dictConteudoPermitido = {nomeUsuarioACompartilhar : listaDadosCompartilhamento} # Atualiza o dicionário 

    arquivoPermissoesEscrita = open("./Sistema/Permissoes.json", "wb")
    dictPermissoesUsuario.update(dictConteudoPermitido)
    dictConteudoPermitido_JS = json.dumps(dictPermissoesUsuario, ensure_ascii = False)
    arquivoPermissoesEscrita.write(dictConteudoPermitido_JS.encode())
    arquivoPermissoesEscrita.close()
    

    


def SERVIDOR_CriarPasta():

    nomeDirCompleto = client.recv(1024).decode("utf-8")
    nomeNovaPasta = client.recv(1024).decode("utf-8")

    os.makedirs("./Usuários/" + nomeDirCompleto + "/" + nomeNovaPasta)

    

def SERVIDOR_TratamentoConteudo(nomeDiretorio, arquivo):

    if os.path.isdir("Usuários/" + nomeDiretorio + "/") == True:
        msgTipoConteudo = "PASTA"
        client.send(msgTipoConteudo.encode("utf-8"))

        escolhaUsuario = client.recv(1024).decode("utf-8")

        if escolhaUsuario == "1":
            pass

        elif escolhaUsuario == "2": 
            SERVIDOR_UploadArquivo()
            EscutaCliente()

        elif escolhaUsuario == "3":
            SERVIDOR_CriarPasta()
            EscutaCliente()
            
        elif escolhaUsuario == "4":
            SERVIDOR_CompartilharConteudo()
            EscutaCliente()
            
    else:

        if arquivo == False:
            msgTipoConteudo = "ARQUIVO"
            client.send(msgTipoConteudo.encode("utf-8"))
            time.sleep(0.5)

        escolhaUsuario = client.recv(1024).decode("utf-8")

        if escolhaUsuario == "1":
            SERVIDOR_DownloadArquivo(nomeDiretorio)
            EscutaCliente()
            
        elif escolhaUsuario == "2":
            SERVIDOR_CompartilharConteudo()
            EscutaCliente()
            


def SERVIDOR_MeuDrive():

    nomeUsuario = client.recv(1024).decode("utf-8")
    nomeDiretorio = nomeUsuario # Para que explore primeiro a pasta inicial do usuário.

    while True:
        listaConteudoDir = os.listdir("Usuários/" + nomeDiretorio)
        
        client.send(nomeDiretorio.encode("utf-8"))
        time.sleep(0.7)
        listaConteudoDir_JS = json.dumps(listaConteudoDir)
        client.send(listaConteudoDir_JS.encode("utf-8"))
        
        nomeConteudoEscolhido = client.recv(1024).decode("utf-8")
        nomeDiretorio += "/" + nomeConteudoEscolhido
    
        SERVIDOR_TratamentoConteudo(nomeDiretorio, arquivo = False)
        

        


def SERVIDOR_CompartilhadosComigo():

    arquivoPermissoesLeitura = open("./Sistema/Permissoes.json", "rb")
    arquivoPermissoesLeitura_STRING = arquivoPermissoesLeitura.readline()
    arquivoPermissoesLeitura_DECODE = arquivoPermissoesLeitura_STRING.decode()
    dictPermissoesUsuario = json.loads(arquivoPermissoesLeitura_DECODE) 
    arquivoPermissoesLeitura.close()

    nomeUsuario = client.recv(1024).decode("utf-8")

    dadosCompartIndividual = dictPermissoesUsuario[nomeUsuario]
    
    dadosCompartIndividual_JS = json.dumps(dadosCompartIndividual)
    client.send(dadosCompartIndividual_JS.encode("utf-8"))

    nomeDirCompleto = client.recv(1024).decode("utf-8")
    
    
    if os.path.isfile("Usuários/" + nomeDirCompleto) == True:

        msgTipoConteudo = "ARQUIVO"
        client.send(msgTipoConteudo.encode("utf-8"))
        time.sleep(0.3)

        SERVIDOR_TratamentoConteudo(nomeDirCompleto, arquivo = True)

    else:
        msgTipoConteudo = "PASTA"
        client.send(msgTipoConteudo.encode("utf-8"))
        time.sleep(0.3)
    
        while True:

            listaConteudoDir = os.listdir("Usuários/" + nomeDirCompleto + "/")
                
            client.send(nomeDirCompleto.encode("utf-8"))
            time.sleep(0.7)
            listaConteudoDir_JS = json.dumps(listaConteudoDir)
            client.send(listaConteudoDir_JS.encode("utf-8"))
                
            nomeConteudoEscolhido = client.recv(1024).decode("utf-8")
            nomeDirCompleto += nomeConteudoEscolhido + "/" 
                
            SERVIDOR_TratamentoConteudo(nomeDirCompleto, arquivo = False)





EscutaCliente()
        


