from contracts.default import Default
from utils.encode import get_data_byte64

from decimal import Decimal
from web3 import Web3
from config import sepolia_rpc


class Sepolia(Default):
    def __init__(self, account):
        super().__init__(account.private_key, sepolia_rpc[0], [], "0x57beDd7eb4C3118669f4F33A3CAe4D4B554f24b7", account.proxy)

    def transfer(self, amount, recipient, fee_mult):
        gas_price = self.w3.eth.gas_price * 1.2
        fee = self.wei_to_gwei(gas_price * 21000)

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": "0x",
            "from": self.address,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "to": recipient,
            "gasPrice": hex(int(gas_price)),
            "value": hex(self.gwei_to_wei(amount - float(fee)*fee_mult)),
        }

        return self.send_transaction(tx, f"transfer to {recipient} ({amount} ETH)", False)

    def create(self):
        account = self.w3.eth.account.create()
        return account.address, account.key.hex()