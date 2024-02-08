import pyautogui
import time
import json
import os
from tqdm import tqdm
from colorama import init, Fore, Style
from datetime import datetime, timedelta

dalay = 0.8
new_dav_dalay = 1
write_interval = 0.05
discount_dalay = 3.5
difference_dalay = 17.74

# Inicia a biblioteca colorama
init()

color_green = Fore.LIGHTGREEN_EX
color_reset = Style.RESET_ALL

def presentation(total_capt_qtd, total_dav_qtd, username, cpf, current_time, time_to_finish):
    os.system('cls')
    future_time = current_time + timedelta(seconds=time_to_finish + (total_dav_qtd * difference_dalay))
    formatted_time = future_time.strftime("%d/%m/%Y %H:%M:%S")
    
    print(Fore.LIGHTBLUE_EX + "\n" + "                        ______           ______      __       __  ")
    print(Fore.LIGHTYELLOW_EX +      "                       / ____/________  / ____/___ _/ /______/ /_ ")
    print(Fore.LIGHTMAGENTA_EX +     "                      / __/ / ___/ __ \/ /   / __ `/ __/ ___/ __ \\")
    print(Fore.LIGHTYELLOW_EX +      "                     / /___/ /__/ /_/ / /___/ /_/ / /_/ /__/ / / /")
    print(Fore.LIGHTBLUE_EX +        "                    /_____/\___/\____/\____/\__,_/\__/\___/_/ /_/ \n" + color_reset)
                                              


    print(f' rCAPTAÇÃO: ' + color_green + str(total_capt_qtd) + color_reset + f' DAV: ' + color_green + str(total_dav_qtd) + color_reset + ' USUÁRIO: ' + color_green + username + color_reset + f' CPF: ' + color_green + cpf + color_reset + ' TÉRMINO: ' + color_green + formatted_time + color_reset + '\n')
    

def calc_time(qtd_capt, currentqtd, dav_product_limit):
    login_time = 5 * dalay
    cpf_time = 2 * dalay
    add_product_time = (4 * dalay) + discount_dalay
    new_dav_time = (2 * dalay) + new_dav_dalay
    time_to_finish = login_time + cpf_time + (qtd_capt * add_product_time) + ((qtd_capt / dav_product_limit) * new_dav_time)
    current_time_to_finish = login_time + cpf_time + (currentqtd * add_product_time) + ((currentqtd / dav_product_limit) * new_dav_time)
    time_left = 0 if time_to_finish - current_time_to_finish < 0 else time_to_finish - current_time_to_finish
    return time_to_finish, time_left

def parseData():
    with open('./data.json', 'r') as file:
        data = json.load(file)
        return data
    
def add_client_cpf(cpf):
    pyautogui.write(cpf, interval=write_interval)

    time.sleep(dalay)
    pyautogui.press('enter')

    time.sleep(dalay)
    
def new_dav(btn_location):
    pyautogui.moveTo(btn_location.x, btn_location.y)

    time.sleep(dalay)
    pyautogui.click()

    time.sleep(new_dav_dalay)
    pyautogui.press('enter')
    
    time.sleep(dalay)

def AddProduct(cod_product, crm):
    pyautogui.write(cod_product, interval=write_interval)

    time.sleep(discount_dalay)
    pyautogui.press('enter')

    time.sleep(dalay)
    pyautogui.press('enter')

    time.sleep(dalay)
    pyautogui.write(crm, interval=write_interval)

    for _ in range(2):
        time.sleep(dalay)
        pyautogui.press('enter')

    time.sleep(dalay)

def login(username, password):
    pyautogui.press('enter')
    time.sleep(dalay)

    pyautogui.write(username, interval=write_interval)
    time.sleep(dalay)
    pyautogui.press('enter')

    time.sleep(dalay)

    pyautogui.write(password, interval=write_interval)
    time.sleep(dalay)
    pyautogui.press('enter')

    time.sleep(dalay)

def show_info(cod_product, name_product, doctor_crm):
    print('+ COD: ' + Fore.LIGHTRED_EX + cod_product.upper() + color_reset + ' PRODUCT: ' + Fore.LIGHTMAGENTA_EX + f'{name_product.upper()} ' + color_reset + 'CRM: ' + Fore.CYAN + doctor_crm.upper() + color_reset)
    
