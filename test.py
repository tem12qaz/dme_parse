import time
import zipfile

from selenium import webdriver
from selenium_stealth import stealth
from pyvirtualdisplay import Display

# PROXY = ('45.130.130.172', '8000', 'rMSWjv', 'J7Ytps')
PROXY = ('217.29.63.202', '28329', 'CUgpsz', 'hxoG2b')


def chrome_proxy_auth(chrome_options, proxy):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % proxy

    pluginfile = 'proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    chrome_options.add_extension(pluginfile)
    return chrome_options


def init_chrome(headless=False, tor=False, win=False, proxy=False):
    options = webdriver.ChromeOptions()

    if not headless:
        if not win:
            display = Display(visible=0, size=(640, 480))
            display.start()
    else:
        options.add_argument("--headless")

    if tor:
        options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

    if proxy:
        options = chrome_proxy_auth(options, PROXY)
        pass
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        options=options
    )

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    if headless or win:
        return [driver]

    else:
        return [driver, display]


cookies = {
            'visid_incap_242093': 'HjHMEm/HTcy/fpR0B9fX5HyPoGAAAAAAQUIPAAAAAAC1wTJjoYSZb1O9SlAkDlu8',
            'copartTimezonePref': '%7B%22displayStr%22%3A%22MSK%22%2C%22offset%22%3A3%2C%22dst%22%3Afalse%2C%22windowsTz%22%3A%22Europe%2FMinsk%22%7D',
            'timezone': 'Europe%2FMinsk',
            's_fid': '23D73D5664338974-3D5DE341A5E5FA63',
            's_cc': 'true',
            'userLang': 'ru',
            'g2usersessionid': '6e26e86c9d293415fecd71ce3d64f555',
            'G2JSESSIONID': 'ADC7FF661F9A142D361536E0699ACA3E-n1',
            'incap_ses_8219_242093': 'z5PNCdHp7whFjX95IMEPcvbQ6mAAAAAAeUBPUiKbm8zDcSHlCAGfiw==',
            's_depth': '1',
            's_vnum': '1628593658046%26vn%3D1',
            's_invisit': 'true',
            's_lv_s': 'More%20than%2030%20days',
            's_pv': 'public%3AsearchResults',
            's_ppvl': 'public%253Ahomepage%2C85%2C20%2C934%2C1920%2C934%2C1920%2C1080%2C1%2CP',
            's_sq': 'copart-g2-us-prod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dpublic%25253AsearchResults%2526link%253D%2525D0%252593%2525D0%2525BE%2525D0%2525B4%2526region%253Dfilters-collapse-1%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dpublic%25253AsearchResults%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.copart.com%25252F%252523collapseinside5%2526ot%253DA',
            's_nr': '1626002450509-New',
            's_lv': '1626002450511',
            's_ppv': 'public%253AsearchResults%2C49%2C34%2C934%2C1094%2C934%2C1920%2C1080%2C1%2CP',
            'userCategory': 'RPU'

        }
headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'www.copart.com',
            'Origin': 'https://www.copart.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Referer': 'https://www.copart.com/ru/lotSearchResults/?free=true&query=toyota',
            'Content-Length': '3697',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'X-XSRF-TOKEN': '9c94d64e-2187-4a40-a816-5df9365d4757',
        }
        # print(f'+++++++++++++++++++++{filter_year}',{self.car})
