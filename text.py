status_messages = {
    1: 'Ваш груз, мест={place}, вес={weight}кг прошёл оформление авиа перевозки{to}.',
    2: 'Ваш груз, мест={place}, вес={weight}кг готов к загрузке в ВС для авиа перевозки в {to}.',
    3: 'Ваш груз, мест={place}, вес={weight}кг вылетел в {to}.'
}

TEXT_2_1 = 'Ожидайте следующее сообщение о ходе Вашей авиа перевозки...'
TEXT_2_2 = 'Ожидайте звонок оператора грузового терминала о готовности Вашего груза к выдаче.<br><br>Обращаем Ваше внимание, на то что грузовой терминал Вашего города при получении груза может взимать терминальный сбор в соответствии с тарифами грузового терминала.<br><br><br>Перевозка завершена!  '
SIGN = 'С уважением , ООО “ВТК” | Авиа грузоперевозки по России |'

SIGN_2 = '''http://vtcargo.ru | e-mail: moscow@vtcargo.ru | тел.: +7 (495) 972-95-62 |'''

HTML = """
    <html>
      <head></head>
        <body>
           <span style="color:#1f497d;font-family:'georgia' , serif;font-size:14pt">{text}</span>
           <br>
           <span style="color:#1f497d;font-family:'georgia' , serif;font-size:14pt">{text_2}</span>
           <br>
           <br>
           <br>
           <span style="color:#1f497d;font-family:'georgia' , serif;font-size:10pt">{SIGN}</span>
           <br>
           <span style="color:#1f497d;font-family:'georgia' , serif;font-size:10pt">{SIGN_2}</span>
           <br>
           <br>
           <img src="cid:image1" alt="Logo" style="width:288px;height:150px;"><br>          
        </body>
    </html>
"""
