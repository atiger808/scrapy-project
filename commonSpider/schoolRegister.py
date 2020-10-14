
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as EC
from PIL import Image
from time import sleep
import time
import sys, re, os
import json

login_url= 'http://ywzs.jyt.henan.gov.cn/xxzs/BasicInfo/StuBasicInfo'
executable_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'
profile_directory = r'--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
options = Options()
options.add_argument('--no-sandbox')
options.add_argument(profile_directory)
# options.add_argument('--headless')
options.add_argument('blink-settings=imagesEnable=false')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=executable_path, options=options)
driver.get(login_url)

driver = webdriver.Chrome(executable_path=executable_path, chrome_options=options)




driver.get(postURL)