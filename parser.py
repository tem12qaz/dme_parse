import time
import traceback

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4

from config import TIME_SLEEP, CHROMEDRIVER_PATH
from flask_app_init import db
from mail import send_mail
from models import Invoice

dme_url = 'https://business.dme.ru/cargo/'
vko_url = 'http://cargo.vnukovo.ru/e-cargo/tracking/'


def driver_init():
    options = webdriver.ChromeOptions()
    # options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        options=options,
        # executable_path=CHROMEDRIVER_PATH
    )
    # display = Display(visible=0, size=(640, 480))
    # display.start()
    return driver


def dme_get_status(status_text: str, departure_time: str):
    if status_text == 'Комплектация на рейс/Груз принят к перевозке':
        if departure_time == ' ':
            return 1
        else:
            return 2
    elif status_text == 'Перевозка выполнена/-Перевозка выполнена-':
        return 3
    else:
        return 0


def vko_get_status(status_text: str, _):
    print(status_text)
    if 'Принята на склад' in status_text:
        return 1
    elif 'Груз в зоне комплектации' in status_text:
        return 2
    elif 'Улетела' in status_text:
        return 3
    else:
        return 0


def dme_get_result(driver: webdriver.Chrome, number: str):
    try:
        driver.get(dme_url)
        driver.find_element(by=By.ID, value='NumberFirstPart').send_keys(number.split('-')[0])
        driver.find_element(by=By.ID, value='NumberSecondPart').send_keys(number.split('-')[1])
        driver.find_element(by=By.CLASS_NAME, value='w155').click()

        time.sleep(2)

        soup = bs4(driver.page_source, 'html.parser')
        table = soup.find('table', class_='table_style_3 table_style_cargo')
        params = table.find_all('td')

        to = params[1].text.split('->')[-1]
        status = params[2].text
        departure_time = params[3].text
        place = params[5].text
        weight = params[6].text
        print(to, status, departure_time, place, weight)
    except:
        return 0, 0, 0, 0, 0

    return to, status, departure_time, place, weight


def vko_get_result(driver: webdriver.Chrome, number: str):
    try:
        driver.get(vko_url)
        driver.switch_to.frame(driver.find_element(by=By.TAG_NAME, value='iframe'))

        driver.find_element(by=By.XPATH, value="//input[@name='fPREAWB']").send_keys(number.split('-')[0].replace(' ', ''))
        driver.find_element(by=By.XPATH, value="//input[@name='fNUMAWB']").send_keys(number.split('-')[1].replace(' ', ''))
        driver.find_element(by=By.XPATH, value="//input[@value='Показать информацию (Search)']").click()

        time.sleep(2)
        soup = bs4(driver.page_source, 'html.parser')
        table = soup.find_all('table')[1]
        params = table.find_all('tr')
        #driver.save_screenshot('eee.png')
        print(params[1])
        if params[1].find('input')['value'] == 'RU':
            status = params[1].find_all('input')[1]['value']
            departure_time = params[1].find_all('input')[3]['value']
            to = params[1].find_all('input')[4]['value']

        else:
            status = params[1].find('input')['value']
            departure_time = ''
            to = soup.find_all('table')[4].find_all('td')[3].find('input')['value']

        params = soup.find_all('table')[5].find_all('tr')[2].find_all('input')

        place = params[0]['value']
        weight = params[1]['value']
        print(to, status, departure_time, place, weight)
    except:
        print(traceback.format_exc())
        return 0, 0, 0, 0, 0

    return to, status, departure_time, place, weight


airports = [
    (dme_get_result, dme_get_status),
    (vko_get_result, vko_get_status)
]


def parse(driver, invoice):
    for airport in airports:
        to, status, departure_time, place, weight = airport[0](driver, invoice.number)
        status = airport[1](status, departure_time)
        if status != 0:
            break

    print(to, status, departure_time, place, weight, flush=True)

    if invoice.status == status:
        return

    if invoice.place and invoice.weight and invoice.place != '-' and invoice.weight != '-':
        for i in range(len(invoice.email.split(' '))):
            print('-------')
            send_mail(
                [invoice.email.split(' ')[i]],
                status,
                (str(invoice.place.split(' ')[i]), str(invoice.weight.split(' ')[i]), to,
                 str(invoice.sender.split(';')[i]), str(invoice.recipient.split(';')[i]))
            )
    else:
        if invoice.recipient and invoice.sender:
            send_mail(
                invoice.email.split(' '),
                status,
                (place, weight, to, invoice.sender, invoice.recipient)
            )
        else:
            send_mail(
                invoice.email.split(' '),
                status,
                (place, weight, to, None, None)
            )
    if status == 3:
        db.session.delete(invoice)
    else:
        invoice.status = status

    db.session.commit()


def parse_all():
    invoices = Invoice.query.all()
    driver = driver_init()
    exc = 0

    for invoice in invoices:
        time.sleep(20)
        exc = 0
        while exc < 2:
            print(invoice.number, flush=True)
            try:
                parse(driver, invoice)

            except Exception as e:
                print(traceback.format_exc(), flush=True)

                exc += 1
                time.sleep(6)
            else:
                exc = 0
                break

    driver.close()
    # display.stop()


def parse_cycle():
    while True:
        parse_all()
        time.sleep(TIME_SLEEP)
