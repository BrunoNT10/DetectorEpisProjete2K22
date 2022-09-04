from sys import maxsize
import pyrebase
import cv2
import json
from cv2 import *
from datetime import *
import pandas as pd
import os
from tkinter import *
import tkinter as tk

config = {
    "apiKey": "AIzaSyDVyPsRvmfFwH3hASMeqLrpMElyeP48RRw",
    "authDomain": "projete-2022.firebaseapp.com",
    "databaseURL": "https://projete-2022-default-rtdb.firebaseio.com",
    "projectId": "projete-2022",
    "storageBucket": "projete-2022.appspot.com",
    "messagingSenderId": "392429305078",
    "appId": "1:392429305078:web:31e7a9605638bbc20380d7",
    "measurementId": "G-31C7LKYKWP"
}

firebase = pyrebase.initialize_app(config)

# ---------- ANALISA O JSON PARA SABER A EMPRESA ----------

def ReceberNomeEmpresa():
    nome_empresa = input("Digite o nome da sua empresa: ")
    return nome_empresa

with open('config/config.json', encoding='utf-8') as meu_json:
    ler_config = json.load(meu_json)

empresa = ler_config['empresa']

if(empresa == ""):
    empresa = ReceberNomeEmpresa()

    json_nome_empresa = {"empresa": empresa}

    object_json_nome_empresa = json.dumps(json_nome_empresa, indent=4)

    with open("config/config.json", "w") as arquivo_nome_empresa:
        arquivo_nome_empresa.write(object_json_nome_empresa)
        print("Nome da empresa salvo com sucesso!")

# ---------- IDENTIFICAÇÃO DO FUNCIONÁRIO ----------

def AbrirCamera():

    camera = cv2.VideoCapture(0)

    return camera

def BuscarData():
    date_today = datetime.now()
    dia = date_today.day
    mes = date_today.month
    ano = date_today.year

    data_completa = str(dia) + "/" + str(mes) + "/" + str(ano)

    return data_completa

def BuscarDataArquivoImagem():
    date_today = datetime.now()
    dia = date_today.day
    mes = date_today.month
    ano = date_today.year

    data_completa = str(dia) + "-" + str(mes) + "-" + str(ano)

    return data_completa

def EnviarArquivosFirebase(nome_arquivo_imagem, nome_arquivo_excel, nome_arquivo_imagem_firebase, nome_arquivo_excel_firebase):
    firebase_storage = firebase.storage()

    local_imagem_firebase = "Imagens/" + nome_arquivo_imagem_firebase
    local_arquivos_excel_firebase = "ArquivosExcel/" + nome_arquivo_excel_firebase

    try:
        firebase_storage.child(local_imagem_firebase).put(nome_arquivo_imagem)
        firebase_storage.child(local_arquivos_excel_firebase).put(nome_arquivo_excel)
        return True

    except:
        return False
   
def CriarNomeArquivos(nome_funcionario, data):
    nome_arquivo_imagem = "img/" + nome_funcionario + data + ".png"
    nome_arquivo_imagem_firebase = nome_funcionario + data + ".png"
    nome_arquivo_excel = "data/" + nome_funcionario + ".xlsx"
    nome_arquivo_excel_firebase = nome_funcionario + ".xlsx"

    return nome_arquivo_imagem, nome_arquivo_excel, nome_arquivo_imagem_firebase, nome_arquivo_excel_firebase

def DefinirTempoInicial():
    momento_inicial = datetime.now()
    segundos_inicio = momento_inicial.second
    print("Verificação INICIADA no segundo ", segundos_inicio)
    return segundos_inicio

def DefinirTempoExecucao():
    momento_execucao = datetime.now()
    segundos_execucao = momento_execucao.second
    return segundos_execucao + 1

def CriarListaOrdenadaEpisEncontradas(json_epis_encontradas):
    lista_epis_encontradas = []

    lista_epis_encontradas.append(json_epis_encontradas["botas"])
    lista_epis_encontradas.append(json_epis_encontradas["capacete"])
    lista_epis_encontradas.append(json_epis_encontradas["colete"])
    lista_epis_encontradas.append(json_epis_encontradas["luvas"])
    lista_epis_encontradas.append(json_epis_encontradas["mascara"])
    lista_epis_encontradas.append(json_epis_encontradas["pa"])

    return lista_epis_encontradas

