### Как запустить бота:

#### Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/VitaliiLuki/cost_analysis_bot
```

#### Зарегистрировать бота у @BotFather и получить токен.

>Указать этот токен для переменной 'TELEGRAM_BOT_TOKEN'

#### Получить id чата, написав @userinfobot, он нужен для отправки сообщений о возникающих ошибках.

>Указать этот id для переменной 'TELEGRAM_CHAT_ID'


#### Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

#### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

#### Запустить код python-файла.
