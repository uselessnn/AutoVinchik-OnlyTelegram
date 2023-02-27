from json import encoder
from typing import Container
import time
import emoji
from skipper import checkSkip, load_config, config, update_config
from telethon import TelegramClient, events, sync
import os
import colorama
from colorama import Fore
import random
from collections import Counter

is_tg_connected = False

sessionpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'AutoVinchik.session')
logpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log.txt')

colorama.init(autoreset=True)
os.system("cls")


def logo():
    print("")
    with open("banner.txt", "r", encoding="UTF-8") as file:
        for i in file.readlines():
            text = i.strip().split("|")
            print(Fore.RED + "   " + text[0], Fore.YELLOW + text[1])
    print("\n")


logo()
typeOfLikes = 0;
print(Fore.YELLOW + "  Загрузка конфигурации")

config = load_config()

print(Fore.YELLOW + "  Подключение ключа Телеграм")
try:
    client = TelegramClient('AutoVinchik', config["API_ID"], config["API_HASH"])
    client.start()
    print(Fore.GREEN + "  Ключ Телеграм подключен")
    is_tg_connected = True
except:
    print(Fore.RED + "  Ключ Телеграм не подключен")
print(Fore.YELLOW + "  Инициализация запуска")
time.sleep(0.3)

BOT = 'leomatchbot'
BOT_ID = 1234060895
mode = 0


def telegram():
    time.sleep(0.5) # Не спрашивайте
    
    print(f"{Fore.CYAN}TG |{Fore.RESET} ", end="")
    message = client.get_messages(BOT,limit=1)[0].message.lower()
    
    if len(message.replace(" ", "")) < 2:
        message = client.get_messages(BOT)[0].message
        for i in client.iter_messages(BOT):
            if (len(i.message) > 0):
                message = i.message
                #print(message)
                break
        #input("ZXFC")
    skip = checkSkip(message)
    try:
        if str(type(skip)) == str(type(1)):
            client.send_message(BOT, str(skip))
            time.sleep(2)
            message = client.get_messages(BOT)[0].text.lower()
            skip = checkSkip(message)
    except:
        pass

    if (skip):
        client.send_message(BOT, emoji.emojize(":thumbs_down:"))
        time.sleep(config["DELAY_TG"])
    else:
        if config["TYPE_OF_LIKES"] == 0:
            client.send_message(BOT, emoji.emojize(":red_heart:"))
        if config["TYPE_OF_LIKES"] == 1:
            input(f"{Fore.CYAN}Для пропуска анкеты нажмите ENTER")
            client.send_message(BOT, emoji.emojize(":thumbs_down:"))
        if config["TYPE_OF_LIKES"] == 2:
            print(f"{Fore.CYAN}[1].{Fore.RESET} Лайк")
            print(f"{Fore.CYAN}[2].{Fore.RESET} Скип")
            do = input(f"{Fore.CYAN}>>>{Fore.RESET} ")
            if do == "2":
                client.send_message(BOT, emoji.emojize(":thumbs_down:"))
            elif do == "1":
                client.send_message(BOT, emoji.emojize(":red_heart:"))


