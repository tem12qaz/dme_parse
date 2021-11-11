# данные подключения к бд
PG_USER = 'dme_parse'
PG_PASSWORD = 'in9df879!#uihhb932B@8'
PG_HOST = 'localhost:5432'
PG_DATABASE = 'dme_parse'

# тексты сообщений
status_messages = {
    1: 'Ваш груз, мест={place}, вес={weight}кг прошёл оформление авиа перевозки{to}',
    2: 'Ваш груз, мест={place}, вес={weight}кг готов к загрузке в ВС для авиа перевозки в {to}',
    3: 'Ваш груз, мест={place}, вес={weight}кг вылетел в {to}'
}

# данные email
EMAIL_ADDRESS = 'tem12qaz@yandex.ru'
EMAIL_PASSWORD = 'xwtapxohafbgujhl'
EMAIL_SUBJECT = 'Информация о грузе'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465

# время между проверками накладных
TIME_SLEEP = 180

CHROMEDRIVER_PATH = "/root/code/dme_parse/chromedriver"

class Configuration(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'
    SQLALCHEMY_POOL_SIZE = 1

    SECRET_KEY = 'something very secret'

    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