def CriarTabelaExcel(json_epis_encontradas, nome_arquivo_excel):

    print(json_epis_encontradas)

    data_completa = BuscarData()

    dir_inicial = os.getcwd()

    os.chdir("data")

    lista_arquivos_criados = os.listdir()

    os.chdir(dir_inicial) 

    arquivo_criado = False

    for arquivo in lista_arquivos_criados:
        arquivo = "data/" + arquivo
        if(nome_arquivo_excel == arquivo):
            arquivo_criado = True

    if(arquivo_criado == False):
        dataframe_epis = pd.DataFrame({data_completa: json_epis_encontradas})

        print(dataframe_epis)

        dataframe_epis.to_excel(nome_arquivo_excel)

    elif(arquivo_criado == True):
        dataframe_epis = pd.read_excel(nome_arquivo_excel, engine="openpyxl")

        lista_epis_encontradas = CriarListaOrdenadaEpisEncontradas(json_epis_encontradas)

        dataframe_epis[data_completa] = lista_epis_encontradas

        try:
            dataframe_epis.drop(columns=("Unnamed: 0.1"))
            excluir_linha_extra = True
        
        except: 
            excluir_linha_extra = False

        if(excluir_linha_extra):
            dataframe_epis = dataframe_epis.drop(columns="Unnamed: 0")

        print(dataframe_epis)
        
        dataframe_epis.to_excel(nome_arquivo_excel)

