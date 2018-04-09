from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pydub import AudioSegment
import os
import json
import time
import boto3
import urllib
from time import gmtime, strftime


def downloadfile():
    mydict={}
    s3 = boto3.client('s3', aws_access_key_id = access_key_id, aws_secret_access_key = access_key)

    driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'],service_log_path=os.path.devnull)
    #driver = webdriver.Chrome()
    driver.get("https://www.newsinslowfrench.com")
    print("driver started")
    #try:
    element = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.LINK_TEXT,"Log in"))
    )
    # except:
        # print("Driver version error")
        # driver.save_screenshot('Error_version.png')

    login = driver.find_element_by_link_text('Log in')
    login.click()

    userElement = driver.find_element_by_name("username")
    userElement.send_keys(username)

    passwordElement = driver.find_element_by_name("password")
    passwordElement.send_keys(password)

    loginElement = driver.find_element_by_name("Login")
    loginElement.click()

    try:
        element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"track-flashcard"))
        )
    except:
        print("Login error")
	driver.save_screenshot('Error_Login.png')
    print("Logged in Succesful")
    element = driver.find_element_by_class_name('downloadTip')
    href = element.get_attribute('href')

    test = urllib.request.URLopener()
    test.retrieve(href,"old.mp3")

    sound = AudioSegment.from_mp3('old.mp3')
    length = len(sound)
    lenghtAfterCut = length/10
    cuttedfile = sound[:lenghtAfterCut]

    cuttedfile.export("cuttedmusicfile.mp3", format="mp3")
    s3client = boto3.client('s3',aws_access_key_id = access_key_id, aws_secret_access_key = access_key)
    s3client.upload_file("cuttedmusicfile.mp3", BUCKET_NAME,"newsfrench.mp3",ExtraArgs={'ACL': 'public-read'})
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print("Uploaded")

downloadfile()
                                                   
