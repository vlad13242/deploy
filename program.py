import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.error import RetryAfter 
import time
from telegram import InputMediaPhoto
import schedule
import re
import base64


def get_all_info_in_url(big_url, tipe_pars, kilk_iner_elem_big):
    print(f"funk go {tipe_pars}")
    BOT_TOKEN = '6791691843:AAFPIy_GLYC7-eRDSb1okBF1bPZ2IUsD_oU'
    CHANNEL_USERNAME = '@aviahunter'
    iter_item = 1
    stop = 0
    for page_listen in range(1, int(kilk_iner_elem_big)):
        try:
            USA = 0
            if stop == 1:
                break
            for i in range(5):
                try:
                    # print(f"{big_url}&s-page={page_listen}")
                    response = requests.get(f"{big_url}&s-page={page_listen}", timeout=120)
                    if response.status_code == 200:
                        break
                except:
                    print("+1 page get")
                    pass
            html_content = response.content

            # Створити об'єкт BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            chrome_options = Options()

            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(300)
            driver.get(f"{big_url}&s-page={page_listen}")
            # Получите HTML-код страницы
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            # time.sleep(100)
            with open("output.html", "w", encoding="utf-8") as file:
                file.write(soup.prettify())
            #  log_listing_click
            elements = soup.find_all(class_='log_listing_click')
            list_url = []
            for element in elements:
                if element["href"] not in list_url:
                    list_url.append(element["href"])
            print(len(list_url))
            if len(list_url) == 0:
                stop = 1
                break
            if int(kilk_iner_elem_big) == 2:
                list_url = list_url[:20]
            for url in list_url:
                try:
                    bot = Bot(token=BOT_TOKEN)
                    chrome_options = Options()
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.set_page_load_timeout(10)
                    stop_sold = 0
                    for ijh in range(5):
                        try:
                            driver.get(f"https://www.trade-a-plane.com/{url}")
                        except:
                            print("selenium попытка")
                        try:
                            # Получите HTML-код страницы
                            html_content = driver.page_source
                            soup = BeautifulSoup(html_content, 'html.parser')
                            # name
                            elem = soup.find_all(attrs={'itemprop': "name"})
                            print(elem[0].text)
                            name_element_1 = elem[0].text
                            #price
                            elements_prise = soup.find_all(class_='price')
                            praice = elements_prise[0].text.split("Price:")[1].split("\n")[0]
                            # print(1/0)
                            #phone
                            elements_prise = soup.find_all(class_='seller-phone-top')
                            phone = elements_prise[0].text
                            af = phone.split("\n")
                            phone = f" {af[2]}\n{af[4]}"
                            #info
                            elements_prise = soup.find_all(class_='info-list-seller')
                            info_item_one = elements_prise[0].text
                            try:
                                info_item_one = "".join(info_item_one.split("\n\t"))
                                info_item_one = info_item_one.replace("                           ", " ")
                                print(info_item_one)
                            except:
                                pass
                            # Використовуємо регулярний вираз для розділення тексту за допомогою "\n" і ":"
                            result = re.split(r'[\n:]', info_item_one)
                            result = result[1:]
                            b = result[::2]
                            c = result[1::2]
                            fin_all_text = ""
                            for iter_text_modern in range(len(c)):
                                fin_all_text += f"<b>{b[iter_text_modern]}:</b>{c[iter_text_modern]}\n"
                            info_item_one = fin_all_text
                            # General Specs
                            elements_general_specs = soup.find_all(id='general_specs')
                            info_item_one_blok2 = elements_general_specs[0].find_all('p')
                            all_info2_block = ''
                            for i in info_item_one_blok2:
                                all_info2_block += f"<b>{i.text.split(':')[0]}:</b> {i.text.split(':')[1]}\n"
                            print(all_info2_block)
                            # if "USA" in info_item_one:
                            #     USA = 1
                            #image
                            elements_image_block = soup.find_all(class_='ps-list')
                            a_image = elements_image_block[0].find_all('a')
                            #url
                            print(f"https://www.trade-a-plane.com/{url}")
                            # block info Detailed Description
                            try:
                                elements_Detailed = soup.find_all(attrs={'itemprop': "description"})
                                # print(elements_Detailed[0].text)
                                if "SOLD".lower() in elements_Detailed[0].text.lower() or "WANTED".lower() in elements_Detailed[0].text.lower() or "PENDING".lower() in elements_Detailed[0].text.lower():
                                    # print("aaaaaaa")
                                    try:
                                        if f"https://www.trade-a-plane.com/{url}" in str(file):
                                            nead_replase = str(file).split("%%$%%%$$$\n")
                                            for nead_replase_one_item in range(len(nead_replase)):
                                                if f"https://www.trade-a-plane.com/{url}" in nead_replase[nead_replase_one_item]:
                                                    # print(nead_replase[nead_replase_one_item].split("%%$%%")[-2])
                                                    try:
                                                        bot.delete_message(chat_id=CHANNEL_USERNAME, message_id=int(nead_replase[nead_replase_one_item].split("%%$%%")[-2]))
                                                        del nead_replase[nead_replase_one_item]
                                                    except:
                                                        pass
                                                    break
                                            rothd = "%%$%%%$$$\n"
                                            with open("info/info.txt", "wt") as f:
                                                for p in nead_replase:
                                                    if p != "":
                                                        f.write(f"{p}{rothd}")
                                            print("delete")
                                    except:
                                        pass
                                    stop_sold = 1
                                    break
                            except:
                                print("not elements Detailed")
                            for url_img in range(len(a_image)):
                                folder_path = f"image/{tipe_pars}/{iter_item}"
                                if not os.path.exists(folder_path):
                                    os.makedirs(folder_path)
                                img_data = requests.get(a_image[url_img]['href']).content
                                
                                # Генерувати унікальне ім'я файлу для кожного зображення
                                image_name = f"image/{tipe_pars}/{iter_item}/image_{url_img + 1}.jpg"

                                # Зберегти зображення в файл
                                with open(image_name, 'wb') as handler:
                                    handler.write(img_data)
                            break
                        except:
                            print("not get 1 items")
                            continue
                    else: # если элемента уже не существует
                        print("nead delete")
                        with open("info/info.txt", "r") as f:
                            file = f.read()
                        try:
                            if f"https://www.trade-a-plane.com/{url}" in str(file):
                                nead_replase = str(file).split("%%$%%%$$$\n")
                                for nead_replase_one_item in range(len(nead_replase)):
                                    if f"https://www.trade-a-plane.com/{url}" in nead_replase[nead_replase_one_item]:
                                        # print(nead_replase[nead_replase_one_item].split("%%$%%")[-2])
                                        try:
                                            bot.delete_message(chat_id=CHANNEL_USERNAME, message_id=int(nead_replase[nead_replase_one_item].split("%%$%%")[-2]))
                                            del nead_replase[nead_replase_one_item]
                                        except:
                                            pass
                                        break
                                rothd = "%%$%%%$$$\n"
                                with open("info/info.txt", "wt") as f:
                                    for p in nead_replase:
                                        if p != "":
                                            f.write(f"{p}{rothd}")
                                print("delete")
                        except:
                            pass
                        continue
                    if stop_sold == 1:
                        print("nead delete")
                        with open("info/info.txt", "r") as f:
                            file = f.read()
                        try:
                            if f"https://www.trade-a-plane.com/{url}" in str(file):
                                nead_replase = str(file).split("%%$%%%$$$\n")
                                for nead_replase_one_item in range(len(nead_replase)):
                                    if f"https://www.trade-a-plane.com/{url}" in nead_replase[nead_replase_one_item]:
                                        # print(nead_replase[nead_replase_one_item].split("%%$%%")[-2])
                                        try:
                                            bot.delete_message(chat_id=CHANNEL_USERNAME, message_id=int(nead_replase[nead_replase_one_item].split("%%$%%")[-2]))
                                            del nead_replase[nead_replase_one_item]
                                        except:
                                            pass
                                        break
                                rothd = "%%$%%%$$$\n"
                                with open("info/info.txt", "wt") as f:
                                    for p in nead_replase:
                                        if p != "":
                                            f.write(f"{p}{rothd}")
                                print("delete")
                        except:
                            pass
                        continue
                    all_info_one_element = f"{praice}%%$%%{phone}%%$%%{info_item_one}%%$%%https://www.trade-a-plane.com/{url}"
                    rothd = "%%$%%%$$$\n"
                    with open("info/info.txt", "r") as f:
                        file = f.read()
                    if f"https://www.trade-a-plane.com/{url}" in str(file):
                        print("Є url")
                        if all_info_one_element not in str(file):
                            print("replays")
                            nead_replase = str(file).split("%%$%%%$$$\n")
                            for nead_replase_one_item in range(len(nead_replase)):
                                if f"https://www.trade-a-plane.com/{url}" in nead_replase[nead_replase_one_item]:
                                    if "Call for" in praice:
                                        MESSAGE_TEXT = f"<b>{name_element_1}</b>\n{info_item_one}\n{all_info2_block}\n{praice}\n\n<b>Seller:</b>{phone}\nhttps://www.trade-a-plane.com/{url}"
                                    else:
                                        MESSAGE_TEXT = f"<b>{name_element_1}</b>\n{info_item_one}\n{all_info2_block}\n<b>Price:</b> {praice}\n\n<b>Seller:</b>{phone}\nhttps://www.trade-a-plane.com/{url}"
                                    # print(nead_replase[nead_replase_one_item].split("%%$%%")[-2])
                                    try:
                                        url_id_button = url.split("id=")[1].split("&s-type")[0]
                                        keyboard = InlineKeyboardMarkup([
                                            [InlineKeyboardButton(f'1', callback_data=f'button_1 {name_element_1} {url_id_button}')],
                                            [InlineKeyboardButton(f'2', callback_data=f'button_2 {name_element_1} {url_id_button}' )],
                                            [InlineKeyboardButton(f'3', callback_data=f'button_3 {name_element_1} {url_id_button}')],
                                            [InlineKeyboardButton(f'4', callback_data=f'button_4 {name_element_1} {url_id_button}')]
                                        ])
                                        # bot.edit_message_caption(chat_id=CHANNEL_USERNAME, message_id=nead_replase[nead_replase_one_item].split("%%$%%")[-2], caption=MESSAGE_TEXT)
                                        bot.edit_message_media(chat_id=CHANNEL_USERNAME, message_id=nead_replase[nead_replase_one_item].split("%%$%%")[-2], media=InputMediaPhoto(media=open(f'image/{tipe_pars}/{iter_item}/image_1.jpg', 'rb'), caption=MESSAGE_TEXT), reply_markup=keyboard, parse_mode='HTML')
                                        nead_replase[nead_replase_one_item] = f"{all_info_one_element}%%$%%{message_id}%%$%%{rothd}"
                                    except:
                                        pass
                                    break
                            with open("info/info.txt", "wt") as f:
                                for p in nead_replase:
                                    f.write(f"{p}{rothd}")
                            print("замінив")
                    else:
                        with open("rekl/1.txt", "r") as f:
                            reklmn_n = int(f.readline())
                            print(reklmn_n)
                            if (reklmn_n + 1) % 100 == 0:
                                sent_message_rekl = bot.send_photo(chat_id=CHANNEL_USERNAME, photo=open(f'rekl/1.jpg', 'rb'))
                        if "Call for" in praice:
                            MESSAGE_TEXT = f"<b>{name_element_1}</b>\n{info_item_one}\n{all_info2_block}\n{praice}\n\n<b>Seller:</b>{phone}\nhttps://www.trade-a-plane.com/{url}"
                        else:
                            MESSAGE_TEXT = f"<b>{name_element_1}</b>\n{info_item_one}\n{all_info2_block}\n<b>Price:</b> {praice}\n\n<b>Seller:</b>{phone}\nhttps://www.trade-a-plane.com/{url}"
                        # тг add елемент
                        for ikh in range(10):
                            try:
                                if USA == 1:
                                    USA = 0
                                    # /search?category_level1=Jets&make=LEARJET&model=60XR&listing_id=2413908&s-type=aircraft
                                    url_id_button = url.split("id=")[1].split("&s-type")[0]
                                    print(url_id_button)
                                    keyboard = InlineKeyboardMarkup([
                                    [InlineKeyboardButton(f'1', callback_data=f'button_1 {name_element_1} {url_id_button}')],
                                    [InlineKeyboardButton(f'2', callback_data=f'button_2 {name_element_1} {url_id_button}' )],
                                    [InlineKeyboardButton(f'3', callback_data=f'button_3 {name_element_1} {url_id_button}')],
                                    [InlineKeyboardButton(f'4', callback_data=f'button_4 {name_element_1} {url_id_button}')]
                                ])
                                    sent_message = bot.send_photo(chat_id=CHANNEL_USERNAME, photo=open(f'image/{tipe_pars}/{iter_item}/image_1.jpg', 'rb'), caption=MESSAGE_TEXT, reply_markup=keyboard, parse_mode='HTML')
                                else:
                                    sent_message = bot.send_photo(chat_id=CHANNEL_USERNAME, photo=open(f'image/{tipe_pars}/{iter_item}/image_1.jpg', 'rb'), caption=MESSAGE_TEXT, parse_mode='HTML')
                                with open("rekl/1.txt", "wt") as f:
                                    f.write(str(reklmn_n + 1))
                                message_id = sent_message.message_id
                                # print(message_id)
                                break
                            except RetryAfter:
                                print("trabl")
                                time.sleep(40)
                        with open("info/info.txt", "a") as f:
                            f.write(f"{all_info_one_element}%%$%%{message_id}%%$%%{rothd}")
                    iter_item += 1
                except RetryAfter as e:
                    print(f"Помилка RetryAfter: {e.retry_after}")
        except RetryAfter as e:
                    print(f"Помилка RetryAfter: {e.retry_after}")

