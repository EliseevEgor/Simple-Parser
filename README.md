# Simple-Parser
## Description
Парсит информацию с сайта https://finance.yahoo.com/lookup.

Необходимо написать телеграм боту (https://t.me/SimpleParsingTelegramBot) команду /start.

Далее можно посмотреть, какие компании доступны на сайте, например, PD GME.

Бот выведет стандартную информацию о данной компании.
## Running
Запустить main.py

## Testing (ветка)
Сейчас есть два файла для тестирования 

server/tests/utest_request_utils.py и 

server/tests/utest_server_impl.py

Чтобы запустить тесты необходимо в папке проекта выполнить:

 python3 -m unittest server/tests/utest_request_utils.py

 python3 -m unittest server/tests/utest_server_impl.py
 
 Также PyCharm дает возможность запустить прям из IDE оба класса
 
 ## Load testing
 Решение находится в папке Docs
 
 Locust тест можно запустить и самому, необходимо запустить приложение (запустить main).
 
 Далее в терминале из папки проекта запустить locust -f server/tests/load_testing/locustfile.py --host=http://0.0.0.0:8000/
 
 После чего перейти по ссылке и выбрать нужное количество пользователей
 
 