data = {
            'raw': '1',
            'columns[0][data]': '0',
            'columns[0][name]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'false',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': '1',
            'columns[1][name]': '',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'false',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'columns[2][data]': '2',
            'columns[2][name]': '',
            'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'true',
            'columns[2][search][value]': '',
            'columns[2][search][regex]': 'false',
            'columns[3][data]': '3',
            'columns[3][name]': '',
            'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'true',
            'columns[3][search][value]': '',
            'columns[3][search][regex]': 'false',
            'columns[4][data]': '4',
            'columns[4][name]': '',
            'columns[4][searchable]': 'true',
            'columns[4][orderable]': 'true',
            'columns[4][search][value]': '',
            'columns[4][search][regex]': 'false',
            'columns[5][data]': '5',
            'columns[5][name]': '',
            'columns[5][searchable]': 'true',
            'columns[5][orderable]': 'true',
            'columns[5][search][value]': '',
            'columns[5][search][regex]': 'false',
            'columns[6][data]': '6',
            'columns[6][name]': '',
            'columns[6][searchable]': 'true',
            'columns[6][orderable]': 'true',
            'columns[6][search][value]': '',
            'columns[6][search][regex]': 'false',
            'columns[7][data]': '7',
            'columns[7][name]': '',
            'columns[7][searchable]': 'true',
            'columns[7][orderable]': 'true',
            'columns[7][search][value]': '',
            'columns[7][search][regex]': 'false',
            'columns[8][data]': '8',
            'columns[8][name]': '',
            'columns[8][searchable]': 'true',
            'columns[8][orderable]': 'true',
            'columns[8][search][value]': '',
            'columns[8][search][regex]': 'false',
            'columns[9][data]': '9',
            'columns[9][name]': '',
            'columns[9][searchable]': 'true',
            'columns[9][orderable]': 'true',
            'columns[9][search][value]': '',
            'columns[9][search][regex]': 'false',
            'columns[10][data]': '10',
            'columns[10][name]': '',
            'columns[10][searchable]': 'true',
            'columns[10][orderable]': 'true',
            'columns[10][search][value]': '',
            'columns[10][search][regex]': 'false',
            'columns[11][data]': '11',
            'columns[11][name]': '',
            'columns[11][searchable]': 'true',
            'columns[11][orderable]': 'true',
            'columns[11][search][value]': '',
            'columns[11][search][regex]': 'false',
            'columns[12][data]': '12',
            'columns[12][name]': '',
            'columns[12][searchable]': 'true',
            'columns[12][orderable]': 'true',
            'columns[12][search][value]': '',
            'columns[12][search][regex]': 'false',
            'columns[13][data]': '13',
            'columns[13][name]': '',
            'columns[13][searchable]': 'true',
            'columns[13][orderable]': 'true',
            'columns[13][search][value]': '',
            'columns[13][search][regex]': 'false',
            'columns[14][data]': '14',
            'columns[14][name]': '',
            'columns[14][searchable]': 'true',
            'columns[14][orderable]': 'false',
            'columns[14][search][value]': '',
            'columns[14][search][regex]': 'false',
            'columns[15][data]': '15',
            'columns[15][name]': '',
            'columns[15][searchable]': 'true',
            'columns[15][orderable]': 'false',
            'columns[15][search][value]': '',
            'columns[15][search][regex]': 'false',
            'start': '0',
            'length': '20',
            'search[value]': '',
            'search[regex]': 'false',
            'filter[FETI]': 'buy_it_now_code:B1',
            'filter[YEAR]': 2010,
            'query': 'Ford Mustang',
            'watchListOnly': 'false',
            'freeFormSearch': 'true',
            'page': '0',
            'size': '100',
        }


def parse(url):
    driver_display = init_chrome(headless=True)

    if len(driver_display) == 2:
        driver, display = driver_display
    else:
        driver = driver_display[0]

    driver.get('https://www.copart.com/public_')
    driver.delete_all_cookies()
    time.sleep(3)
    for name, value in cookies.items():
        driver.add_cookie({'name': name, 'value': value})

    driver.
    print(driver.page_source)
    driver.close()

    if len(driver_display) == 2:
        display.stop()


# parse('https://meshok.net/item/254068667')

with open('ee.txt') as f:
    text = f.read()
    text = text.replace('=', "': '")
    text = text.replace('; ', "',\n'")
    text = "'" + text
    print(text)
