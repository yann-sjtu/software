
import ipfshttpclient
import os

usage = '''
Usage:
    1.Upload file
    2.View file
    3.Download file
    4.All file keys
    5.Quit
'''

ipfs_api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
# res = ipfs_api.add("requirements.txt")
# print("res:", res)
res = ipfs_api.get("QmcSLuGyFN6gCTpwUoEz1LnEJDo4CoeW5kwnHPWuYqTbd8")
print(res)


# if __name__ == "__main1__":
#     try:
#         ipfs_api = ipfshttpclient.connect('127.0.0.1', 5001)
#         print(usage)
#         while True:
#             choice = input("input a number: ")
#             if choice == '1':
#                 file_name = input("Enter file name with full path: ")
#                 new_file = ipfs_api.add(file_name)
#                 print("file hash:", new_file['Hash'])

#             elif choice == '2':
#                 key = input("Please enter file hash : ")
#                 res = ipfs_api.cat(key)
#                 print("The file content is:", res)
            
#             elif choice == '3':
#                 key = input("Please enter file hash : ")
#                 ipfs_api.get(key)
#                 print("File with hash " + str(key) + " is downloaded to current directory.")
#             elif choice == '4':
#                 res = ipfs_api.pin.ls(type='all')
#                 print(res)
#             else:
#                 print("bye~")
#                 break

#     except ipfshttpclient.exceptions.ConnectionError as ce:
#         print(str(ce))
