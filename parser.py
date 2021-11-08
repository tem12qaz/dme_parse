import time

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4

from config import TIME_SLEEP, CHROMEDRIVER_PATH
from flask_app_init import db
from mail import send_mail
from models import Invoice

url = 'https://business.dme.ru/cargo/'


def driver_init():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        options=options,
        executable_path=CHROMEDRIVER_PATH
    )
    display = Display(visible=0, size=(640, 480))
    display.start()
    return driver


def get_status(status_text: str, departure_time: str):
    if status_text == 'Комплектация на рейс/Груз принят к перевозке':
        if departure_time == '':
            return 1
        else:
            return 2
    elif status_text == 'Перевозка выполнена/-Перевозка выполнена-':
        return 3
    else:
        return 0


def get_result(driver: webdriver.Chrome, number: str):
    driver.get(url)
    driver.find_element(by=By.ID, value='NumberFirstPart').send_keys(number[:3])
    driver.find_element(by=By.ID, value='NumberSecondPart').send_keys(number[3:])
    driver.find_element(by=By.CLASS_NAME, value='submit w155').click()

    time.sleep(2)

    soup = bs4(driver.page_source, 'html.parser')
    table = soup.find('table', class_='table_style_3 table_style_cargo')
    params = table.find_all('td')

    to = params[1].text
    status = params[2].text
    departure_time = params[3].text
    place = params[5].text
    weight = params[6].text

    return to, status, departure_time, place, weight


def parse_all():
    invoices = Invoice.query.all()
    driver, display = driver_init()

    for invoice in invoices:
        to, status, departure_time, place, weight = get_result(driver, invoice.number)
        status = get_status(status, departure_time)

        if invoice.status == status:
            continue

        send_mail(invoice.email, status, (place, weight, to))

        if status == 3:
            db.session.delete(invoice)
        else:
            invoice.status = status

        db.session.commit()


def parse_cycle():
    parse_all()
    time.sleep(TIME_SLEEP)

