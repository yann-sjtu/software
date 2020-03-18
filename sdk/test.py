from client.bcosclient import (
    BcosClient,
    BcosError
)
import os
import ipfshttpclient
from eth_utils import to_checksum_address
from client.datatype_parser import DatatypeParser

client = BcosClient()


#从文件加载abi定义
abi_file  ="contracts/SoftwareTransaction.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi

contract_addr = "0x290ecb451d85eb7ab8e2b0ec941bde7093f61b06"
print(contract_abi)
res = client.call(contract_addr, contract_abi, "buySoftware",["apache".encode('utf8')])