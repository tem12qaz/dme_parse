import time
import zipfile

from fake_useragent import UserAgent
from selenium import webdriver
from selenium_stealth import stealth
from pyvirtualdisplay import Display


PROXY = ('45.130.130.172', '8000', 'rMSWjv', 'J7Ytps')


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
        executable_path="/root/code/dme_parse/chromedriver" if not win else 'chromedriver.exe',
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


COOKIES = {
    'yandexuid': '6816921641636721023',
    'yuidss': '6816921641636721023',
    'yabs-sid': '1630863921636721023',
    'i': 'klQnrWLCiYtfHs/+6tiSR2J+LVTQ41DEpEe24UpKhZEMAxkXemAgBxrJfmPIMsjkyY5tMH3Jrp8EEmkJGnwFDtuFoiQ=',
    'ymex': '1952081023.yrts.1636721023#1952081023.yrtsi.1636721023',
}


def parse(url):
    driver_display = init_chrome()

    if len(driver_display) == 2:
        driver, display = driver_display
    else:
        driver = driver_display[0]

    driver.get('https://meshok.net/_______________________________')
    driver.delete_all_cookies()
    time.sleep(3)
    for name, value in COOKIES.items():
        driver.add_cookie({'name': name, 'value': value})

    driver.get(url)
    print(driver.page_source)
    driver.close()

    if len(driver_display) == 2:
        display.stop()


parse('https://meshok.net/item/254068667')


