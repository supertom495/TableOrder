# 点餐API

##### 对不同前端提供接口服务
1. 用户扫码点餐，固定一桌一码，下单后产品直接进入厨房
2. 用户扫码预点餐，一店一码，下单后生成二维码，在POS上扫二维码完成落单。
3.  Kiosk点餐
4. Mt扫描点餐
5. Uber eats （未完成）
6. 熊猫外卖 （未完成）


### sourcecode入口

##### api\

run_server.py : production entry  
 
flask_api.py: development entry  
 
models.py : database ORM  
 
database.py: connection pool  
 
router: controller  
 

### pyinstaller

目前32和64位程序不兼容，32位程序在vmware运行32位Windows下编译完成

编译方法：
1. 打开命令行  

  ```conda activate webapi-ngrok```
  
  ```  cd C:\Users\SUPERTOM\Documents\TableOrder\packing ```
  
 ```  pyinstaller --onefile --clean --name FlaskApi --icon=iconfinder_shrimp-prawn-seafood-animal-marine_3558097.ico ../api/run_server.py ``` 

 
 


https://blog.csdn.net/zhoury/article/details/86104105
https://pyinstaller.readthedocs.io/en/stable/usage.html

