from contracts.default import Default
from utils.encode import get_data_byte64

from decimal import Decimal
import requests


class Faucet(Default):
    def __init__(self, account, chain):
        super().__init__(account.private_key, chain.rpc, [], chain.contract_address, account.proxy)
        self.chain = chain

    def amounts(self, amount_in):
        amount_in = int(amount_in*1e18)
        data = get_data_byte64("0xf7729d43",
                               self.chain.address,
                               "e71bdfe1df69284f00ee185cf0d95d0c7680c0d4",
                               "bb8", hex(amount_in), "")

        resp = requests.post(self.rpc, json=[
            {
                "method": "eth_call",
                "params": [
                    {
                        "to": "0xb27308f9f90d607463bb33ea1bebb41c27ce5ab6",
                        "data": data
                    },
                    "latest",
                ],
                "id": 82,
                "jsonrpc": "2.0",
            },
        ])

        amount_out = int(int(resp.json()[0]["result"], 16) * 0.95)

        return amount_in, amount_out

    def swap_eth(self, amount):
        amount_in, amount_out = self.amounts(amount)

        data = get_data_byte64("0xae30f6ee",
                               hex(amount_in), hex(amount_out),
                               hex(161),
                               self.address,
                               self.address,
                               "", hex(224), "")


        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "maxFeePerGas": self.gwei_to_wei(0.01, 9),
            "maxPriorityFeePerGas": self.gwei_to_wei(0.01, 9),
            "value": hex(amount_in + 6000000000000),
            "to": self.contract_address
        }

        return self.send_transaction(tx, f"{self.chain.name} swap ({amount} ETH)")