def progress_bar_position(cod_product=None, name_product=None, doctor_crm=None, old_capt=[], dav_product_limit=None):
    for old_capt_item in old_capt:
        show_info(cod_product=old_capt_item['product']['cod_product'], name_product=old_capt_item['product']['name_product'], doctor_crm=old_capt_item['crm'])

    if cod_product and name_product and doctor_crm:
        show_info(cod_product, name_product, doctor_crm)

    for _ in range(dav_product_limit - len(old_capt) + 4):
        if dav_product_limit - len(old_capt) == 0:
            break
        print('')

def start():
    username = input('Digite sua chapa: ')
    password = input('Digite sua senha: ')
    client_cpf = input('Digite o CPF de cadastro: ')
    qtd_capt = None
    currentqtd = 0
    cont_capt = 1
    cont_dav = 1
    dav_product_limit = 10
    json_data = parseData()
    old_capt = []

    while qtd_capt == None:
        try:
            qtd_capt = int(input('Quantidade de captação: '))
        except:
            pass
    
    btn_confirm_position = input('Localização do botão confirmar: ')
    btn_confirm_position = pyautogui.position()

    os.system('cls')
    print('Aguarde....')
    time.sleep(10)

    current_time = datetime.now()

    login(username, password)
    add_client_cpf(client_cpf)
    
    with tqdm(total=qtd_capt) as progress_bar:
        while True:
            for item in json_data:
                products = item.get('products')
                doctors = item.get('crms')
                for product in products:
                    cod_product = str(product.get('cod_product'))
                    name_product = str(product.get('name_product'))
                    for doctor in doctors:
                        doctor_crm = str(doctor.get('cod_crm') + doctor.get('uf'))
                        time_to_finish, time_left = calc_time(qtd_capt=qtd_capt, currentqtd=currentqtd, dav_product_limit=dav_product_limit)
                        if cont_capt > dav_product_limit:
                            presentation(
                                total_capt_qtd=qtd_capt, 
                                total_dav_qtd=int(qtd_capt / dav_product_limit), 
                                username=username, 
                                cpf=client_cpf, 
                                time_to_finish=time_to_finish,
                                current_time=current_time
                            )

                            progress_bar_position(
                                old_capt=old_capt,
                                dav_product_limit=dav_product_limit
                            )

                            print(Fore.LIGHTBLUE_EX + f'\n(*) ' + color_reset + f'{str(currentqtd)} Captações')
                            print(Fore.LIGHTMAGENTA_EX + '    (*) ' + color_reset + f'Faltam {str(int(time_left / 60))} minutos')
                            print(Fore.GREEN + f"        (+) " + color_reset + f"{str(cont_dav)} DAV gerada | Processando {str(int((qtd_capt / dav_product_limit) - (currentqtd / dav_product_limit)))} restante...\n")
                            
                            progress_bar.refresh()
                            
                            new_dav(btn_confirm_position)

                            if qtd_capt - (currentqtd + 1) > -1:
                                login(username, password)
                                add_client_cpf(client_cpf)

                            old_capt.clear()
                            
                            cont_capt = 1
                            cont_dav += 1

                        if currentqtd + 1 <= qtd_capt:
                            AddProduct(cod_product, doctor_crm)

                            presentation(
                                total_capt_qtd=qtd_capt, 
                                total_dav_qtd=int(qtd_capt / dav_product_limit), 
                                username=username, 
                                cpf=client_cpf, 
                                time_to_finish=time_to_finish,
                                current_time=current_time
                            )

                            progress_bar_position(
                                cod_product=cod_product,
                                name_product=name_product,
                                doctor_crm=doctor_crm,
                                old_capt=old_capt,
                                dav_product_limit=dav_product_limit
                            )

                            progress_bar.update(1)

                            old_capt.append({'product': {'cod_product': cod_product,'name_product': name_product},'crm': doctor_crm})
                            currentqtd += 1
                            cont_capt += 1
                        else:
                            input('\n\nPressione ENTER para sair...')
                            exit()
                        

if __name__ == "__main__":
    start()