# try:
get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Jets&s-type=aircraft&s-page_size=100", "Jets", 100)  # Jets
# except:
#     pass
try:
    get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Multi+Engine+Piston&s-type=aircraft&s-page_size=100", "Multi Engine Piston", 100)  # Multi Engine Piston
except:
    pass
try:
    get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Piston+Helicopters&s-type=aircraft&s-page_size=100", "Piston Helicopters", 100)  # Piston Helicopters
except:
    pass
try:
    get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&s-type=aircraft&s-page_size=100", "Single Engine Piston", 100)  # Single Engine Piston
except:
    pass
try:
    get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Turbine+Helicopters&s-type=aircraft&s-page_size=100", "Turbine Helicopters", 100)  # Turbine Helicopters
except:
    pass
try:
    get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Turboprop&s-type=aircraft&s-type=aircraft&s-page_size=100", "Turboprop", 100)  # Turboprop
except:
    pass

def function_a():
    print("funk a")
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Jets&s-type=aircraft&s-page_size=100", "Jets", 2)  # Jets
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Multi+Engine+Piston&s-type=aircraft&s-page_size=100", "Multi Engine Piston", 2)  # Multi Engine Piston
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Piston+Helicopters&s-type=aircraft&s-page_size=100", "Piston Helicopters", 2)  # Piston Helicopters
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&s-type=aircraft&s-page_size=100", "Single Engine Piston", 2)  # Single Engine Piston
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Turbine+Helicopters&s-type=aircraft&s-page_size=100", "Turbine Helicopters", 2)  # Turbine Helicopters
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Turboprop&s-type=aircraft&s-type=aircraft&s-page_size=100", "Turboprop", 2)  # Turboprop
    except:
        pass


def function_b():
    print("funk b")
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Jets&s-type=aircraft&s-page_size=100", "Jets", 100)  # Jets
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Multi+Engine+Piston&s-type=aircraft&s-page_size=100", "Multi Engine Piston", 100)  # Multi Engine Piston
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Piston+Helicopters&s-type=aircraft&s-page_size=100", "Piston Helicopters", 100)  # Piston Helicopters
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Single+Engine+Piston&s-type=aircraft&s-page_size=100", "Single Engine Piston", 100)  # Single Engine Piston
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Turbine+Helicopters&s-type=aircraft&s-page_size=100", "Turbine Helicopters", 100)  # Turbine Helicopters
    except:
        pass
    try:
        get_all_info_in_url("https://www.trade-a-plane.com/search?category_level1=Turboprop&s-type=aircraft&s-type=aircraft&s-page_size=100", "Turboprop", 100)  # Turboprop
    except:
        pass


schedule.every().week.at("18:00").do(function_b)


schedule.every(10).minutes.do(function_a)
while True:
    schedule.run_pending()
    time.sleep(1)
