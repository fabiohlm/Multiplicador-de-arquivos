import os, sys
import PySimpleGUI as sg
import shutil

endereco = str()
ncopias = int()
njpg = int()
npastas = int()
listapastas = []

def navigate_and_rename(src, n):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        if os.path.isdir(s):
            continue 
        elif s.endswith(".jpg"):
            if s.endswith(f"#{range(1,int(n)+1)}.jpg"):
                continue
            else:
                for i in range(1,int(n)+1):
                    newitem = s[:-4]
                    shutil.copy(s, os.path.join(src, newitem+f"#{i}.jpg"))
                os.remove(s)  

layout1 = [[sg.Text("Digite o endereço da pasta contendo as NFT's")],
           [sg.Input(R"",key="endereco")],
           [sg.Text("",key="aviso1")],
           [sg.Button("Avançar", key="avancar1"),sg.Button("Sair", key="Sair1")]]

layout2 = [[sg.Text("Digite o número de cópias de cada NFT")],
           [sg.Input("",enable_events=True, key="ncopias")],
           [sg.Text("",key="aviso2")],
           [sg.Button("Avançar", key="avancar2"),sg.Button("Voltar", key="voltar2"),sg.Button("Sair", key="Sair2")]]

layout3 = [[sg.Text("Dados:")],
           [sg.Text("",key="npastas")],
           [sg.Text("",key="njpg")],
           [sg.Text("",key="aviso3")],
           [sg.Button("Avançar", key="avancar3"),sg.Button("Voltar", key="voltar3"),sg.Button("Sair", key="Sair3")]]

layout4 = [[sg.Text("Resultado:")],
           [sg.Text(".",key="aviso4")],
           [sg.Button("Sair", key="Sair4")]]


layout = [[sg.Column(layout1, key="-COL1-"), sg.Column(layout2, visible=False, key="-COL2-"), sg.Column(layout3, visible=False, key="-COL3-"), sg.Column(layout4, visible=False, key="-COL4-")]]

window = sg.Window("Multiplicador de NFT", layout)
 
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, "Sair1", "Sair2", "Sair3", "Sair4") or event == sg.WIN_CLOSED:
        break

    if values["endereco"] == "":
        window["aviso1"].update("*Digite o endereço antes de continuar!")
        window["aviso1"].update(text_color = "red")
    
    if values["endereco"] != "":
        
        # Averigua se o endereço digitado é uma pasta existente no sistema
        if os.path.isdir(values["endereco"]):
            window["aviso1"].update("Endereço válido")
            window["aviso1"].update(text_color = "green")
            if event == "avancar1":
                endereco = values["endereco"]
                window[f"-COL1-"].update(visible=False)
                window[f"-COL2-"].update(visible=True)
        else:
            window["aviso1"].update("Endereço inválido")
            window["aviso1"].update(text_color = "red")
    
    # Averigua se os caractéres digitados são números ao digitar
    if len(values["ncopias"]) and values["ncopias"][-1] not in ("0123456789"):
        window["ncopias"].update(values["ncopias"][:-1])
    
    if values["ncopias"] == 0 or values["ncopias"] == "" or values["ncopias"] == "0":
        window["aviso2"].update("*Digite um valor")
        window["aviso2"].update(text_color = "red")
    else:
        window["aviso2"].update("Valor válido")
        window["aviso2"].update(text_color = "green")
        if event == "avancar2":
            ncopias = values["ncopias"]
            
            # Conta quantos arquivos jpeg existem dentro da pasta
            for i in os.listdir(endereco):
                if i.endswith(".jpg") or i.endswith(".jpeg"):
                    njpg = njpg + 1
                if os.path.isdir(endereco+"\\"+i):
                    npastas = npastas + 1
                    listapastas.append(endereco+"\\"+i)
            
            # Conta quantos arquivos jpeg existem dentro de cada pasta dentro da pasta
            for i in listapastas:
                for j in os.listdir(i):
                    if j.endswith(".jpg") or j.endswith(".jpeg"):
                        njpg = njpg + 1
            
            window["npastas"].update(f"Número de pastas no endereço digitado: {npastas}")
            window["njpg"].update(f"Número de imagens no endereço digitado: {njpg}")
            window[f"-COL2-"].update(visible=False)
            window[f"-COL3-"].update(visible=True)
    if njpg == 0:
        window["aviso3"].update("Não há imagens nesse endereço")
        window["aviso3"].update(text_color = "red")
    else:
        window["aviso3"].update("Deseja avançar com a operação?")
        window["aviso3"].update(text_color = "white")
        if event == "avancar3":
            window[f"-COL3-"].update(visible=False)
            window[f"-COL4-"].update(visible=True)
            try:
                navigate_and_rename(endereco, ncopias)
                if len(listapastas) > 0:
                    for i in listapastas:
                        navigate_and_rename(i, int(ncopias))
            except Exception as e:
                # window["aviso4"].update("Ocorreu um erro")
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e)
            else:
                window["aviso4"].update("Operação concluída com sucesso!")
                    

    if event == "voltar2":
        window[f"-COL1-"].update(visible=True)
        window[f"-COL2-"].update(visible=False)

    if event == "voltar3":
        window[f"-COL2-"].update(visible=True)
        window[f"-COL3-"].update(visible=False) 

    if event in (None, "Sair2") or event == sg.WIN_CLOSED:
        break

window.close()

