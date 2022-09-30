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
import serial
from time import sleep
from operator import truediv
from turtle import width
import pandas as pd 
import pyautogui as pg
import time 
import webbrowser as web

font = cv2.FONT_HERSHEY_COMPLEX_SMALL


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

# ---------- IDENTIFICAÇÃO DO FUNCIONÁRIO ----------

def AbrirCamera():

    camera = cv2.VideoCapture(1)

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
        
        dataframe_epis.to_excel(nome_arquivo_excel)

def EnviarJsonFirebase(nome_empresa, nome_funcionario, data, epis_encontradas):
    db = firebase.database()

    path_firebase = nome_empresa + "/json_funcionarios/" + nome_funcionario
    valor_json_funcionario = {data: epis_encontradas}

    db.child(path_firebase).update(valor_json_funcionario)

def EnviarWhatsapp(nome_funcionario):
    data = pd.read_csv("arquivo_csv/Lista_numeros_pesquisa_sk.csv", sep=";")
# data

#fazendo o envio
    data_dict = data.to_dict('list')

    leads = data_dict['WhatsApp']
    messages = data_dict['msg']
    combo = zip(leads,messages)
    first = True
    for lead, message in combo:
        time.sleep(4)
        message = "Funcionário {} não está usando todas as EPI's".format(nome_funcionario)
        web.open("https://web.whatsapp.com/send?phone="+lead+"&text="+message)
        if first:
            time.sleep(6)
            first=False
        width,height = pg.size()
        pg.click(width/2,height/2)
        time.sleep(8)
        pg.press('esc')
        time.sleep(5)
        pg.press('enter')
        time.sleep(10)
        pg.hotkey('ctrl', 'w')

