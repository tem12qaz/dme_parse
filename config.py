# данные подключения к бд
PG_USER = 'dme_parse'
PG_PASSWORD = 'in9df879!#uihhb932B8'
PG_HOST = 'localhost:5432'
PG_DATABASE = 'dme_parse'

# данные email
EMAIL_ADDRESS = 'vtcargo@awbtrack.online'
EMAIL_PASSWORD = 'ejxissciqcumhcvw'
EMAIL_SUBJECT = 'Информация о статусе авиа грузоперевозки'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465

# время между проверками накладных
TIME_SLEEP = 1200

CHROMEDRIVER_PATH = "/root/code/dme_parse/chromedriver"

class Configuration(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'
    SQLALCHEMY_POOL_SIZE = 1

    SECRET_KEY = 'someth3489rh6&r65r^R#2$%GkBHJKN98 secret'

    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

