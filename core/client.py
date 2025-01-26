from config import *
from utils.file_manager import append_to_txt
from utils.logs import logger

from decimal import Decimal
import time, random

from models.chains import *
from contracts.faucet import Faucet

class Client:
    def __init__(self, account):
        self.account = account

    def sleep(self, delay):
        s = random.randint(*delay)
        logger.info(f"ожидаем {s} сек..")
        time.sleep(s)

    def start(self):
        client_sepolia = Faucet(self.account, SEPOLIA)
        if client_sepolia.balance() >= min_amount:
            logger.info(f"{client_sepolia.acc_name} на счете больше {min_amount} ETH")
            return 0

        chains = [ARB, OP]
        amount = round(random.uniform(*amounts), 6)

        client_selected = None
        for chain in chains:
            client = Faucet(self.account, chain)
            if client.balance() > amount:
                logger.info(f"{client.acc_name} будем бриджить из {chain.name} {amount} ETH")
                client_selected = client
                break

        if client_selected:
            client = client_selected
            for i in range(5):
                if client.swap_eth(amount):
                    return 1
                else:
                    logger.info(f"{client.acc_name} ошибка при отправке транзакции, повторяем попытку {i+1}/5")
                    self.sleep([5, 10])
        else:
            logger.warning(f"{client.acc_name} недостаточно срадств на кошельке")

        return 2
