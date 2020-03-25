from client.bcosclient import (
    BcosClient,
    BcosError
)
import os
import ipfshttpclient
from eth_utils import to_checksum_address
from client.datatype_parser import DatatypeParser

def deploy():
    client = BcosClient()
    #从文件加载abi定义
    abi_file  ="contracts/SoftwareTransaction.abi"
    data_parser = DatatypeParser()
    data_parser.load_abi_file(abi_file)
    contract_abi = data_parser.contract_abi

    #部署合约
    with open("contracts/SoftwareTransaction.bin", 'r') as load_f:
        contract_bin = load_f.read()
        load_f.close()
    result = client.deploy(contract_bin)
    print("contract address:", result["contractAddress"])

if __name__=='__main__':
    deploy()
