pyinstaller --log-level=DEBUG --debug=all dataApi.py

--add-data api-ms-win-crt-runtime-l1-1-0

https://blog.csdn.net/zhoury/article/details/86104105
https://pyinstaller.readthedocs.io/en/stable/usage.html


# go to src folder run than build
pyinstaller -D --add-data api-ms-win-crt-runtime-l1-1-0.dll;. TableOrder.py



# this is the sample for debug software
pyinstaller -D --add-data api-ms-win-crt-runtime-l1-1-0.dll;. --log-level=DEBUG --debug=all uploadCustomer.py