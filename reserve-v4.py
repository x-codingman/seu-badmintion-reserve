"""
@Description :   
@Author      :   x-codingman 
@Time        :   2021/10/31 10:13:13
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import random
import checkcode
import threading
import datetime


users=[
    [
        {
          "uid":"",
          "pwd":"",
          "target_time":"18:00-19:00"
      },
      {
          "uid":"",
          "pwd":"",
          "target_time":"19:00-20:00"
      },
      {
          "uid":"",
          "pwd":"",
          "target_time":"20:00-21:00"
      }
    ],
    [
      {
          "uid":"",
          "pwd":"",
          "target_time":"18:00-19:00"
      },
      {
          "uid":"",
          "pwd":"",
          "target_time":"19:00-20:00"
      },
      {
          "uid":"213173779",
          "pwd":"",
          "target_time":"20:00-21:00"
      }
    ],
    [
        {
          "uid":"",
          "pwd":"",
          "target_time":"18:00-19:00"
      },
      {
          "uid":"",
          "pwd":"",
          "target_time":"19:00-20:00"
      },
      {
          "uid":"",
          "pwd":"",
          "target_time":"20:00-21:00"
      }
    ]
]

users_extra=[
    
        {
          "uid":"",
          "pwd":"",
          "target_time":"20:00-21:00"
      },
      {
          "uid":"",
          "pwd":"",
          "target_time":"19:00-20:00"
      }
    
]


def wait_element_click(driver,wait,path):
    wait.until(EC.element_to_be_clickable((By.XPATH, path)))
    driver.find_element_by_xpath(path).click()



def request_check_code(r):
    img_name=str(random.randint(0,1000))
    with open(img_name+'.png', 'wb') as file:
        file.write(r.content)
    return checkcode.get_check_code(img_name+'.png')


def reserve(uid,pwd,target_time,name):

        date_time=(datetime.date.today()+datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        
        order_time=date_time+" "+target_time
        print(order_time+" "+name)

        #chromedriver_autoinstaller.install() 
        chrome_options = webdriver.ChromeOptions()
        # 指定chrome启动类型为headless 并且禁用gpu
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome("/usr/local/bin/chromedriver",options=chrome_options)
        driver.get("http://yuyue.seu.edu.cn/eduplus/order/initOrderIndex.do?sclId=1")
        driver.find_element_by_xpath("//div[@class='auth_tab_content']/div[1]/form/p[1]/input").send_keys(uid)
        driver.find_element_by_xpath("//div[@class='auth_tab_content']/div[1]/form/p[2]/input").send_keys(pwd)
        driver.find_element_by_xpath("//div[@class='auth_tab_content']/div[1]/form/p[5]/button").click()
        wait = WebDriverWait(driver,2,0.5)
        
        payload={"itemId":"10","dayInfo":"2021-04-06","time":"12:30-13:30"}
        url="http://yuyue.seu.edu.cn/eduplus/order/order/judgeOrder.do?sclId=1"
        driver_cookies = driver.get_cookies()
        c = {c['name']:c['value'] for c in driver_cookies}
        myheaders = {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Encoding": "br, gzip, deflate",
            "Accept-Language": "zh-cn",
            "Host": "yuyue.seu.edu.cn",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        }
        #r=requests.post(url,headers=myheaders,params=payload,cookies=c)
        image_url="http://yuyue.seu.edu.cn/eduplus/control/validateimage"
        r=requests.get(image_url,headers=myheaders,cookies=c)
       
        vc=request_check_code(r)
        while(vc==""):
            while(r.status_code!=200):
                r=requests.get(image_url,headers=myheaders,cookies=c)
            print("get image ------")
            vc=request_check_code(r)
        print(vc)
        url_judge="http://yuyue.seu.edu.cn/eduplus/order/order/order/judgeUseUser.do?sclId=1"
        payload_judge={"ids":"","useTime":"2021-04-06 11:30-12:30","itemId":"10","allowHalf":"2","validateCode":vc}
        url_order="http://yuyue.seu.edu.cn/eduplus/order/order/order/insertOredr.do?sclId=1"
        payload_order={"orderVO.useTime":order_time,"orderVO.itemId":"10",
        "orderVO.useMode":"2","orderVO.phone":"13918888888","orderVO.remark":"","validateCode":vc}
       
        
        r=requests.post(url_order,params=payload_order,headers=myheaders,cookies=c)
        i=0
        while((r.text).find("cess")<0 and i<1500 and (r.text).find("Error")<0):
            r=requests.post(url_order,params=payload_order,headers=myheaders,cookies=c)
            i=i+1
        #print(r.text)
        if(i==1500):
            print(name+"failed"+" i="+str(i))
        else:
            print(name+"success"+" i="+str(i))

def user_select():
    week_day=datetime.datetime.today().weekday()
    if week_day <2 or week_day==6:
        return users[0]
    elif week_day<4:
        return users[1]
    else:
        return users[2]
     


if __name__ == "__main__":
 
    user=user_select()
    for u in user:
        thread_reserve=threading.Thread(target=reserve,args=(u["uid"],u["pwd"],u["target_time"],u["uid"]))
        thread_reserve.start()
    week_day=datetime.datetime.today().weekday()
    if week_day >=2 and week_day<5:
        for u in users_extra:
            thread_reserve=threading.Thread(target=reserve,args=(u["uid"],u["pwd"],u["target_time"],u["uid"]))
            thread_reserve.start()
   
 
   
    

   
