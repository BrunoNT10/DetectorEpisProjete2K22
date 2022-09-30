import serial
from tkinter import *
import tkinter as tk
import json

def CadastrarBiometria():
    ser = serial.Serial("COM4")
    nome_funcionario = inputName.get()
    if nome_funcionario == "":
        
        labelResposta = Label(janela, text="Digite o nome do funcionário!")
        labelResposta.pack(side=TOP)

        return

    valor = "C"

    cadastroIniciado = False
    id_recebido = False

    while True:
        ser.write(valor.encode())

        if ser.readline().decode("utf-8") == "cadastrar\r\n":
            cadastroIniciado = True

        if cadastroIniciado == True:
            print("Cadastro iniciado")
            # nome_funcionario = input("Digite o nome do funcionário: ")

            with open("json/funcionarios_id_biometria.json", encoding="utf-8") as json_ids:
                json_ids_funcionarios = json.load(json_ids)

            lista_ids_cadastradas = list(json_ids_funcionarios.keys())

            for id in lista_ids_cadastradas:
                id = int(id)

            id = id + 1
            id = str(id)

            json_ids_funcionarios[id] = nome_funcionario

            enviar_id_funcionario = json.dumps(json_ids_funcionarios, indent=4)

            with open("json/funcionarios_id_biometria.json", "w") as json_ids:
                json_ids.write(enviar_id_funcionario)

            while True:
                ser.write(id.encode())

                if ser.readline().decode("utf-8") == "id_ok\r\n":
                    print("id_recebido")
                    id_recebido = True

                    while True:
                        if(ser.readline().decode("utf-8") == "cadastrado\r\n"):
                            print("Digital cadastrada!")                        
                            break
                    break

        if id_recebido == True:
            break

janela = tk.Tk()
janela.geometry("600x600+100+100")

labelTitle = Label(janela, text="Cadastro das digitais", font=("calibri 25"))
labelTitle.pack(side=TOP)

labelName = Label(
    janela, text="Digite o nome do funcionário: ", font=("calibri 12"))
labelName.pack(side=TOP)

inputName = Entry(janela, width=40)
inputName.pack(side=TOP)

buttonRegister = Button(janela, text="Cadastrar Digital",
                        width=20, command=CadastrarBiometria)
buttonRegister.pack(side=TOP)
buttonRegister["bg"] = "green"
buttonRegister["fg"] = "white"

janela.mainloop()
