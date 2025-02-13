from concurrent.futures import ThreadPoolExecutor
import threading

from contracts.sepolia import Sepolia
from models.accounts import Account

from utils.file_manager import *
from utils.logs import logger

from config import *
import random
import time


ready_addr = []
def remove_addr():
    global ready_addr

    while True:
        time.sleep(5)

        for addr in ready_addr.copy():
            remove_line("address_recipient", addr)
            ready_addr.remove(addr)

def distribution(index, address_count, addr, proxies, private_sender):
    global ready_addr

    client_sender = Sepolia(Account(private_sender, random.choice(proxies)))
    addr = client_sender.w3.to_checksum_address(addr)
    
    amount = round(random.uniform(*amounts_distribution), 6)
    client_intermediate = client_sender

    for i in range(intermediate + 1):
        send_recipient = i == intermediate

        if not send_recipient:
            wallet_address, private_key = client_intermediate.create()
            logger.info(f"{index}/{address_count} создан {wallet_address} ({private_key}) {i + 1}/{intermediate}")
        else:
            wallet_address, private_key = addr, None
            logger.info(f"{index}/{address_count} отправляем на конечный адрес {addr}")

        for k in range(20):
            try:
                status = client_intermediate.transfer(amount, wallet_address, 1.8)

                if status:
                    if send_recipient:
                        logger.info(f"{index}/{address_count} отправили на конечный адрес {addr}")
                        ready_addr.append(addr)
                        break

                    client_intermediate = Sepolia(Account(private_key, random.choice(proxies)))
                    for j in range(10):
                        balance = client_intermediate.balance()
                        if balance != 0:
                            amount = float(balance)
                            break
                        else:
                            logger.info(f"{index}/{address_count} ожидаем ETH на {wallet_address}")
                            time.sleep(10)
                    break
                else:
                    client_intermediate.upd_w3_client(rpc=random.choice(sepolia_rpc), proxy=random.choice(proxies))
                    # logger.warning(f"{index}/{address_count} ошибка при отправке, повторяем попытку")

            except Exception as err:
                if "Cannot convert None of type <class 'NoneType'> to bytes" == str(err): continue
                logger.error(err)
                time.sleep(3)


def start_distribution():
    private_sender = input(f"Введите приватный ключ отправителя: ")
    proxies = txt_to_list("proxies")

    client_sender = Sepolia(Account(private_sender, random.choice(proxies)))

    logger.info(f"баланс отправителя {round(client_sender.balance(), 4)} ETH")

    address = txt_to_list("address_recipient")
    address_count = len(address)
    logger.info(f"рассылаем на {address_count} адресов")

    threading.Thread(target=remove_addr).start()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(distribution, i+1, address_count, addr, proxies, private_sender) for i, addr in enumerate(address)]

        for future in futures:
            result = future.result()
