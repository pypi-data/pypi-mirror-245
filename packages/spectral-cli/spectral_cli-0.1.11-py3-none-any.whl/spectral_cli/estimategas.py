from web3 import Web3
from spectral_cli import ABIS
alchemy_url = "https://arb-goerli.g.alchemy.com/v2/4OVA2qAgumYlGA7v1Y2E_-YPZCBgSvS5"  # testnet
w3 = Web3(Web3.HTTPProvider(alchemy_url))
print(w3.is_connected())
competition_address = "0x0163655101Dd34f5a7D8cC9c52Fa60AfcED1c929"  # dev
modeler_address = "0x5d538650b17097142122be8B09404d400B1A28Ca"  # dev
cli_wallet = "0xE49B7374c27B5d7b685833d7362AEacDC0811879"
competition_contract = w3.eth.contract(
    address=competition_address, abi=ABIS['Competition'])

# data = competition_contract.functions.signUpToCompetition("A").build_transaction({'chainId': 421613, 'nonce': w3.eth.get_transaction_count(
# "0x40442288Fe70822BF76949197EDB819434B964eD"), 'gasPrice': 800000000, 'gas': 1000000000})

# print(w3.eth.estimate_gas(data))