def IdentificarEPIS(nome_funcionario, lista_epis_necessarias):
    print("Iniciando a identificação das EPIS...")

    camera = AbrirCamera()

    data = BuscarDataArquivoImagem()

    nome_arquivo_imagem, nome_arquivo_excel, nome_arquivo_imagem_firebase, nome_arquivo_excel_firebase = CriarNomeArquivos(nome_funcionario, data)
    print(nome_arquivo_imagem, "+ ", nome_arquivo_excel)

    # CÓDIGO PARA ADICIONAR OS HAARCASCADES
    cascade_capacete = cv2.CascadeClassifier("cascades/cascade_capacete.xml")
    cascade_luvas = cv2.CascadeClassifier("cascades/cascade_luvas.xml")
    cascade_colete = cv2.CascadeClassifier("cascades/cascade_colete.xml")
    cascade_pa = cv2.CascadeClassifier("cascades/cascade_pa.xml")
    cascade_botas = cv2.CascadeClassifier("cascades/cascade_botas.xml")
    cascade_mascara = cv2.CascadeClassifier("cascades/cascade_mascara.xml")

    # FIM DO CÓDIGO PARA ADICIONAR OS HAARCASCADES 

    capacete_necessario, luvas_necessario, botas_necessario, mascara_necessario, pa_necessario, colete_necessario = False, False, False, False, False, False
    capacete_detectado, luvas_detectado, botas_detectado, mascara_detectado, pa_detectado, colete_detectado = False, False, False, False, False, False
    epis_encontradas = False

    for x in lista_epis_necessarias:
        if(x == "capacete"):
            capacete_necessario = True
        
        elif(x == "luvas"):
            luvas_necessario = True

        elif(x == "botas"):
            botas_necessario = True
        
        elif(x == "oculos"):
            mascara_necessario = True

        elif(x == "pa"):
            pa_necessario = True

        elif(x == "colete"):
            colete_necessario = True

    numero_epis_verificacao = len(lista_epis_necessarias)
    print(lista_epis_necessarias)

    tempo_inicio_while = DefinirTempoInicial()

    while True:
        _, video = camera.read()

        tempo_execucao_while = DefinirTempoExecucao()

        if(tempo_execucao_while == tempo_inicio_while):
            cv2.imwrite(nome_arquivo_imagem, video)
            epis_encontradas = False
            break
        
        video = cv2.resize(video, (800, 600))
        video = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
        video_detectar_capacete = video[0:200, 300:500]
        video_detectar_luvas = video[200:400, 0:800]
        video_detectar_botas = video[400:600, 0:800]

        if(capacete_necessario and capacete_detectado == False):

            # print("Buscando capacete...")
            deteccao_capacete = cascade_capacete.detectMultiScale(video_detectar_capacete, scaleFactor=1.02, minNeighbors=10)
            # print("capacete: ", deteccao_capacete)
            for(w, x, y, z) in deteccao_capacete:
                cv2.rectangle(video_detectar_capacete, (w, x), (w + y, x + z), (0, 255, 0), 2)

            if(deteccao_capacete != ()):
                # print("Capacete detectado!")
                print("capacete")

                capacete_detectado = True
                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                capacete_detectado = False
            
        if(luvas_necessario and luvas_detectado == False):

            # print("Buscando luvas...")
            deteccao_luvas = cascade_luvas.detectMultiScale(video_detectar_luvas, scaleFactor=1.02, minNeighbors=10)

            # print("luvas: ", deteccao_luvas)

            for(w, x, y, z) in deteccao_luvas:
                cv2.rectangle(video_detectar_luvas, (w, x), (w + y, x + z), (0, 0, 255), 2)

            if(deteccao_luvas != ()):
                # print("luvas detectado!")
                luvas_detectado = True
                print("Luvas")
                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                luvas_detectado = False
        
        if(colete_necessario and colete_detectado == False):

            deteccao_colete = cascade_colete.detectMultiScale(video_detectar_luvas, scaleFactor=1.02, minNeighbors=10)

            # print("colete: ", deteccao_colete)

            for(w, x, y, z) in deteccao_colete:
                cv2.rectangle(video_detectar_luvas, (w, x), (w + y, x + z), (255, 0, 0), 2)

            if(deteccao_colete != ()):
                # print("colete detectado!")
                print("Colete")
                colete_detectado = True
                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                colete_detectado = False

        if(mascara_necessario and mascara_detectado == False):

            deteccao_mascara = cascade_mascara.detectMultiScale(video_detectar_capacete, scaleFactor=1.02, minNeighbors=10)

            # print("colete: ", deteccao_mascara)

            for(w, x, y, z) in deteccao_mascara:
                cv2.rectangle(video_detectar_capacete, (w, x), (w + y, x + z), (255, 0, 0), 2)

            if(deteccao_mascara != ()):
                # print("mascara detectado!")
                mascara_detectado = True
                print("mascara")

                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                mascara_detectado = False

        if(pa_necessario and pa_detectado == False):

            deteccao_pa = cascade_pa.detectMultiScale(video_detectar_capacete, scaleFactor=1.02, minNeighbors=10)

            for(w, x, y, z) in deteccao_pa:
                cv2.rectangle(video_detectar_capacete, (w, x), (w + y, x + z), (255, 0, 255), 2)

            if(deteccao_pa != ()):
                # print("pa detectado!")
                pa_detectado = True
                print("pa")

                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                pa_detectado = False

        if(botas_necessario and botas_detectado == False):

            deteccao_botas = cascade_botas.detectMultiScale(video_detectar_botas, scaleFactor=1.02, minNeighbors=10)

            for(w, x, y, z) in deteccao_botas:
                cv2.rectangle(video_detectar_botas, (w, x), (w + y, x + z), (255, 0, 255), 2)

            if(deteccao_botas != ()):
                # print("botas detectado!")
                botas_detectado = True
                print("botas")

                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                botas_detectado = False
            
        if(cv2.waitKey(1) == ord("q")):
            cv2.imwrite(nome_arquivo_imagem, video)
            break

        if(numero_epis_verificacao == 0):
            cv2.imwrite(nome_arquivo_imagem, video)
            print("Todas as epis foram encontradas!!!!!")
            break

        cv2.imshow("Identificação funcionário", video)
        cv2.imshow("Video detecção capacete", video_detectar_capacete)
        cv2.imshow("Video detecção colete", video_detectar_luvas)
        cv2.imshow("Video detectar botas", video_detectar_botas)

    camera.release()

    cv2.destroyAllWindows()
    
    # CÓDIGO PARA CRIAR O DICIONÁRIO DAS EPIS ENCONTRADAS

    json_epis_encontradas = {}

    if(capacete_necessario):
        if(capacete_detectado):
            json_epis_encontradas["capacete"] = "sim"

        else:
            json_epis_encontradas["capacete"] = "não"

    else:
        json_epis_encontradas["capacete"] = "-"

    if(mascara_necessario):
        if(mascara_detectado):
            json_epis_encontradas["mascara"] = "sim"

        else:
            json_epis_encontradas["mascara"] = "não"

    else:
        json_epis_encontradas["mascara"] = "-"

    if(luvas_necessario):
        if(luvas_detectado):
            json_epis_encontradas["luvas"] = "sim"

        else:
            json_epis_encontradas["luvas"] = "não"

    else:
        json_epis_encontradas["luvas"] = "-"

    if(colete_necessario):
        if(colete_detectado):
            json_epis_encontradas["colete"] = "sim"

        else:
            json_epis_encontradas["colete"] = "não"

    else:
        json_epis_encontradas["colete"] = "-"
    
    if(botas_necessario):
        if(botas_detectado):
            json_epis_encontradas["botas"] = "sim"

        else:
            json_epis_encontradas["botas"] = "não"

    else:
        json_epis_encontradas["botas"] = "-"

    if(pa_necessario):
        if(pa_detectado):
            json_epis_encontradas["pa"] = "sim"

        else:
            json_epis_encontradas["pa"] = "não"

    else:
        json_epis_encontradas["pa"] = "-"


    print(json_epis_encontradas)

    # FIM DO CÓDIGO PARA CRIAR O DICIONÁRIO DAS EPIS ENCONTRADAS

    CriarTabelaExcel(json_epis_encontradas, nome_arquivo_excel)

    resposta_envio_arquivos_firebase = EnviarArquivosFirebase(nome_arquivo_imagem, nome_arquivo_excel, nome_arquivo_imagem_firebase, nome_arquivo_excel_firebase)

    if(resposta_envio_arquivos_firebase):
        print("Arquivos enviados com SUCESSO!!!!!")

    else:
        print("Erro ao enviar arquivos para o firebase storage!!!!!")

    return True

