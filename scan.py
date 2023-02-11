# main #
import os
import random
import time
import datetime
from os import system, name

# scanner #
import selenium
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium import common
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urls import urls
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from config import keys

# email #
import httplib2
import oauth2client
from oauth2client import client, tools, file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

# recaptcha #
import speech_recognition as sr
import urllib
from urllib import request
import pydub
from urllib.parse import urlparse

# EMAIL NOTIFICATOR STARTS #


SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Gmail API Python Send Email'


def checkgoogle():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        nopath = "No credentials path exists, please run gmail.bat from install directory."

        return nopath


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def SendMessage(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    if attachmentFile:
        message1 = createMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, attachmentFile)
    else:
        message1 = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
    result = SendMessageInternal(service, "me", message1)
    return result


def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"


def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}


def createMessageWithAttachment(
        sender, to, subject, msgHtml, msgPlain, attachmentFile):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      msgHtml: Html message to be sent
      msgPlain: Alternative plain text message for older email clients
      attachmentFile: The path to the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('mixed')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    message_a = MIMEMultipart('alternative')
    message_r = MIMEMultipart('related')

    message_r.attach(MIMEText(msgHtml, 'html'))
    message_a.attach(MIMEText(msgPlain, 'plain'))
    message_a.attach(message_r)

    message.attach(message_a)

    print("create_message_with_attachment: file: %s" % attachmentFile)
    content_type, encoding = mimetypes.guess_type(attachmentFile)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachmentFile, 'r')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(attachmentFile, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(attachmentFile, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(attachmentFile, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(attachmentFile)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def emailnotification(to, msg):
    to = to
    sender = "bot@gmail.com"
    subject = "AMD has restocked some " + str(msg) + "!"
    msg_html = "buyBot is trying to get you a brand new " + str(msg) + "! You need to go on your PC and ensure you " \
                                                                       "get one! GOOD LUCK!"
    msg_plain = msg
    SendMessage(sender, to, subject, msg_html, msg_plain)
    # Send message with attachment:
    # SendMessage(sender, to, subject, msg_html, msg_plain, '/path/to/file.pdf')


# EMAIL NOTIFICATOR ENDS #


def notification(t):
    # Replace below path with the absolute path
    # to chromedriver in your computer
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\joona\\AppData\\Local\\Google\\Chrome\\Selenium data")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)

    # Replace 'Friend's Name' with the name of your friend
    # or the name of a group
    # target = '"Oma1"'

    # Replace the below string with your own message
    string = "buyBot is trying to get you a brand new " + str(t) + "!"

    # x_arg = '//span[contains(@title,' + target + ')]'
    # group_title = wait.until(EC.presence_of_element_located((
    #     By.XPATH, x_arg)))
    time.sleep(3)
    name = driver.find_element_by_xpath("//*[@id='pane-side']/div[1]/div/div/div[11]/div/div/div[2]/div[1]/div["
                                        "1]/span/span")
    name.click()
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
    input_box = wait.until(EC.presence_of_element_located((
        By.XPATH, inp_xpath)))
    for i in range(1):
        input_box.send_keys(string + Keys.ENTER)
        time.sleep(1)


def add_values_in_dict(sample_dict, key, list_of_values):
    """Append multiple values to a key in the given dictionary"""
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict


def selector(p):
    products = p
    selection = int(input("What products do you want to select for a scan, give a number of a one product and press "
                          "ENTER. \n(0 ends "
                          "selection and starts the scanner): "))
    selection -= 1

    if int(selection) == -1:
        return 0

    else:
        res = list(products.keys())[int(selection)]
        max_price = input("What is the max price you are willing to pay for the product?: ")
        add = p[res]
        added = {res: add}
        selected_product = add_values_in_dict(added, res, [max_price])
        return selected_product


# def products(s):
#     options = Options()
#     options.add_argument("--incognito")
#     options.add_argument("--headless")  # Runs Chrome in headless mode.
#     options.add_argument('--no-sandbox')  # Bypass OS security model
#     options.add_argument('--disable-gpu')  # applicable to windows os only
#     options.add_argument('start-maximized')  #
#     options.add_argument('disable-infobars')
#     options.add_argument("--disable-extensions")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#         "Chrome/84.0.4147.125 Safari/537.36")
#     browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#     url = s
#     browser.get(url)
#     _html = browser.page_source
#     data = browser.find_elements_by_xpath('//*[@id="block-amd-content"]/div/div/div/div')
#
#     soup = BeautifulSoup(_html, features="lxml")
#     number = 0
#     products = {}
#
#     for match in soup.find_all('div', class_='views-row'):
#         number = number + 1
#         try:
#             name = match.find('div', class_='shop-title').text.strip()
#             price = match.find('div', class_='shop-price').text.strip()
#             buy = match.find('button', href=True, )
#             add = {name: [price, buy['href']]}
#             products |= add
#
#         except TypeError:
#             name = match.find('div', class_='shop-title').text.strip()
#             price = match.find('div', class_='shop-price').text.strip()
#             buy = 0
#             add = {name: [price, buy]}
#             products |= add
#             pass
#     browser.quit()
#     return products


def delay():
    time.sleep(random.randint(2, 3))


def afterbuy():
    print()
    keep_searching = input("Do you want to keep searching other products after succeeded buying one? Same product "
                           "won't be bought twice! (y/n): ")
    if keep_searching == "y":
        keep_looking = 1
    else:
        keep_looking = 0
    return keep_looking


# def buybot(u, p, k):
#     url = u
#     product = p
#     print("Starting buyBot\nThe bot is trying to buy: " + product)
#     print("URL: is " + url)
#     emailnotification(k["email"], product)
#
#     # notification(product)     #CALL WHATSUP NOTIFICATION
#     options = Options()
#     options.add_argument("--incognito")
#     options.add_argument("--headless")  # Runs Chrome in headless mode.
#     options.add_argument('--no-sandbox')  # Bypass OS security model
#     options.add_argument('--disable-gpu')  # applicable to windows os only
#     options.add_argument('start-maximized')  #
#     options.add_argument('disable-infobars')
#     options.add_argument("--disable-extensions")
#     options.add_argument("--window-size=1400x1000")
#     options.add_experimental_option("excludeSwitches", ['enable-logging'])
#     options.add_experimental_option("detach", True)
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#         "Chrome/84.0.4147.125 Safari/537.36")
#     driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#     driver.get(url)
#     wait = WebDriverWait(driver, 500)
#
#     try:
#         cookies = wait.until(EC.element_to_be_clickable((
#             By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
#         cookies.click()
#         # driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
#         print("Clearing cookie-window.")
#         try:
#             driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
#             print("Clearing survey")
#         except selenium.common.exceptions.NoSuchElementException:
#             pass
#         driver.get_screenshot_as_file("screenshot1.png")
#         wait.until(EC.element_to_be_clickable((
#             By.XPATH, '//*[@id="product-details-info"]/div[2]/div/div[2]/button'))).click()
#         print("Adding product to a cart")
#         # driver.find_element_by_xpath('//*[@id="product-details-info"]/div[2]/div/div[2]/button').click()
#         wait.until(EC.presence_of_element_located((
#             By.XPATH, '//*[@id="line-items-cart-container"]/div[2]/div[2]/a'))).click()
#         print("Moving to customer info page")
#         # driver.find_element_by_xpath('//*[@id="line-items-cart-container"]/div[2]/div[2]/a').click()
#
#         try:
#             driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
#         except selenium.common.exceptions.NoSuchElementException:
#             pass
#         driver.get_screenshot_as_file("screenshot2.png")
#         iframe = driver.find_element_by_xpath('//iframe[contains(@name, "cardnumber")]')
#         driver.switch_to.frame(iframe)
#         driver.find_element_by_xpath('//*[@id="ccNumber"]').send_keys(k["cardn"])
#         driver.switch_to.default_content()
#
#         iframe = driver.find_element_by_xpath('//iframe[contains(@name, "cardexpiration")]')
#         driver.switch_to.frame(iframe)
#         driver.find_element_by_xpath('//*[@id="ccExpiry"]').send_keys(k["cardexp"])
#         driver.switch_to.default_content()
#
#         iframe = driver.find_element_by_xpath('//iframe[contains(@name, "cardcvv")]')
#         driver.switch_to.frame(iframe)
#         driver.find_element_by_xpath('//*[@id="ccCVV"]').send_keys(k["cardv"])
#         driver.switch_to.default_content()
#         print("Filled creditcard info")
#         driver.get_screenshot_as_file("screenshot3.png")
#
#         driver.find_element_by_xpath('//*[@id="edit-first-name"]').send_keys(k["firstn"])
#         driver.find_element_by_xpath('//*[@id="edit-last-name"]').send_keys(k["lastn"])
#         driver.find_element_by_xpath('//*[@id="edit-address-line"]').send_keys(k["address"])
#         driver.find_element_by_xpath('//*[@id="edit-postal-code"]').send_keys(k["postal_code"])
#         driver.find_element_by_xpath('//*[@id="edit-email"]').send_keys(k["email"])
#         driver.find_element_by_xpath('//*[@id="edit-city"]').send_keys(k["city"])
#         driver.find_element_by_xpath('//*[@id="edit-phone-number"]').send_keys(k["phone"])
#
#         driver.find_element_by_xpath('//*[@id="edit-shop-country"]/option[6]').click()
#         driver.get_screenshot_as_file("screenshot4.png")
#         print("Filled customer info")
#         time.sleep(2)
#         driver.find_element_by_xpath('//*[@id="edit-submit"]').click()
#         time.sleep(2)
#         driver.find_element_by_xpath('//*[@id="payment-details"]/div[1]/div/a[1]/div/span').click()
#
#         wait.until(EC.presence_of_element_located((
#             By.XPATH, '//*[@id="edit-submit"]'))).click()
#         print("Moving to order-page")
#         # time.sleep(8)  ##*****
#
#         try:
#             driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
#         except selenium.common.exceptions.NoSuchElementException:
#             pass
#
#         try:
#             driver.find_element_by_xpath('//*[@id="fsrInvite"]/section[3]/button[2]').click()
#
#         except selenium.common.exceptions.NoSuchElementException:
#             pass
#         driver.get_screenshot_as_file("screenshot5.png")
#         print("Starting the recaptcha solver.")
#         # # # /// recaptcha solver ///
#         recaptcha = 1
#         click_audio = True
#
#         #
#         # switch to recaptcha frame
#         wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout-review"]/div[3]/div[1]')))
#         time.sleep(1)
#         frames = driver.find_elements_by_tag_name("iframe")
#         driver.switch_to.frame(frames[0])
#
#         # click on checkbox to activate recaptcha
#         driver.find_element_by_class_name("recaptcha-checkbox-border").click()
#
#         # switch to recaptcha audio control frame
#         while click_audio:
#             try:
#                 driver.switch_to.default_content()
#                 delay()
#                 frames = driver.find_elements_by_tag_name("iframe")
#                 delay()
#                 # frames = driver.find_elements_by_xpath('/html/body/div[13]/div[4]/iframe')
#                 # frames = driver.find_element_by_xpath('//iframe[contains(@name, "c-")]')
#                 driver.switch_to.frame(frames[-1])
#
#                 # rc - button
#                 # goog - inline - block
#                 # rc - button - audio
#                 # click on audio challenge
#
#                 driver.find_element_by_class_name('rc-button-audio').click()
#                 # driver.find_element_by_xpath('//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[2]').click()
#                 click_audio = False
#             except selenium.common.exceptions.NoSuchElementException:
#                 pass
#         # switch to recaptcha audio challenge frame
#         driver.switch_to.default_content()
#         frames = driver.find_elements_by_tag_name("iframe")
#         driver.switch_to.frame(frames[-1])
#         delay()
#
#         # click on the play button
#         driver.find_element_by_xpath('//*[@id=":2"]').click()
#
#         # get the mp3 audio file
#         src = driver.find_element_by_xpath('/html/body/div/div/div[6]/a').get_attribute('href')
#         print("[INFO] Audio src: %s" % src)
#         res = urlparse(src)
#         result = 'https://www.google.com/recaptcha/api2/payload?' + res.query
#
#         # download the mp3 audio file from the source
#         urllib.request.urlretrieve(result, os.getcwd() + "\\sample.mp3")
#         sound = pydub.AudioSegment.from_mp3(os.getcwd() + "\\sample.mp3")
#         sound.export(os.getcwd() + "\\sample.wav", format="wav")
#         sample_audio = sr.AudioFile(os.getcwd() + "\\sample.wav")
#         r = sr.Recognizer()
#
#         with sample_audio as source:
#             audio = r.record(source)
#
#         # translate audio to text with google voice recognition
#         key = r.recognize_google(audio)
#         print("[INFO] Recaptcha Passcode: %s" % key)
#
#         # key in results and submit
#         driver.find_element_by_id("audio-response").send_keys(key.lower())
#         time.sleep(1)
#         driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
#         print("Submit first recaptcha result")
#         driver.get_screenshot_as_file("screenshot6.png")
#         while recaptcha == 1:
#             if recaptcha == 1:
#                 delay()
#                 # get the mp3 audio file
#                 src = driver.find_element_by_xpath('/html/body/div/div/div[6]/a').get_attribute('href')
#                 print("[INFO] Audio src: %s" % src)
#                 res = urlparse(src)
#                 result = 'https://www.google.com/recaptcha/api2/payload?' + res.query
#                 # download the mp3 audio file from the source
#                 urllib.request.urlretrieve(result, os.getcwd() + "\\sample.mp3")
#                 sound = pydub.AudioSegment.from_mp3(os.getcwd() + "\\sample.mp3")
#                 sound.export(os.getcwd() + "\\sample.wav", format="wav")
#                 sample_audio = sr.AudioFile(os.getcwd() + "\\sample.wav")
#                 r = sr.Recognizer()
#
#                 with sample_audio as source:
#                     audio = r.record(source)
#
#                 # translate audio to text with google voice recognition
#                 key = r.recognize_google(audio)
#                 print("[INFO] Recaptcha Passcode: %s" % key)
#                 try:
#                     # key in results and submit
#                     driver.find_element_by_id("audio-response").send_keys(key.lower())
#                     time.sleep(1)
#                     driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
#                     print("Submit the next recaptcha results")
#                     driver.get_screenshot_as_file("screenshot7.png")
#                 except selenium.common.exceptions.ElementNotInteractableException:
#                     recaptcha = 0
#                     print("Recaptcha should be resolved")
#                     driver.get_screenshot_as_file("screenshot8.png")
#                     pass
#             else:
#                 driver.switch_to.default_content()
#                 driver.find_element_by_id("recaptcha-demo-submit").click()
#                 print("Recaptcha should be resolved")
#                 driver.get_screenshot_as_file("screenshot8.png")
#                 delay()
#
#         driver.switch_to.default_content()
#         driver.get_screenshot_as_file("screenshot9.png")
#         driver.find_element_by_xpath('//*[@id="terms-and-conditions-check"]').click()
#         print("Check terms and conditions")
#
#         # driver.find_element_by_xpath('//*[@id="newsletter-signup"]').click()
#         driver.find_element_by_xpath('//*[@id="confirm-order-link"]/button').click()
#         print("Submitted the order")
#         time.sleep(5)
#         driver.get_screenshot_as_file("screenshot10.png")
#         driver.quit()
#
#     except selenium.common.exceptions.NoSuchElementException:
#         driver.quit()
#         return 0


run = True
selection = True
scanning = True
keep_scanning = 0
stock_dict = {}
clear = lambda: os.system('cls')

if __name__ == '__main__':
    products_to_scan = {}
    # page = urls(urls['scanner_url1'])
    nopath = checkgoogle()
    # available_products = products(urls['direct_buy'])
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1400x1000")
    options.add_experimental_option("excludeSwitches", ['enable-logging'])
    options.add_experimental_option("detach", True)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/84.0.4147.125 Safari/537.36")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    url = urls['direct_buy']
    driver.get(url)
    _html = driver.page_source
    data = driver.find_elements_by_xpath('//*[@id="block-amd-content"]/div/div/div/div')

    soup = BeautifulSoup(_html, features="lxml")
    number = 0
    products = {}

    for match in soup.find_all('div', class_='views-row'):
        number = number + 1
        try:
            name = match.find('div', class_='shop-title').text.strip()
            price = match.find('div', class_='shop-price').text.strip()
            buy = match.find('button', href=True, )
            add = {name: [price, buy['href']]}
            products |= add

        except TypeError:
            name = match.find('div', class_='shop-title').text.strip()
            price = match.find('div', class_='shop-price').text.strip()
            buy = 0
            add = {name: [price, buy]}
            products |= add
            pass
    unreleased = {"AMD Radeon™ RX 6700 XT Graphics": ["???", "0"]}
    # products |= unreleased
    available_products = products
    add = 1
    clear()
    the_number = 0
    while selection:
        print()
        print("Available products for scanning:")
        for kv in available_products.items():
            the_number += 1
            amd_price = kv[1][0]
            amd_price = amd_price.replace('.', '')
            print(the_number, ": ", kv[0], ': \t', 'price = ', amd_price)
        print()

        add = selector(available_products)
        if add == 0:
            clear()
            selection = False
            print()
            print("You have selected:")
            print()
            for kv in products_to_scan.items():
                print(kv[0], ': \t', 'Current price: ', kv[1][0], " - Max price is set to: ", kv[1][2], "€.")
            keep_scanning = afterbuy()
            the_number = 0
        else:
            clear()
            products_to_scan |= add
            print()
            print("You have selected:")
            for kv in products_to_scan.items():
                print(kv[0], ': \t', 'Current price: ', kv[1][0], " - Max price is set to: ", kv[1][2], "€.")
            the_number = 0
            print()

    f = open("result.txt", "a")
    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(ts).strftime(' - %Y%m%d_%H:%M:%S - ')
    f.write("\n" + sttime + " - Bot has started scanning -")
    f.close()
    while scanning:
        driver.quit()
        print("Checking products...")
        # available_products = products(urls['direct_buy'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(url)
        time.sleep(3)
        _html = driver.page_source
        data = driver.find_elements_by_xpath('//*[@id="block-amd-content"]/div/div/div/div')

        soup = BeautifulSoup(_html, features="lxml")
        number = 0
        products = {}

        for match in soup.find_all('div', class_='views-row'):
            number = number + 1
            try:
                name = match.find('div', class_='shop-title').text.strip()
                price = match.find('div', class_='shop-price').text.strip()
                buy = match.find('button', href=True, )
                main = 1
                product_page_url = 0
                add = {name: [price, buy['href'], main, product_page_url]}
                products |= add

            except TypeError:
                name = match.find('div', class_='shop-title').text.strip()
                price = match.find('div', class_='shop-price').text.strip()
                buy = 0
                main = 0
                add = {name: [price, buy, main]}
                products |= add
                product_page = match.find('a', href=True, )
                product_page = product_page['href']
                parsed_product_page = urlparse(product_page)
                parsed = urllib.parse.urlsplit(str(parsed_product_page))
                product_page_url = f"https://www.amd.com/en/direct-buy/{parsed.path.split('/')[-2]}/fi"

                cart_link = 0
                driver.get(product_page_url)
                product_html = driver.page_source
                other_soup = BeautifulSoup(product_html, features="lxml")
                for match2 in other_soup.find_all('div', class_='product-page-description'):
                    try:
                        check_if_exists = match2.find('button', href=True, )
                        cart_link = check_if_exists['href']
                        pass
                    except TypeError:
                        product_page_url = 0
                        pass
                products[str(name)].append(product_page_url)
                pass

        available_products = products

        clear()
        print()
        print("------- Selected products ---------")
        print("You have selected:")
        for kv in products_to_scan.items():
            print(kv[0], ': \t', kv[1][0], " - Max price is set to: ", kv[1][2], "€.")
        print()
        print("------ Products in AMD's website ------")
        print()
        for kv in available_products.items():
            time.sleep(0.1)
            buy_success = 1
            check = kv[1][1]
            check_product_page = kv[1][3]
            found_item = kv[0]
            in_stock = {found_item: 'Available'}
            if check == 0 and check_product_page == 0:
                amd_price = kv[1][0]
                amd_price = amd_price.replace('.', '')
                print(kv[0], ': \t', amd_price, "\t - Not available")

            if check != 0 or check_product_page != 0:
                try:
                    if check != 0:
                        print(kv[0], ': \t', kv[1][0], "\t - FOUND IN STOCK FROM MAINPAGE!!")
                    if check_product_page != 0:
                        print(kv[0], ': \t', kv[1][0], "\t - FOUND IN STOCK FROM PRODUCTPAGE!!")
                    item_key = kv[0]
                    current_price = kv[1][0]
                    price = current_price.replace('€', '')
                    price = price.replace(' ', '')
                    price = price.replace('.', '')
                    price = price.replace(',', '.')
                    max_price = products_to_scan[str(item_key)][2]

                    try:
                        if float(price) <= float(max_price):
                            print("Product is available for purchasing!")
                            if found_item in available_products:
                                print("Starting buying-module...please wait.")
                                f = open("result.txt", "a")
                                ts = time.time()
                                sttime = datetime.datetime.fromtimestamp(ts).strftime(' - %Y%m%d_%H:%M:%S - ')
                                f.write(
                                    "\n" + sttime + " - Bot has started buying-module, it's trying to buy " + found_item + ". -")
                                f.close()
                                # product_url_base = kv[1][1] + "/"
                                # parsed_product_url = urlparse(product_url_base)
                                # parsed = urllib.parse.urlsplit(str(parsed_product_url))
                                # product_url = f"https://www.amd.com/en/direct-buy/{parsed.path.split('/')[-2]}/fi"
                                # buy_success = buybot(product_url, found_item, keys)
                                k = keys
                                product = found_item
                                print("The bot is trying to buy: " + product)
                                print("URL: is " + url)
                                wait = WebDriverWait(driver, 15)

                                # notification(product)     #CALL WHATSAPP NOTIFICATION
                                if kv[1][2] == 1:
                                    driver.get(url)
                                    driver.get_screenshot_as_file("screenshot1.png")
                                    try:
                                        cookies = wait.until(EC.element_to_be_clickable((
                                            By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
                                        cookies.click()
                                        # driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                                        print("Clearing cookie-window.")
                                        try:
                                            driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
                                            print("Clearing survey")
                                        except (selenium.common.exceptions.NoSuchElementException,
                                                selenium.common.exceptions.ElementClickInterceptedException):
                                            pass

                                        # add_to_cart = "//button[.//span[text()=""'+product+'""]]"
                                        # print(add_to_cart)
                                        wait.until(EC.element_to_be_clickable((
                                            By.XPATH, "//button[.//span[text()='" + product + "']]"))).click()
                                        print("Adding product to a cart")
                                        # driver.find_element_by_xpath('//*[@id="product-details-info"]/div[2]/div/div[2]/button').click()
                                        wait.until(EC.presence_of_element_located((
                                            By.XPATH, '//*[@id="line-items-cart-container"]/div[2]/div[2]/a'))).click()
                                        print("Moving to customer info page")
                                        # driver.find_element_by_xpath('//*[@id="line-items-cart-container"]/div[2]/div[2]/a').click()

                                        try:
                                            driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
                                        except selenium.common.exceptions.NoSuchElementException:
                                            pass
                                    except (selenium.common.exceptions.NoSuchElementException,
                                            selenium.common.exceptions.TimeoutException):
                                        buy_success = 0
                                        pass
                                if kv[1][2] == 0:
                                    product_url = kv[1][3]
                                    driver.get(product_url)
                                    driver.get_screenshot_as_file("screenshot1.png")

                                    try:
                                        cookies = wait.until(EC.element_to_be_clickable((
                                            By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
                                        cookies.click()
                                        # driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                                        print("Clearing cookie-window.")
                                        try:
                                            driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
                                            print("Clearing survey")
                                        except selenium.common.exceptions.NoSuchElementException:
                                            pass
                                        driver.get_screenshot_as_file("screenshot1.png")
                                        wait.until(EC.element_to_be_clickable((
                                            By.XPATH, '//*[@id="product-details-info"]/div[2]/div/div[2]/button'))).click()
                                        print("Adding product to a cart")
                                        # driver.find_element_by_xpath('//*[@id="product-details-info"]/div[2]/div/div[2]/button').click()
                                        wait.until(EC.presence_of_element_located((
                                            By.XPATH, '//*[@id="line-items-cart-container"]/div[2]/div[2]/a'))).click()
                                        print("Moving to customer info page")
                                        # driver.find_element_by_xpath('//*[@id="line-items-cart-container"]/div[2]/div[2]/a').click()

                                        try:
                                            driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
                                        except selenium.common.exceptions.NoSuchElementException:
                                            pass
                                    except (selenium.common.exceptions.NoSuchElementException,
                                            selenium.common.exceptions.TimeoutException):
                                        buy_success = 0
                                        pass
                                try:
                                    driver.get_screenshot_as_file("screenshot2.png")
                                    iframe = driver.find_element_by_xpath('//iframe[contains(@name, "cardnumber")]')
                                    driver.switch_to.frame(iframe)
                                    driver.find_element_by_xpath('//*[@id="ccNumber"]').send_keys(k["cardn"])
                                    driver.switch_to.default_content()

                                    iframe = driver.find_element_by_xpath('//iframe[contains(@name, "cardexpiration")]')
                                    driver.switch_to.frame(iframe)
                                    driver.find_element_by_xpath('//*[@id="ccExpiry"]').send_keys(k["cardexp"])
                                    driver.switch_to.default_content()

                                    iframe = driver.find_element_by_xpath('//iframe[contains(@name, "cardcvv")]')
                                    driver.switch_to.frame(iframe)
                                    driver.find_element_by_xpath('//*[@id="ccCVV"]').send_keys(k["cardv"])
                                    driver.switch_to.default_content()
                                    print("Filled creditcard info")
                                    driver.get_screenshot_as_file("screenshot3.png")

                                    driver.find_element_by_xpath('//*[@id="edit-first-name"]').send_keys(k["firstn"])
                                    driver.find_element_by_xpath('//*[@id="edit-last-name"]').send_keys(k["lastn"])
                                    driver.find_element_by_xpath('//*[@id="edit-address-line"]').send_keys(k["address"])
                                    driver.find_element_by_xpath('//*[@id="edit-postal-code"]').send_keys(
                                        k["postal_code"])
                                    driver.find_element_by_xpath('//*[@id="edit-email"]').send_keys(k["email"])
                                    driver.find_element_by_xpath('//*[@id="edit-city"]').send_keys(k["city"])
                                    driver.find_element_by_xpath('//*[@id="edit-phone-number"]').send_keys(k["phone"])

                                    driver.find_element_by_xpath('//*[@id="edit-shop-country"]/option[6]').click()
                                    driver.get_screenshot_as_file("screenshot4.png")
                                    print("Filled customer info")
                                    time.sleep(2)
                                    driver.find_element_by_xpath('//*[@id="edit-submit"]').click()
                                    time.sleep(2)
                                    driver.find_element_by_xpath(
                                        '//*[@id="payment-details"]/div[1]/div/a[1]/div/span').click()

                                    wait.until(EC.presence_of_element_located((
                                        By.XPATH, '//*[@id="edit-submit"]'))).click()
                                    print("Moving to order-page")
                                    # time.sleep(8)  ##*****

                                    try:
                                        driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
                                    except selenium.common.exceptions.NoSuchElementException:
                                        pass

                                    try:
                                        driver.find_element_by_xpath(
                                            '//*[@id="fsrInvite"]/section[3]/button[2]').click()

                                    except selenium.common.exceptions.NoSuchElementException:
                                        pass
                                    driver.get_screenshot_as_file("screenshot5.png")
                                    print("Starting the recaptcha solver.")
                                    # # # /// recaptcha solver ///
                                    recaptcha = 1
                                    click_audio = True

                                    #
                                    # switch to recaptcha frame
                                    wait.until(EC.presence_of_element_located(
                                        (By.XPATH, '//*[@id="checkout-review"]/div[3]/div[1]')))
                                    time.sleep(1)
                                    frames = driver.find_elements_by_tag_name("iframe")
                                    driver.switch_to.frame(frames[0])

                                    # click on checkbox to activate recaptcha
                                    driver.find_element_by_class_name("recaptcha-checkbox-border").click()

                                    # switch to recaptcha audio control frame
                                    while click_audio:
                                        try:
                                            driver.switch_to.default_content()
                                            delay()
                                            frames = driver.find_elements_by_tag_name("iframe")
                                            delay()
                                            # frames = driver.find_elements_by_xpath('/html/body/div[13]/div[4]/iframe')
                                            # frames = driver.find_element_by_xpath('//iframe[contains(@name, "c-")]')
                                            driver.switch_to.frame(frames[-1])

                                            # rc - button
                                            # goog - inline - block
                                            # rc - button - audio
                                            # click on audio challenge

                                            driver.find_element_by_class_name('rc-button-audio').click()
                                            # driver.find_element_by_xpath('//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[2]').click()
                                            click_audio = False
                                        except selenium.common.exceptions.NoSuchElementException:
                                            pass
                                    # switch to recaptcha audio challenge frame
                                    driver.switch_to.default_content()
                                    frames = driver.find_elements_by_tag_name("iframe")
                                    driver.switch_to.frame(frames[-1])
                                    delay()

                                    # click on the play button
                                    driver.find_element_by_xpath('//*[@id=":2"]').click()

                                    # get the mp3 audio file
                                    src = driver.find_element_by_xpath('/html/body/div/div/div[6]/a').get_attribute(
                                        'href')
                                    print("[INFO] Audio src: %s" % src)
                                    res = urlparse(src)
                                    result = 'https://www.google.com/recaptcha/api2/payload?' + res.query

                                    # download the mp3 audio file from the source
                                    urllib.request.urlretrieve(result, os.getcwd() + "\\sample.mp3")
                                    sound = pydub.AudioSegment.from_mp3(os.getcwd() + "\\sample.mp3")
                                    sound.export(os.getcwd() + "\\sample.wav", format="wav")
                                    sample_audio = sr.AudioFile(os.getcwd() + "\\sample.wav")
                                    r = sr.Recognizer()

                                    with sample_audio as source:
                                        audio = r.record(source)

                                    # translate audio to text with google voice recognition
                                    key = r.recognize_google(audio)
                                    print("[INFO] Recaptcha Passcode: %s" % key)

                                    # key in results and submit
                                    driver.find_element_by_id("audio-response").send_keys(key.lower())
                                    time.sleep(1)
                                    driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
                                    print("Submit first recaptcha result")
                                    driver.get_screenshot_as_file("screenshot6.png")
                                    while recaptcha == 1:
                                        if recaptcha == 1:
                                            delay()
                                            # get the mp3 audio file
                                            src = driver.find_element_by_xpath(
                                                '/html/body/div/div/div[6]/a').get_attribute('href')
                                            print("[INFO] Audio src: %s" % src)
                                            res = urlparse(src)
                                            result = 'https://www.google.com/recaptcha/api2/payload?' + res.query
                                            # download the mp3 audio file from the source
                                            urllib.request.urlretrieve(result, os.getcwd() + "\\sample.mp3")
                                            sound = pydub.AudioSegment.from_mp3(os.getcwd() + "\\sample.mp3")
                                            sound.export(os.getcwd() + "\\sample.wav", format="wav")
                                            sample_audio = sr.AudioFile(os.getcwd() + "\\sample.wav")
                                            r = sr.Recognizer()

                                            with sample_audio as source:
                                                audio = r.record(source)

                                            # translate audio to text with google voice recognition
                                            key = r.recognize_google(audio)
                                            print("[INFO] Recaptcha Passcode: %s" % key)
                                            try:
                                                # key in results and submit
                                                driver.find_element_by_id("audio-response").send_keys(key.lower())
                                                time.sleep(1)
                                                driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
                                                print("Submit the next recaptcha results")
                                                driver.get_screenshot_as_file("screenshot7.png")
                                            except selenium.common.exceptions.ElementNotInteractableException:
                                                recaptcha = 0
                                                print("Recaptcha should be resolved")
                                                driver.get_screenshot_as_file("screenshot8.png")
                                                pass
                                        else:
                                            driver.switch_to.default_content()
                                            driver.find_element_by_id("recaptcha-demo-submit").click()
                                            print("Recaptcha should be resolved")
                                            driver.get_screenshot_as_file("screenshot8.png")
                                            delay()

                                    driver.switch_to.default_content()
                                    driver.get_screenshot_as_file("screenshot9.png")
                                    driver.find_element_by_xpath('//*[@id="terms-and-conditions-check"]').click()
                                    print("Check terms and conditions")

                                    # driver.find_element_by_xpath('//*[@id="newsletter-signup"]').click()
                                    driver.find_element_by_xpath('//*[@id="confirm-order-link"]/button').click()
                                    print("Submitted the order")
                                    time.sleep(10)
                                    driver.get_screenshot_as_file("screenshot10.png")

                                except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.TimeoutException):
                                    buy_success = 0
                                    pass
                                if buy_success == 0:
                                    print("Bot has failed to buy " + found_item + ".")
                                    f = open("result.txt", "a")
                                    ts = time.time()
                                    sttime = datetime.datetime.fromtimestamp(ts).strftime(' - %Y%m%d_%H:%M:%S - ')
                                    f.write(
                                        "\n" + sttime + " - Bot has failed to buy " + found_item + ". -")
                                    f.close()
                                    pass
                                else:

                                    print("Bot has accomplished the buying process.")
                                    f = open("result.txt", "a")
                                    ts = time.time()
                                    sttime = datetime.datetime.fromtimestamp(ts).strftime(' - %Y%m%d_%H:%M:%S - ')
                                    f.write(
                                        "\n" + sttime + " - Bot has accomplished the buying process of " + found_item + ". -")
                                    f.close()
                                    products_to_scan.pop(str(item_key), None)
                                    emailnotification(k["email"], product)
                                    if keep_scanning == 0:
                                        scanning = False
                                        break
                        else:
                            if found_item in stock_dict:
                                pass
                            else:
                                stock_dict |= in_stock
                                f = open("result.txt", "a")
                                ts = time.time()
                                sttime = datetime.datetime.fromtimestamp(ts).strftime(' - %Y%m%d_%H:%M:%S - ')
                                f.write(
                                    "\n" + sttime + " - " + found_item + " is in stock, but it cost more than you are willing to pay!!!")
                                f.close()
                            print(kv[0], "is in stock, but it cost more than you are willing to pay!!!")
                            print()
                    except KeyError:
                        pass

                except KeyError:
                    if found_item in stock_dict:
                        pass
                    else:
                        stock_dict |= in_stock
                        f = open("result.txt", "a")
                        ts = time.time()
                        sttime = datetime.datetime.fromtimestamp(ts).strftime(' - %Y%m%d_%H:%M:%S - ')
                        f.write("\n" + sttime + " - " + found_item + " is in stock, but you haven't selected it.")
                        f.close()
                    print(kv[0], "is available, but you haven't selected it!")
                    print()
                    pass
        if scanning:
            print()
            print("Re-checking in 5 seconds...")
        else:
            driver.quit()
            print("Ending the scan.")
