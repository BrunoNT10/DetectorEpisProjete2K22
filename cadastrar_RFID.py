import json
import serial
import tkinter as tk
from tkinter import *

def Sair(janela):
    janela.destroy()
    print("Encerrando aplicação...")

def Cadastrar(labelTitle, labelNomeFunc, inputNomeFunc, buttonCadastrar, janela):
    
    ser = serial.Serial("COM4")

    nome_funcionario = inputNomeFunc.get()

    id_cartao = ser.readline()
    id_cartao = id_cartao.decode("utf-8")
    id_cartao = id_cartao.rstrip("\n")
    id_cartao = id_cartao.rstrip("\r")

    with open("json/nome_funcionario_RFID.json", encoding="utf-8") as json_nomes_funcionarios:
        json_nomes = json.load(json_nomes_funcionarios)

    try:
        json_nomes[id_cartao] = nome_funcionario

        atualizar_json_funcionarios = json.dumps(json_nomes, indent=4)

        with open("json/nome_funcionario_RFID.json", "w") as json_nomes_funcionarios:
            json_nomes_funcionarios.write(atualizar_json_funcionarios)

        labelMensagem = Label(janela, text="TAG cadastrada com sucesso!")
        labelMensagem.pack(side=TOP)
        labelMensagem["bg"] = "light green"

        buttonCadastrarOutroFuncionario = Button(janela, text="Cadastrar outro funcionário", height=2, width=30, command=lambda:CriarJanelaSecundaria(janela))
        buttonCadastrarOutroFuncionario.pack(side=TOP)
        buttonCadastrarOutroFuncionario["bg"] = "light blue"

        buttonSair = Button(janela, text="Sair", height=2, width=30, command= lambda:Sair(janela))
        buttonSair.pack(side=TOP)
        buttonSair["bg"] = "red"

        labelTitle.destroy()
        labelNomeFunc.destroy()
        inputNomeFunc.destroy()
        labelTitle.destroy()
        buttonCadastrar.destroy()

    except:
        
        labelMensagem = Label(janela, text="Erro ao cadastrar TAG!")
        labelMensagem.pack(side=TOP)
        labelMensagem["bg"] = "red"

def CriarJanelaSecundaria(janela):

    janela.destroy()

    janela = tk.Tk()

    janela.title("Cadastrar RFID")

    janela.geometry("400x400")

    labelTitle = Label(janela, text="Cadastro dos crachás dos funcionários", font=("Calibri 15"))
    labelTitle.pack(side=TOP)

    labelNomeFunc = Label(janela, text='Digite no campo abaixo o nome do funcionário, clique em "Cadastrar" \n e aproxime o crachá do leitor')
    labelNomeFunc.pack(side=TOP)

    inputNomeFunc = Entry(janela, width=40)
    inputNomeFunc.pack(side=TOP)

    buttonCadastrar = Button(janela, text="Cadastrar", height=2, width=30, command=lambda: Cadastrar(labelTitle, labelNomeFunc, inputNomeFunc, buttonCadastrar, janela))
    buttonCadastrar.pack(side=TOP)

    janela.mainloop()

def CriarJanelaPrincipal():

    janela = tk.Tk()

    janela.title("Cadastrar RFID")

    janela.geometry("400x400")

    labelTitle = Label(janela, text="Cadastro dos crachás dos funcionários", font=("Calibri 15"))
    labelTitle.pack(side=TOP)

    labelNomeFunc = Label(janela, text='Digite no campo abaixo o nome do funcionário, clique em "Cadastrar" \n e aproxime o crachá do leitor')
    labelNomeFunc.pack(side=TOP)

    inputNomeFunc = Entry(janela, width=40)
    inputNomeFunc.pack(side=TOP)

    buttonCadastrar = Button(janela, text="Cadastrar", height=2, width=30, command=lambda: Cadastrar(labelTitle, labelNomeFunc, inputNomeFunc, buttonCadastrar, janela))
    buttonCadastrar.pack(side=TOP)

    janela.mainloop()

CriarJanelaPrincipal()