def CriarListaEpisNecessarias(epis_necessarias):
    lista_epis_necessarias = []
    if(epis_necessarias['capacete']):
        lista_epis_necessarias.append("capacete")

    if(epis_necessarias['luvas']):
        lista_epis_necessarias.append("luvas")
        
    if(epis_necessarias['colete']):
        lista_epis_necessarias.append("colete")

    if(epis_necessarias['oculos']):
        lista_epis_necessarias.append("oculos")

    if(epis_necessarias['pa']):
        lista_epis_necessarias.append("pa")

    if(epis_necessarias['botas']):
        lista_epis_necessarias.append("botas")

    return lista_epis_necessarias

def BuscarFuncionario(nome_funcionario):
    db = firebase.database()
    print("Conexão ao banco de dados efetuada com sucesso!")
    base_dados_funcionario = empresa+"/funcionarios/"+nome_funcionario

    dados_funcionario = db.child(base_dados_funcionario).get()

    try:
        teste_atencao_necessario = dados_funcionario.val()['teste']
        setor = dados_funcionario.val()['setor']
    except:
        print("Funcionário não cadastrado nos bancos de dados da empresa...")
        return

    base_dados_epis_funcionarios = empresa+"/setores/"+setor+"/epis"

    dados_epis = db.child(base_dados_epis_funcionarios).get()
    epis_necessarias = dados_epis.val()

    lista_epis_necessarias = CriarListaEpisNecessarias(epis_necessarias)

    if(teste_atencao_necessario):
        teste_atencao_realizado = dados_funcionario.val()['teste_realizado']
        if(teste_atencao_realizado):
            IdentificarEPIS(nome_funcionario, lista_epis_necessarias)

        else:
            print("Realize o teste!")
            return
    else:
        IdentificarEPIS(nome_funcionario, lista_epis_necessarias)

    return

def UsarDeteccaoFacial():
    print("Usar deteccção facial")
    nome_funcionario = input("Digite o nome do funcionário: ")
    BuscarFuncionario(nome_funcionario)
    
def UsarBiometria():
    print("Usar biometria")
    nome_funcionario = input("Digite o nome do funcionário: ")
    BuscarFuncionario(nome_funcionario)

def UsarRFID():
    print("Usar RFID")
    nome_funcionario = input("Digite o nome do funcionário: ")
    BuscarFuncionario(nome_funcionario)

janela = tk.Tk()

janela.title("Modo de identificação")

janela.geometry("200x130+600+200")

janela["bg"] = "light blue"

LabelJanela = Label(janela, text="Selecione o modo de \n identificação que será utilizado: ")
LabelJanela.pack(side=TOP)

LabelJanela["bg"] = "light blue"

ButtonDeteccaoFacial = Button(janela, text="Detecção Facial", command=UsarDeteccaoFacial)
ButtonDeteccaoFacial.pack(side=TOP)

ButtonBiometria = Button(janela, text="Biometria", command=UsarBiometria)
ButtonBiometria.pack(side=TOP)

ButtonRFID = Button(janela, text="RFID", command=UsarRFID)
ButtonRFID.pack(side=TOP)

janela.mainloop()





    

