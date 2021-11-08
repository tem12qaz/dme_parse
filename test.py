from pyvirtualdisplay import Display
from selenium import webdriver

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
    executable_path="/home/ubuntu/code/dme_parse/chromedriver"
)
display = Display(visible=0, size=(640, 480))
display.start()
driver.get('https://www.google.ru/')
print(driver.page_source)