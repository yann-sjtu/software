'''
  bcosliteclientpy is a python client for FISCO BCOS2.0 (https://github.com/FISCO-BCOS/FISCO-BCOS)
  bcosliteclientpy is free software: you can redistribute it and/or modify it under the terms of the MIT License as published by the Free Software Foundation
  This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
  Thanks for authors and contributors of eth-abi，eth-account，eth-hash，eth-keys，eth-typing，eth-utils，rlp, eth-rlp , hexbytes ...and relative projects
  @author: kentzhang
  @date: 2019-06
'''
from client.bcosclient import (
    BcosClient,
    BcosError
)
import os
import ipfshttpclient
from eth_utils import to_checksum_address
from client.datatype_parser import DatatypeParser

client = BcosClient()
ipfs_api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')


#从文件加载abi定义
abi_file  ="contracts/SoftwareTransaction.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi

#部署合约
print("\n\n>>> Deploying Contract, please wait...")
with open("contracts/SoftwareTransaction.bin", 'r') as load_f:
    contract_bin = load_f.read()
    load_f.close()
result = client.deploy(contract_bin)
#print("deploy",result)
print("contract address : ",result["contractAddress"])
contract_name =  os.path.splitext(os.path.basename(abi_file))[0]
memo = "tx:"+result["transactionHash"]
#把部署结果存入文件备查
from client.contractnote import ContractNote
ContractNote.save_address(contract_name, result["contractAddress"], int(result["blockNumber"], 16), memo)
to_address = result['contractAddress'] #use new deploy address

usage = '''
===== 欢迎使用Fisco软件交易系统 =====

使用方法:
  1.发布软件
  2.提供官方验证为软件背书
  3.键查询软件价格
  4.键购买软件
  
  其他键退出
'''
print(usage)
while True:
	choice = input("请输入数字：（1键发布软件，2键提供官方验证为软件背书，3键查询软件价格, 4键购买软件，其他键退出）")
	if choice == '1':
		file_name = input('''请输入待提交软件所在路径
路径：''')
		new_file = ipfs_api.add(file_name)
		print("软件提交到ipfs成功，哈希值为", new_file, type(new_file), new_file['Hash'])#
		software_name = input("请输入软件名：")
		software_price = input("请输入软件价格：")
		args = [software_name.encode('utf8'), int(software_price), new_file['Hash']]
		receipt = client.sendRawTransactionGetReceipt(to_address,contract_abi,"publish",args)
		#print("receipt:",receipt)

		#解析receipt里的log
		txhash = receipt['transactionHash']
		#获取对应的交易数据，解析出调用方法名和参数
		txresponse = client.getTransactionByHash(txhash)
		inputresult = data_parser.parse_transaction_input(txresponse['input'])
		#print("transaction input parse:",txhash)
		#print(inputresult, "\n")

		#解析该交易在receipt里输出的output,即交易调用的方法的return值
		outputresult  = data_parser.parse_receipt_output(inputresult['name'], receipt['output'])
		#print("receipt output :",outputresult)
		print("软件已发布到 Fisco, 交易哈希为",txhash)
	elif choice == '2':
		name = input("请输入软件名：")
		receipt = client.sendRawTransactionGetReceipt(to_address,contract_abi,"varify",[name.encode('utf8'), 8])
		if receipt['status'] == '0x0':
			print("软件{}验证成功，已开放购买".format(name))
		else:
			print("软件{}授权失败".format(name))
	elif choice == '3':
		name = input("请输入您想购买的软件：")
		receipt = client.sendRawTransactionGetReceipt(to_address,contract_abi,"getPrice",[name.encode('utf8')])
		if receipt['status'] != '0x0':
			print("软件{}不存在".format(name))
		else:
			res = client.call(to_address, contract_abi, "getPrice",[name.encode('utf8')])
			print("软件价格为：", res[0])
	elif choice == '4':
		name = input("请输入您想购买的软件：")
		receipt = client.sendRawTransactionGetReceipt(to_address, contract_abi, "buySoftware", [name.encode('utf8')])
		if receipt['status'] != '0x0':
			print("软件购买失败")
		else:
			res = client.call(to_address, contract_abi, "buySoftware",[name.encode('utf8')])
			print("所购软件在ipfs的哈希值为", res[0])
			print("正在从ipfs拉取源代码...")
			file_hash = res[0]
			res = ipfs_api.get(file_hash)
			print("源代码拉取成功！")
	else:
		choice2 = input("确定退出吗？ y/n")
		if choice2 != 'y' and choice2 != 'Y':
			continue
		client.finish()
		break