def IdentificarEPIS(nome_funcionario, lista_epis_necessarias):

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
    todas_epis_encontradas = False

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

    tempo_inicio_while = DefinirTempoInicial()

    num_deteccao_capacete, num_deteccao_luvas, num_deteccao_botas, num_deteccao_pa, num_deteccao_mascara, num_deteccao_colete = 0, 0, 0, 0, 0, 0 

    todas_epis_detectadas = False

    while True:
        _, video = camera.read()

        tempo_execucao_while = DefinirTempoExecucao()

        if(tempo_execucao_while == tempo_inicio_while):
            cv2.imwrite(nome_arquivo_imagem, video)
            epis_encontradas = False
            break
        
        video = cv2.resize(video, (800, 600))
        video = cv2.rectangle(video, (300, 0), (500, 200), (0, 0, 0), 2)
        video = cv2.rectangle(video, (0, 200), (800, 400), (0, 0, 0), 2)
        video = cv2.rectangle(video, (0, 400), (800, 600), (0, 0, 0), 2)
        
        video = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
        video_detectar_capacete = video[0:200, 300:500]
        # video_detectar_capacete = cv2.resize(video_detectar_capacete, (800, 800))

        video_detectar_luvas = video[200:400, 0:800]
        # video_detectar_luvas = cv2.resize(video_detectar_luvas, (1600, 400))
        video_detectar_botas = video[400:600, 0:800]
        # video_detectar_botas = cv2.resize(video_detectar_botas, (400, 1600))

        if(capacete_necessario and capacete_detectado == False):

            deteccao_capacete = cascade_capacete.detectMultiScale(video_detectar_capacete, scaleFactor=1.02, minNeighbors=10, minSize=(30,30))

            for(w, x, y, z) in deteccao_capacete:
                # w = int(w/4)
                # z = int(z/4)
                # x = int(x/4)
                # y = int(y/4)
                cv2.rectangle(video, (w + 300, x), (w + y + 300, x + z), (255, 255, 255), 2)
                cv2.putText(video, str("CAPACETE"), (w + 300, x + z + 20), font, 1, (255, 255, 255))

            if(deteccao_capacete != ()):

                num_deteccao_capacete = num_deteccao_capacete + 1

                print("capacete")
            
            if(num_deteccao_capacete == 20):
                capacete_detectado = True
                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                capacete_detectado = False

        if(luvas_necessario and luvas_detectado == False):

            deteccao_luvas = cascade_luvas.detectMultiScale(video_detectar_luvas, scaleFactor=1.02, minNeighbors=10, minSize=(20, 20))

            for(w, x, y, z) in deteccao_luvas:
                # w = int(w/2)
                # z = int(z/2)
                # y = int(y/2)
                # x = int(x/2)
                cv2.rectangle(video, (w, x + 200), (w + y, x + z + 200), (255, 255, 255), 2)
                cv2.putText(video, str("LUVA"), (w, x + z + 220), font, 1, (255, 255, 255))


            if(deteccao_luvas != ()):
                num_deteccao_luvas = num_deteccao_luvas + 1

                print("Luvas")
            
            if(num_deteccao_luvas == 20):
                luvas_detectado = True
                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                luvas_detectado = False

        if(colete_necessario and colete_detectado == False):

            deteccao_colete = cascade_colete.detectMultiScale(video_detectar_luvas, scaleFactor=1.02, minNeighbors=10)

            # print("colete: ", deteccao_colete)

            for(w, x, y, z) in deteccao_colete:
                cv2.rectangle(video, (w, x), (w + y, x + z), (255, 255, 255), 2)
                # w = int(w/2)
                # z = int(z/2)
                # y = int(y/2)
                # x = int(x/2)
                # cv2.rectangle(video, (w, x + 200), (w + y, x + z + 200), (0, 0, 255), 2)
                cv2.putText(video, str("COLETE"), (w, x + z + 220), font, 1, (255, 255, 255))

            if(deteccao_colete != ()):
                # print("colete detectado!")
                print("Colete")
                num_deteccao_colete = num_deteccao_colete + 1
            
            if(num_deteccao_colete == 20):
                colete_detectado = True
                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                colete_detectado = False
            
        if(mascara_necessario and mascara_detectado == False):

            deteccao_mascara = cascade_mascara.detectMultiScale(video_detectar_capacete, scaleFactor=1.02, minNeighbors=10)

            # print("colete: ", deteccao_mascara)

            for(w, x, y, z) in deteccao_mascara:
                # w = int(w/4)
                # z = int(z/4)
                # x = int(x/4)
                # y = int(y/4)
                cv2.rectangle(video, (w + 300, x), (w + y + 300, x + z), (255, 255, 255), 2)
                cv2.putText(video, str("MASCARA"), (w + 300, x + z + 20), font, 1, (255, 255, 255))

            if(deteccao_mascara != ()):
                # print("mascara detectado!")
                print("mascara")

                num_deteccao_mascara = num_deteccao_mascara + 1

            if(num_deteccao_mascara == 20):
                mascara_detectado = True
                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                mascara_detectado = False

        if(pa_necessario and pa_detectado == False):

            deteccao_pa = cascade_pa.detectMultiScale(video_detectar_capacete, scaleFactor=1.02, minNeighbors=10)

            # for(w, x, y, z) in deteccao_pa:
            #     cv2.rectangle(video, (w, x), (w + y, x + z), (255, 0, 255), 2)

            if(deteccao_pa != ()):
                # print("pa detectado!")

                num_deteccao_pa = num_deteccao_pa + 1

                print("pa")

            if(num_deteccao_pa == 20):
                pa_detectado = True
                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                pa_detectado = False

        if(botas_necessario and botas_detectado == False):

            deteccao_botas = cascade_botas.detectMultiScale(video_detectar_botas, scaleFactor=1.02, minNeighbors=10)

            for(w, x, y, z) in deteccao_botas:
                cv2.rectangle(video, (w, x), (w + y, x + z), (255, 0, 255), 2)

            if(deteccao_botas != ()):
                # print("botas detectado!")
                print("botas")
                num_deteccao_botas = num_deteccao_botas + 1

                
            if(num_deteccao_botas == 20):
                botas_detectado = True
                numero_epis_verificacao = numero_epis_verificacao - 1

            else:
                botas_detectado = False
            
        if(cv2.waitKey(1) == ord("q")):
            cv2.imwrite(nome_arquivo_imagem, video)
            break

        if(numero_epis_verificacao == 0):
            todas_epis_encontradas = True
            epis_encontradas = True
            EnviarJsonFirebase(empresa, nome_funcionario, data, epis_encontradas)
            ser = serial.Serial("COM4")
            valor = "A"
            cv2.imwrite(nome_arquivo_imagem, video)
            iniciar_script = ser.readline().decode("utf-8")

            while True:
                ser.flush()
                ser.write(valor.encode())

                if ser.inWaiting() > 0:
                    print(ser.readline())
                    if ser.readline().decode("utf-8") == "led\r\n":
                        ser.flush()
                        ser.close()
                        break
            
            ser = serial.Serial("COM4")

            a = 0
            valor = "B"
            while a < 100:
                ser.flush()
                ser.write(valor.encode())
                a = a+1


            print("Todas as epis foram encontradas!!!!!")
            break

        cv2.imshow("Identificação funcionário", video)
        # cv2.imshow("Video detecção capacete", video_detectar_capacete)
        # cv2.imshow("Video detecção colete", video_detectar_luvas)
        # cv2.imshow("Video detectar botas", video_detectar_botas)

    camera.release()

    cv2.destroyAllWindows()

    if(todas_epis_encontradas == False):
        EnviarWhatsapp(nome_funcionario)
        epis_encontradas = False
        EnviarJsonFirebase(empresa, nome_funcionario, data, epis_encontradas)

    
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
    print(nome_funcionario)
    db = firebase.database()
    print("Conexão ao banco de dados efetuada com sucesso!")
    base_dados_funcionario = empresa+"/funcionarios/"+nome_funcionario
    print(base_dados_funcionario)

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
    teste_atencao_necessario = False
    if(teste_atencao_necessario):
        teste_atencao_realizado = dados_funcionario.val()['teste_realizado']
        if(teste_atencao_realizado):
            IdentificarEPIS(nome_funcionario, lista_epis_necessarias)

        else:
            print("Realize o teste!")
            return
    else:
        IdentificarEPIS(nome_funcionario, lista_epis_necessarias)

    db.child(base_dados_funcionario).update({"teste_realizado": False})

    return

