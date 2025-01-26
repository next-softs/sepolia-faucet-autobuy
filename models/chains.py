
class Chain:
    def __init__(self, name, rpc, address="", contract_address=""):
        self.name = name
        self.rpc = rpc
        self.address = address
        self.contract_address = contract_address

ARB = Chain("arb", "https://arb1.arbitrum.io/rpc", "82af49447d8a07e3bd95bd0d56f35241523fbab1", "0xfcA99F4B5186D4bfBDbd2C542dcA2ecA4906BA45")
OP = Chain("op", "https://rpc.ankr.com/optimism", "4200000000000000000000000000000000000006", "0x8352C746839699B1fc631fddc0C3a00d4AC71A17")
SEPOLIA = Chain("sepolia", "https://sepolia.drpc.org", "", "0x57beDd7eb4C3118669f4F33A3CAe4D4B554f24b7")