leave_config = False
while True:
    os.system("cls")
    logo()
    print(f"{Fore.CYAN}  [0]{Fore.RESET} Конфигурация")
    print(f"{Fore.CYAN}  [1]{Fore.RESET} Поиск по телеграм")
    do = input(f"{Fore.CYAN}  >>>{Fore.RESET} ")

    if do == "0":
        while True:
            os.system("cls")
            logo()
            neutral = Fore.RED
            n_text = "Отключено"
            if config["SKIP_ALL"]:
                neutral = Fore.GREEN
                n_text = "Включено"
            print(f"{Fore.CYAN}   [0]{Fore.RESET} Выход из конфигурации")
            print(f"{Fore.CYAN}   [1]{Fore.RESET} Токен Телеграм " + Fore.YELLOW + "(" + str(config["API_ID"])[
                                                                                      :2] + "***:***" + config[
                                                                                                            "API_HASH"][
                                                                                                        -4::] + ")")
            print(f"{Fore.CYAN}   [2]{Fore.RESET} Настройка запрещённых ключей " + Fore.YELLOW + str(config["BLACKLIST"]))
            print(f"{Fore.CYAN}   [3]{Fore.RESET} Настройка искомых ключей " + Fore.YELLOW + str(config["WHITELIST"]))
            print(f"{Fore.CYAN}   [4]{Fore.RESET} Задержка для Телеграм " + Fore.YELLOW + "(" + str(
                config["DELAY_TG"]) + " сек)")
            print(
                f"{Fore.CYAN}   [5]{Fore.RESET} Останавливаться только на искомых ключах " + neutral + "(" + n_text + ")")
            print(f"{Fore.CYAN}   [6]{Fore.RESET} Минимальное количество символов для пропуска " + Fore.YELLOW + "(" + str(
                config["MIN_SYMBOL"]) + ")")
            print(f"{Fore.CYAN}   [7]{Fore.RESET} Удалить сессию (требуется перезапуск + без подключения сессии краш) ")
            print(f"{Fore.CYAN}   [8]{Fore.RESET} Выбор способа лайка" + Fore.YELLOW + " (" + str(
                config["TYPE_OF_LIKES"]) + ")");
            print(f"{Fore.CYAN}   [9]{Fore.RESET} Удалить лог ")
            print(f"{Fore.CYAN}   [10]{Fore.RESET} Стандартный конфиг ")
            print(f"{Fore.CYAN}   [11]{Fore.RESET} Инфо ")
            do = input(f"{Fore.CYAN}   >>>{Fore.RESET} ")
            if do == "0":
                leave_config = True
                break
            elif do == "1":
                os.system("cls")
                logo()
                api_id = input(f"{Fore.CYAN}   Введите API_ID: ")
                api_hash = input(f"{Fore.CYAN}   Введите API_HASH: ")
                config["API_ID"] = api_id
                config["API_HASH"] = api_hash
            elif do == "2" or do == "3":
                type = "BLACKLIST"
                if do == "3":
                    type = "WHITELIST"
                while True:
                    os.system("cls")

                    logo()
                    print("")
                    print(f"{Fore.CYAN}   ID | Все значения:")
                    for index, i in enumerate(config[type]):
                        print(f"{Fore.CYAN}[{index}]{Fore.RESET}. {i}")
                    print("\n")
                    print(f"{Fore.CYAN}   Можно указать сразу несколько значений через точку с запятой (;)")
                    print(f"{Fore.CYAN}   [0]{Fore.RESET} Удалить значения")
                    print(f"{Fore.CYAN}   [1]{Fore.RESET} Добавить значения")
                    print(f"{Fore.CYAN}   [2]{Fore.RESET} Выход из редактора")
                    do = input(f"{Fore.CYAN}   >>>{Fore.RESET} ")
                    if do == "2":
                        break
                    elif do == "0":
                        sid = input(f"{Fore.CYAN}Введите ID значений: {Fore.RESET}")
                        for i in sid.split(";"):
                            config[type][int(i)] = "//TODELETE//"
                        while "//TODELETE//" in config[type]:
                            config[type].remove("//TODELETE//")
                    elif do == "1":
                        new_value = input(f"{Fore.CYAN}Новые значение: {Fore.RESET}")
                        for i in new_value.split(";"):
                            config[type].append(i.lower())
                    update_config(config)
            elif do == "4":
                dat1a = input(f"{Fore.CYAN}Новая задержка для Телеграм: ")
                config["DELAY_TG"] = float(dat1a)
            elif do == "5":
                config["SKIP_ALL"] = not config["SKIP_ALL"]
            elif do == "6":
                data = input(f"{Fore.CYAN}Новое количество символов: ")
                config["MIN_SYMBOL"] = int(data)
            elif do == "7":
                  client.disconnect()
                  os.remove(sessionpath)
                  print(f"\n{Fore.GREEN}  Выполнено")
                  os.system("py main.py")
            elif do == "8":
                os.system("cls")
                print(f"\n{Fore.CYAN}   [0]{Fore.RESET} Всегда лайк")
                print(f"{Fore.CYAN}   [1]{Fore.RESET} Дизлайк на ENTER")
                print(f"{Fore.CYAN}   [2]{Fore.RESET} Выбор в консоли")
                do = input(f"{Fore.CYAN}   >>>{Fore.RESET} ");
                if (do == "0"):
                    config["TYPE_OF_LIKES"] = 0
                elif (do == "1"):
                    config["TYPE_OF_LIKES"] = 1
                elif (do == "2"):
                    config["TYPE_OF_LIKES"] = 2

            elif do == "9":
                try:
                    os.remove(logpath)
                    print(f"\n{Fore.GREEN}Выполнено")
                    input(f"{Fore.CYAN}   Для выхода нажмите ENTER")
                except:
                    os.system("cls")
                    logo()
                    print(f"{Fore.CYAN}   Лога нет!")
                    input(f"{Fore.CYAN}   Для выхода нажмите ENTER")
            if do == "10":

                config["SKIP_ALL"] = True
                config["DELAY_TG"] = float(1.0)
                config["MIN_SYMBOL"] = int(5)
                config["WHITELIST"] = []
                config["BLACKLIST"] = []
                config["API_ID"] = ""
                config["API_HASH"] = ""

                update_config(config)

            elif do == "11":

                os.system("cls")
                logo()
                print(f"{Fore.CYAN}   Coded by t.me/useleeess & t.me/prizrak_farfore")
                print(f"{Fore.CYAN}   Changelog: https://t.me/autovinchik")
                print(f"{Fore.CYAN}   Version: 0.3")
              
                update_config(config)
                input(f"\n{Fore.CYAN}   Для выхода нажмите ENTER")

    if leave_config:
        leave_config = False
        continue
    elif do == "1":
        mode = 0
    elif do == "2":
        mode = 1
    elif do == "3":
        mode = 2
    os.system("cls")
    logo()

    print("")
    time.sleep(1)
    print(f"{Fore.YELLOW}Не забудьте запустить режим поиска в сообщениях винчика! {Fore.RESET}\n")
    print(f"{Fore.YELLOW}Для выхода из поиска нажмите CTRL+C {Fore.RESET}\n")
    while True:
        try:
            if (mode == 0 or mode == 2):
                telegram()
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\nВыход в меню... {Fore.RESET}")
            time.sleep(0.3)
            break