def UsarDeteccaoFacial():
    # camera = cv2.VideoCapture(0)

    # classificadorFace = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")
    # reconhecedor = cv2.face.LBPHFaceRecognizer_create()

    # reconhecedor.read("classificadores/classificadorLBPH.yml")

    # largura, altura = 220, 220

    # font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    # face_detectada = 0

    # while True:
    #     _, video = camera.read()
    #     videoCinza = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)

    #     facesDetectadas = classificadorFace.detectMultiScale(videoCinza, scaleFactor=1.1, minSize=(30, 30))

    #     for(x, y, l, a) in facesDetectadas:
    #         imagemFace = cv2.resize(videoCinza[y:y + a, x:x + l], (largura, altura))

    #         cv2.rectangle(video, (x, y), (x + l, y + a), (0, 0, 255), 2)

    #         id, confianca = reconhecedor.predict(imagemFace)

    #         with open("json/nomes_funcionarios.json", encoding="utf-8") as json_funcionarios:
    #             json_nome_funcionarios = json.load(json_funcionarios)

    #         nome_funcionario = "Funcionario nao detectado!"
    #         # print(id)

    #         if(id != -1):
    #             face_detectada = face_detectada + 1
    #             nome_funcionario = json_nome_funcionarios[str(id)]

    #         cv2.putText(video, str(nome_funcionario), (x, y + (a + 30)), font, 1, (0, 0, 255))

    #     cv2.imshow("Face", video)
    #     if cv2.waitKey(1) == ord("q"):
    #         break

    #     if face_detectada == 10:
    #         break

    # camera.release()

    # cv2.destroyAllWindows()
    nome_funcionario = input()
    
    BuscarFuncionario(nome_funcionario)
    
def UsarBiometria():
    ser = serial.Serial("COM4")

    valor = "L"
    print(valor.encode())

    verificacaoIniciada = False
    while True:
        ser.write(valor.encode())

        if ser.inWaiting() > 0:
            print(ser.readline())

        if ser.readline().decode("utf-8") == "65535\r\n":
            verificacaoIniciada = True

        if verificacaoIniciada == True:
            valorId = ser.readline().decode("utf-8").rstrip("\n").rstrip("\r")
            # print(valorId)

            if(valorId != "65535"):
                print("Id detectado: ", valorId)
                print("Biometria detectada!")
                break

            # if(ser.readline().decode("utf-8") != "65535\r\n"):
            #     print("Biometria detectada!")

    with open("json/funcionarios_id_biometria.json", encoding="utf-8") as json_ids:
        json_ids_funcionarios = json.load(json_ids)

    nome_funcionario = json_ids_funcionarios[valorId]

    ser.close()

    print(nome_funcionario)
    BuscarFuncionario(nome_funcionario)

def UsarRFID():
    ser = serial.Serial("COM4")

    valor = "R"

    while True:
        id_cartao = ser.readline()
        print(id_cartao)
        if(id_cartao.decode() == "1\r\n"):
            print("Id detectada")
            break
    
    id_cartao = ser.readline()

    id_cartao = id_cartao.decode("utf-8")
    id_cartao = id_cartao.rstrip("\n")
    id_cartao = id_cartao.rstrip("\r")

    with open("json/nome_funcionario_RFID.json", encoding="utf-8") as json_nome_funcionarios:
        json_funcionarios = json.load(json_nome_funcionarios)

    nome_funcionario = json_funcionarios[id_cartao]

    ser.close()

    print(nome_funcionario)
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





    

