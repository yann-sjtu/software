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
from io import BytesIO
from PIL import Image
import os
import ipfshttpclient
from eth_utils import to_checksum_address
from client.datatype_parser import DatatypeParser

client = BcosClient()
ipfs_api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
#info = client.init()
#print(client.getinfo())


#从文件加载abi定义
abi_file  ="contracts/Chaoyang.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi

#部署合约
print("\n\n>>> Deploying Contract, please wait...")
with open("contracts/Chaoyang.bin", 'r') as load_f:
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
===== 欢迎使用朝阳大妈说 =====

使用方法:
  1.提交举报信息
  2.查看举报信息
  
  回车键退出
'''
print(usage)
count = -1
while True:
	choice = input("请输入数字：（1键提交举报，2键查看举报，其他键退出）")
	if choice == '1':
		file_name = input('''请输入待提交文件所在路径
====================
测试图片文件：
./img/img1.jpeg
./img/img2.jpeg
./img/img3.jpg
====================
路径：''')
		new_file = ipfs_api.add(file_name)
		print("文件提交到ipfs成功，哈希值为", new_file['Hash'])
		args = ['行人闯红灯', 0, '北京市朝阳区','15202183323',new_file['Hash'], 40, 116]
		receipt = client.sendRawTransactionGetReceipt(to_address,contract_abi,"registerComplain",args)
		print("receipt:",receipt)

		#解析receipt里的log
		txhash = receipt['transactionHash']
		#获取对应的交易数据，解析出调用方法名和参数
		txresponse = client.getTransactionByHash(txhash)
		inputresult = data_parser.parse_transaction_input(txresponse['input'])
		#print("transaction input parse:",txhash)
		print("\n注：为简化代码，测试用举报信息为自动生成")
		print(inputresult, "\n")
		print("事件信息：",inputresult['args'][0])
		print("处理进度：（0未处理，1已处理）",inputresult['args'][1])
		print("地址：",inputresult['args'][2])
		print("举报人手机号：",inputresult['args'][3])
		print("举报文件哈希值：",inputresult['args'][4])
		print("GPS 定位，东经{}°，北纬{}°".format(inputresult['args'][5],inputresult['args'][6]))

		#解析该交易在receipt里输出的output,即交易调用的方法的return值
		outputresult  = data_parser.parse_receipt_output(inputresult['name'], receipt['output'])
		#print("receipt output :",outputresult)
		print("举报信息已提交到 Fisco, 交易哈希为" ,txhash,"举报信息序号为", outputresult[0])
		count+=1
	elif choice == '2':
		num = input("已有{}条举报信息，请输入查询序号：(0~{})".format(count+1, count))
		try:
			num=int(num)
		except:
			print("非法序号！")
			continue
		if num > count or num < 0:
			print("序号不在范围内！")
			continue
		res = client.call(to_address, contract_abi, "viewComplain",[num])
		print("举报信息为:", res)
		print("正在从ipfs拉取多媒体文件...")
		file_hash = res[6]
		res = ipfs_api.cat(file_hash)
		try:
			bytes_stream = BytesIO(res)
			img = Image.open(bytes_stream)
			img.show()
		except:
			pass
		choice2 = input("是否保存文件到本地？ y/n")
		if choice2 == 'y' or choice2 == 'Y':
			ipfs_api.get(file_hash)
			print("文件已保存到当前文件夹，文件名为：", file_hash)
	else:
		choice2 = input("确定退出吗？ y/n")
		if choice2 != 'y' and choice2 != 'Y':
			continue
		client.finish()
		break

