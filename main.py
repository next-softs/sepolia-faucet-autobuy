from concurrent.futures import ThreadPoolExecutor
import threading, time, random

from models.accounts import Accounts, Account
from utils.first_message import first_message
from core.client import Client
from utils.logs import logger
from config import *

from contracts.sepolia import Sepolia
from contracts.faucet import Faucet
from models.chains import *

from core.resender import start_distribution
import logging


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


def check_balances(accounts):
    def check_balance(acc):
        client = Faucet(acc, SEPOLIA)
        logger.info(f"{client.address} {round(client.balance(), 4)} ETH")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_balance, acc) for acc in accounts]

        for future in futures:
            result = future.result()

def main():
    accounts_manager = Accounts()
    accounts_manager.loads_accs()
    accounts = accounts_manager.accounts

    action = input("> 1. Запустить бридж ETH\n"
                   "> 2. Рассылка ETH\n"
                   "> 3. Балансы ETH Sepolia\n"
                   ">> ")

    print("-"*50+"\n")


    if action == "1":
        start_bridge(accounts)
    elif action == "2":
        logging.getLogger("web3").setLevel(logging.CRITICAL)
        logging.getLogger("urllib3").setLevel(logging.CRITICAL)

        start_distribution()
    elif action == "3":
        check_balances(accounts)
    else:
        logger.warning(f"Выбран вариант, которого нет!")

if __name__ == '__main__':
    first_message()
    main()

