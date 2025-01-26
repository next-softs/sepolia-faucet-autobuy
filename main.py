import threading, time, random

from models.accounts import Accounts

from utils.first_message import first_message
from core.client import Client
from utils.logs import logger
from config import *

from contracts.faucet import Faucet
from models.chains import *


def start_bridge(accounts):
    clients = [Client(account) for account in accounts]

    count_clients = len(clients)
    clients_error = []

    for i, client in enumerate(clients):
        status = client.start()
        logger.info(f"обработано {i}/{count_clients} кошельков")


        if status == 2:
            clients_error.append(client)
        elif status == 1:
            client.sleep(delay_actions)


    for client in clients_error:
        print(client.account.private_key)

def check_balances(accounts):
    for account in accounts:
        client = Faucet(account, SEPOLIA)
        logger.info(f"{client.address} {round(client.balance(), 4)} ETH")


def main():
    accounts_manager = Accounts()
    accounts_manager.loads_accs()
    accounts = accounts_manager.accounts

    action = input("> 1. Запустить бридж ETH\n"
                   "> 2. Балансы ETH Sepolia\n"
                   ">> ")
    print("-"*50+"\n")


    if action == "1":
        start_bridge(accounts)
    elif action == "2":
        check_balances(accounts)
    else:
        logger.warning(f"Выбран вариант, которого нет!")

if __name__ == '__main__':
    first_message()
    main()

