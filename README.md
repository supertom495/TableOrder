pyinstaller --log-level=DEBUG --debug=all dataApi.py

--add-data api-ms-win-crt-runtime-l1-1-0

https://blog.csdn.net/zhoury/article/details/86104105
https://pyinstaller.readthedocs.io/en/stable/usage.html


debug logger is settle up

# go to src folder run than build
pyinstaller --clean --windowed -D --add-data api-ms-win-crt-runtime-l1-1-0.dll;. src/TableOrder-wxUI.py

# this is the sample for debug software
pyinstaller --clean -D --add-data api-ms-win-crt-runtime-l1-1-0.dll;. --log-level=DEBUG --debug=all src/TableOrder-wxUI.py

3.5 build
Fix the bug that stock can not be match any printer