# === SEPOLIA FAUCET 1.1 ===

**SEPOLIA FAUCET** — это бот для автоматической покупки и рассылки тестовых ETH SEPOLIA.    

`Текущий курс 0.0003 ETH (1 USDT) = 4.3 ETH SEPOLIA`

## Функционал бота:  
- [Бридж](https://testnetbridge.com/sepolia) ETH из OP или ARB переводим в SEPOLIA. Сеть из которой берем ETH определяется автоматически т.е. если ETH в OP, то тестовые токены будут куплены из OP
- Вывод балансов ETH SEPOLIA
- Рассылка ETH на другие кошельки через промежуточные

## Параметры:  
- Случайные задержки между действиями
- Случайные объёмы ETH
- Кол-во потоков

## Установка:  
- [Устанавливаете](https://www.python.org/downloads/) `python 3.11.9`  
- Запускаете файл `setup.bat`

## Запуск:  
- В файле `config.py` настраиваем бота.
- В файле `data>private_keys.txt` указываем приватные ключи.
- В файле `data>address_recipient.txt` указываем адреса для получения токенов при рассылке.
- В файле `data>proxy.txt` указываете прокси.  
- Запускать бота файлом `start.bat`  

[![Telegram](https://img.shields.io/badge/-Telegram-090909?style=for-the-badge&logo=telegram&logoColor=27A0D9&color=02223b)](https://t.me/next_softs)
