
import sys
import json
import base64
from tinydb import TinyDB, Query, where
# code by nguyentri729
# 17/04/2020
# auto ads facebook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
import string
import re
import time
import requests
import pathlib
import os
import ctypes
class autofb:
    def __init__(self, proxyIP='', hideWindow=False, fakeURL='', keyActive='', postion='left', numberThread = 1, totalThread = 1):
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        
        option.add_argument("--disable-background-mode")
        prefs = {"profile.managed_default_content_settings.images": 2}
        option.add_experimental_option("prefs", prefs)
        if postion == 'left':
            option.add_argument("window-size=960,950")
            option.add_argument("--window-position=0,0")
            option.add_argument("--auto-open-devtools-for-tabs")
        else:
            # user32 = ctypes.windll.user32
            # user32.SetProcessDPIAware()

            # option.add_argument("window-size=150,300")
            # maxHeight = round(user32.GetSystemMetrics(1) / 300)
            # maxWidth = round(user32.GetSystemMetrics(1) / 150)
            # heightY = int(numberThread) * 300
            # widthX = 0
            # if maxHeight >= user32.GetSystemMetrics(1):
            #     widthX = int(numberThread) * 150
            # option.add_argument("--window-position="+str(int(numberThread) * widthX)+","+str(heightY)+"")
            # print('goc ne')
            option.add_argument("window-size=960,950")
            option.add_argument("--window-position=960,0")
        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        self.fakeURL = fakeURL
        self.keyActive = keyActive
        if hideWindow:
            option.add_argument("--headless")
        capabilities = webdriver.DesiredCapabilities.CHROME
        if proxyIP != '':
            prox = Proxy()
            prox.proxy_type = ProxyType.MANUAL
            prox.ssl_proxy = proxyIP
            prox.add_to_capabilities(capabilities)
        self.driver = webdriver.Chrome(
            options=option, executable_path=r".\\chromedriver.exe", desired_capabilities=capabilities)

    def testChangeIP(self):
        self.driver.get('https://api.myip.com/')
    
    def checkKey(self):
        return True
        try:
            check = requests.get(
                'http://199.34.16.50/checkKeys.php?key='+self.keyActive+'')
            if check.text == 'success':
                return True
            else:
                return False
        except:
            return False
        return False

    def login(self, data):
        self.driver.get('https://www.facebook.com/')
        if self.checkKey() == False:
            self.driver.execute_script(
                """document.getElementsByTagName('body')[0].innerHTML = '<div style="text-align: center; padding: 10%; font-size: 25px; color: red"><h1 style="font-size: 50px; color: red">KEY SAI HOẶC HẾT HẠN</h1><br><a href="https://www.facebook.com/Duc.EUMedia">Liên hệ: Nguyễn Thái Đức</a></div>'""")
            time.sleep(1000)
            return False
        
        if data['loginType'] == 'cookie':
            cookies = data['cookie'].split(';')
            for cookie in cookies:
                try:
                    splitCookie = cookie.split('=')
                    self.driver.add_cookie({
                        'name': splitCookie[0].strip(),
                        'value': splitCookie[1].strip()
                    })
                except err:
                    print(err)
            self.driver.get('https://www.facebook.com/')
            self.driver.execute_script("""
            document.getElementsByClassName('noCount')[0].innerHTML=`<button id="emiwwVN" onclick='intl_set_locale(null, "www_card_selector", "vi_VN"); return false;'>Em iww Viet Nam</button>`;document.getElementById('emiwwVN').click()
            """)
            return True
        if data['loginType'] == 'account':
            emailInput = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "email")))
            passwordInput = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "pass")))
            emailInput.send_keys(data['username'])
            time.sleep(0.5)
            passwordInput.send_keys(data['password'])

            time.sleep(0.2)

            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            # check 2fa
            try:
                codeInput = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "approvals_code")))
                submitButton = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "checkpointSubmitButton")))
                r = requests.get(
                    'https://jickmeaz.000webhostapp.com/getCode.php?secrect=' + data['secret'] + '')

                if r.status_code == 200:
                    codeInput.send_keys(r.text)
                    submitButton.click()
                else:
                    return False
            except NameError:
                print('loi ne' + NameError)
            for x in range(6):
                try:
                    submitButton = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.ID, "checkpointSubmitButton")))
                    submitButton.click()
                except:
                    break
            self.driver.execute_script("""
            document.getElementsByClassName('noCount')[1].innerHTML=`<button id="emiwwVN" onclick='intl_set_locale(null, "www_card_selector", "vi_VN"); return false;'>Em iww Viet Nam</button>`;document.getElementById('emiwwVN').click()
            """)
        if data['loginType'] == 'all':
            data['loginType'] = 'cookie'
            if self.login(data):
                pass
            else:
                data['loginType'] = 'account'
                self.login(data)
        return True

    def checkLogin(self):
        try:
            self.driver.get('https://www.facebook.com/profile.php')
            # divdata-click="profile_icon"
            userNav = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-click='profile_icon']")))
            return True
        except:
            return False

    def getInfo(self):
        try:
            
            self.driver.get('https://www.facebook.com')
            type_user = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[@data-type='type_user']")))
            
            
            name = type_user.text
            uid = type_user.get_attribute('data-nav-item-id')
            
            return {
                'uid': uid,
                'name': name
            }
            
        except:
            self.quit()
            return False

    def getCookie(self):
        cookies = self.driver.get_cookies()
        cookieStr = ''
        for cookie in cookies:
            cookieStr += cookie['name'] + '=' + cookie['value'] + ";"
        return cookieStr

    def addCredit(self, creditCard):
        self.driver.get('https://www.facebook.com/ads/manager/account_settings/account_billing/')
        try:
            # wait button show
            addCreditButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='cm_add_pm_button']")))
            addCreditButton.click() 
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@data-testid='credit_card_number']")))



            webdriver.ActionChains(self.driver).send_keys(Keys.TAB + Keys.TAB + Keys.TAB).perform()
            cardExperied = creditCard['cardExperied'].split('/')
            webdriver.ActionChains(self.driver).send_keys(creditCard['cardNumber'] + Keys.TAB).perform()
            webdriver.ActionChains(self.driver).send_keys(cardExperied[0]).perform()
            webdriver.ActionChains(self.driver).send_keys(cardExperied[1] + Keys.TAB).perform()
            webdriver.ActionChains(self.driver).send_keys(creditCard['ccv'] + Keys.TAB).perform()
            self.driver.execute_script("document.getElementsByClassName('uiOverlayFooterGrid')[0].getElementsByTagName('button')[0].click()")
        except:
            self.driver.execute_script("alert('loi !')")
            return False

        try:
            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, "//input[@data-testid='credit_card_month']")))
        except err:
            return False
            
        time.sleep(2)
        return True

    def addAdsAccount(self, moneyTypeIndex='16', timeIndex='61', countryIndex='13'):
        try:
            # add ads
            self.driver.get(
                'https://www.facebook.com/ads/manager/account_settings/information/')
            changeMoney = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                (By.XPATH, "//a[contains(text(),'Thay đổi đơn vị tiền tệ')]")))
            changeMoney.click()
            time.sleep(3)
            enterButton = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='currency']")))

            webdriver.ActionChains(self.driver).send_keys(
                Keys.TAB + Keys.ENTER).perform()
            time.sleep(2)
            self.driver.execute_script(
                "document.getElementsByClassName('_54nh')["+str(moneyTypeIndex)+"].click(); ")
            time.sleep(2)
            webdriver.ActionChains(self.driver).send_keys(
                Keys.TAB + Keys.ENTER).perform()
            time.sleep(1.5)
            self.driver.execute_script(
                "document.getElementsByClassName('_54nh')["+str(timeIndex)+"].click()")
            time.sleep(2)
            webdriver.ActionChains(self.driver).send_keys(
                Keys.TAB + Keys.TAB).perform()
            time.sleep(2)
            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(2)
            afterClick = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='jazoest']")))
            webdriver.ActionChains(self.driver).send_keys(
                Keys.TAB + Keys.TAB + Keys.ENTER).perform()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_50f7")))
        except:
            time.sleep(2)

        time.sleep(2)
        try:
            # enter new ads
            self.driver.get(
                'https://www.facebook.com/ads/manager/account_settings/information/')

            businessName = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@data-testid='business_name']")))
            businessName.send_keys(self.randomString(8))

            address_street1 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@data-testid='address_street1']")))
            address_street1.send_keys(self.randomString(8))

            address_city = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@data-testid='address_city']")))
            address_city.send_keys(self.randomString(8))

            address_state = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@data-testid='address_state']")))
            address_state.send_keys(self.randomString(8))

            self.driver.execute_script(
                "document.getElementsByClassName('_1f')[0].click();setTimeout(function(){console.log(document.getElementsByClassName('_3leq'));document.getElementsByClassName('_3leq')["+str(countryIndex)+"].click()},2000)")

            time.sleep(3)

            cm_settings_page_save_button = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-testid='cm_settings_page_save_button']")))
            cm_settings_page_save_button.click()

            time.sleep(5)
        except:
            time.sleep(5)
        try:
            # buoc tiep theo ne
            self.driver.get(
                'https://www.facebook.com/ads/manager/account_settings/account_billing/')
            # wait button show
            addCreditButton = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-testid='cm_add_pm_button']")))
            addCreditButton.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "new_direct_debit_v2_title")))
            self.driver.execute_script(
                "document.getElementById('new_direct_debit_v2_title').click();setTimeout(function(){document.getElementsByClassName('layerConfirm')[0].click()},3000)")

            # get data from fake IT site
            fakeData = self.fakeIT()
            account_holder_name = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='account_holder_name']")))
            account_holder_name.send_keys(fakeData['name'])

            bankAccountNumber = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='bankAccountNumber']")))
            bankAccountNumber.send_keys(fakeData['iban'])
            routing_number = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='routing_number']")))
            routing_number.send_keys(fakeData['bic'])

            # addCreditButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@value='1']")))
            # addCreditButton.click()
            street = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='street']")))
            street.send_keys(fakeData['address'])

            city = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='city']")))
            city.send_keys(fakeData['city'])

            zipCode = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='zip']")))
            zipCode.send_keys(fakeData['zipcode'])

            approval = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='approval']")))
            approval.send_keys(Keys.SPACE)
            addButton = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "AdsPaymentsDirectDebitButton")))
            addButton.click()
            time.sleep(5)
        except:
            pass
        
    def createPage(self):
        self.driver.get(
            'https://www.facebook.com/pages/create/?ref_type=pages_you_admin')
        startButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@data-testid='NON_BUSINESS_SUPERCATEGORYSelectButton']")))
        startButton.click()

        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB + self.randomString()).perform()
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB + "Cộng đồng").perform()
        time.sleep(1)
        webdriver.ActionChains(self.driver).send_keys(
            Keys.ENTER + Keys.TAB + Keys.TAB + Keys.ENTER).perform()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@name='admin_to_do_profile_pic']")))
        contentArea = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "content")))
        contentArea.click()
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB + Keys.ENTER).perform()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@name='admin_to_do_cover_photo']")))
        contentArea = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "content")))
        contentArea.click()
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB + Keys.ENTER).perform()
        time.sleep(2)

    def adsActive(self):

        self.driver.refresh()
        entity_sidebar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "entity_sidebar")))
        self.driver.execute_script(
            "document.getElementsByTagName('button')[1].click()")
        time.sleep(2)
        # check show poupup
        checkPop = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "uiOverlayFooter")))
        time.sleep(2)
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB + Keys.TAB + Keys.ENTER).perform()
        time.sleep(2)
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB + Keys.TAB + Keys.TAB + Keys.ENTER).perform()
        time.sleep(5)

    # gender (0: Tất cả, 1: Nam, 2: Nữ)
    def adsCreatePost(self, postContent='abcdef', gender=0, startAge=14, endAge=45, location='Việt Nam', dayAds=1, finance=600000, creditCard='4056400172321306|04|23|222'):

        # self.driver.get('https://www.facebook.com/Gmmdhmbj-112937363720458/?modal=admin_todo_tour')

        self.driver.refresh()
        createPostArea = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@name='xhpc_message']")))
        createPostArea.click()
        time.sleep(2)
        qcButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@style='max-width: 500px; letter-spacing: normal; color: rgb(68, 73, 80); font-size: 12px; font-weight: bold; font-family: Arial, sans-serif; line-height: 22px; text-align: center; background-color: rgb(245, 246, 247); border-color: rgb(218, 221, 225); height: 24px; padding-left: 7px; padding-right: 7px; border-radius: 2px;']")))
        time.sleep(1)
        webdriver.ActionChains(self.driver).send_keys(
            self.randomString()).perform()
        qcButton.click()
        time.sleep(3)
        changeButton = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Chỉnh sửa')]")))
        changeButton.click()
        # gender
        genderButton = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "GENDER")))
        # excute script here
        self.driver.execute_script('const genderIndex='+str(gender)+';const startAgeIndex='+str(startAge)+';const endAgeIndex='+str(
            endAge)+';const genderDiv=document.getElementById("GENDER");const buttonGender=genderDiv.getElementsByTagName("button");buttonGender[genderIndex].click();const ageDev=document.getElementById("AGE");const startAge=ageDev.getElementsByTagName("button")[0];const endAge=ageDev.getElementsByTagName("button")[1];startAge.click();setTimeout(()=>{document.getElementsByClassName("uiContextualLayerBelowLeft")[0].getElementsByTagName("li")[startAgeIndex-13].getElementsByTagName("div")[1].click();endAge.click()},2000);setTimeout(()=>{document.getElementsByClassName("uiContextualLayerBelowLeft")[0].getElementsByTagName("li")[endAgeIndex-13].getElementsByTagName("div")[1].click()},4000);')
        time.sleep(4)
        locationInput = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@data-testid='ads-targeting-location-typeahead']")))
        locationInput.click()
        time.sleep(3)
        webdriver.ActionChains(self.driver).send_keys(location).perform()
        time.sleep(2)
        webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(2)
        confirmButton = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@action='confirm']")))
        confirmButton.click()
        time.sleep(3)

        duration_days_editor = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-testid='duration_days_editor']")))
        duration_days_editor.send_keys(Keys.BACK_SPACE + str(dayAds))
        locationInput = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//label[@style='background: rgb(255, 255, 255); border-color: rgb(218, 221, 225); color: rgb(28, 30, 33);']")))

        locationInput.click()
        time.sleep(1)
        for index in range(0, 20):
            webdriver.ActionChains(self.driver).send_keys(
                Keys.BACK_SPACE).perform()
        time.sleep(1)
        webdriver.ActionChains(self.driver).send_keys(str(finance)).perform()
        time.sleep(2)
        buttonPrimary = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='primary_button']")))
        buttonPrimary.click()

        try:
            credit_card_number = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='creditCardNumber']")))
            # split credit credit
            credit = creditCard.split('|')
            time.sleep(2)
            webdriver.ActionChains(self.driver).send_keys(
                Keys.TAB + Keys.TAB + Keys.TAB + credit[0]).perform()
            webdriver.ActionChains(self.driver).send_keys(
                Keys.TAB + credit[1]).perform()
            webdriver.ActionChains(self.driver).send_keys(credit[2]).perform()
            webdriver.ActionChains(self.driver).send_keys(
                Keys.TAB + credit[3]).perform()
            for index in range(1, 6):
                webdriver.ActionChains(
                    self.driver).send_keys(Keys.TAB).perform()
            time.sleep(1)
            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        except:
            pass

        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(
            (By.XPATH, "//input[@name='creditCardNumber']")))

        # post button click

        self.driver.execute_script(
            'const buttonList=document.getElementById("feedx_sprouts_container").getElementsByTagName("button");buttonList[buttonList.length-1].click()')
        time.sleep(6)

    def addMainCloneAds(self, name):
        
        self.driver.get(
            'https://www.facebook.com/ads/manager/account_settings/information/')
        addPeople = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@style='letter-spacing: normal; color: rgb(255, 255, 255); font-size: 12px; font-weight: bold; font-family: Arial, sans-serif; line-height: 26px; text-align: center; background-color: rgb(24, 119, 242); border-color: rgb(24, 119, 242); height: 28px; padding-left: 11px; padding-right: 11px; border-radius: 2px;']")))
        addPeople.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@name='search_query']")))
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB + name).perform()
        time.sleep(2)
        webdriver.ActionChains(self.driver).send_keys(
            Keys.ARROW_DOWN + Keys.ENTER + Keys.TAB + Keys.ENTER + Keys.ARROW_UP + Keys.ENTER).perform()
        time.sleep(1)
        webdriver.ActionChains(self.driver).send_keys(
            Keys.TAB + Keys.TAB + Keys.TAB + Keys.ENTER).perform()
        time.sleep(5)
        idCampRegex = r"https://www\.facebook\.com/ads/manager/account_settings/information/\?act=(.*?)&"
        idCamp = re.findall(idCampRegex, self.driver.current_url)
        return idCamp[0]

    def addFriends(self, uid):
        self.driver.get('https://www.facebook.com/'+uid+'')
        try:
            try:
                FriendRequestAdd = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "FriendRequestAdd")))
                FriendRequestAdd.click()
            except:
                try:
                    addFriend = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Thêm bạn bè']")))
                    addFriend.click()
                except:
                    try:
                        self.driver.execute_script("document.getElementById('pagelet_timeline_profile_actions').getElementsByClassName('FriendRequestAdd')[0].click()")
                    except:
                        self.driver.execute_script("""document.querySelector("div[aria-label='Thêm bạn bè']").click()""")
        except:
            return False

                
        return True

    def acceptFriends(self, uid):
        self.driver.get('https://www.facebook.com/friends/requests/')
        try:
            requestFriendArea = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-id='"+uid+"']//button[1]")))
            requestFriendArea.click()
            # webdriver.ActionChains(self.driver).send_keys(
            #     Keys.TAB + Keys.TAB + Keys.ENTER).perform()
            return True
        except:
            return False
    # import ads excel
    def importAdsExcel(self, idCamp='', excelPath = 'camp.csv'):
        self.driver.get('https://www.facebook.com/adsmanager/manage/campaigns?act='+str(idCamp)+ '')
        try:
            campaign_group_tab = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//li[@data-testid='campaign_group_tab']")))
            campaign_group_tab.click()

            time.sleep(1)
            for index in range(1, 9):
                webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
                time.sleep(0.1)
            webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)
            webdriver.ActionChains(self.driver).send_keys(
                Keys.ARROW_UP + Keys.ARROW_UP + Keys.ENTER).perform()
            uploadExcel = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//input[@data-testid='import-file-input']")))
            uploadExcel.send_keys(os.path.abspath(excelPath))

            time.sleep(1)
            importButton = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-testid='import-button']")))
            importButton.click()

            for index in range(1, 10):
                try:
                    review_changes_button = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='review-changes-button']")))
                    review_changes_button.click()
                    #self.driver.execute_script("""document.querySelector("button[data-testid='review-changes-button']").click()""")
                    
                    checkboxErrorPost = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@style='letter-spacing: normal; color: rgb(28, 30, 33); font-size: 12px; font-family: Arial, sans-serif; line-height: 16px; font-weight: normal;']")))
                    break
                except:
                    print('doi hien')
                    time.sleep(4)
                    pass
            try:
                # label click

                #checkboxErrorPost = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//label[@style='letter-spacing: normal; color: rgb(28, 30, 33); font-size: 12px; font-family: Arial, sans-serif; line-height: 16px; font-weight: normal;']")))
                checkboxErrorPost.click()
                time.sleep(1)
                publishButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='continue-publish-button']")))
                publishButton.click()
                time.sleep(3)
            except:
                print('loi')

            
        except err:
            print('error cu lon deo biet o day dit me no')
            pass
        time.sleep(5)
    
    def quit(self):
        self.driver.stop_client()
        self.driver.close()

    def randomString(self, stringLength=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
    
    def fakeIT(self):

        req = requests.get(self.fakeURL)
        regexName = (r"<th width=\"30%\">Name<\/th>\n"
            r"					<td style=\"max-width:50px; word-wrap:break-word;\">(.*)<\/td>")
        addressRegex = (r"<th width=\"30%\">Adresse<\/th>\n"
            r"					<td style=\"max-width:50px; word-wrap:break-word;\">(.*)<\/td>")
        cityRegex = (r"<th width=\"30%\">Stadt<\/th>\n"
            r"					<td style=\"max-width:50px; word-wrap:break-word;\">(.*)<\/td>")
        bicRegex = (r"<th width=\"30%\">BIC<\/th>\n"
            r"					<td style=\"max-width:50px; word-wrap:break-word;\">\n						\n"
            r"						<div class=\"row\">\n							<div class=\"col-md-8\">(.*) </div>")
        ibanRegex = (r"					<th width=\"30%\">IBAN</th>\n"
            r"					<td style=\"max-width:50px; word-wrap:break-word;\">\n"
            r"						\n"
            r"						<div class=\"row\">\n"
            r"							\n"
            r"							<div class=\"col-md-8\">\n(.*)<form")

        name = re.findall(regexName, req.text)[0]
        address = re.findall(addressRegex, req.text)[0]
        city = re.findall(cityRegex, req.text)[0]
        bic = re.findall(bicRegex, req.text)[0]
        iban = re.findall(ibanRegex, req.text)[0]

        return({
            'name': name,
            'address': address,
            'city': city,
            'zipcode': '43100',
            'bic': bic,
            'iban': iban.strip()
        })
    def executeScript(self, script):
        try:
            self.driver.execute_script(script)
        except:
            print('error')
        
# enter command
createAds = False
testChangeIP = False
updateCookie = False
hideWindow = False
checkKey = False
auto50 = False
proxyIP = ''
fakeURL = 'https://identinator.com/?for_country=aut'
createAdsAccount = False
shareAccountAds = False
keyActive = ''
pathExcel = ''
mainID = ''
numberThread = 1
totalThread = 1

for index in range(1, len(sys.argv)):
    if sys.argv[index] == '-credit':
        message_bytes = base64.b64decode(sys.argv[index + 1])
        message = message_bytes.decode('ascii')
        creditCard = json.loads(message)
    if sys.argv[index] == '-acc':
        message_bytes = base64.b64decode(sys.argv[index + 1])
        message = message_bytes.decode('ascii')
        account = json.loads(message)
    # ads get params
    if sys.argv[index] == '-createAdsAccount':
        createAdsAccount = True
    if sys.argv[index] == '-moneyIndex':
        moneyIndex = sys.argv[index + 1]
    if sys.argv[index] == '-timeIndex':
        timeIndex = sys.argv[index + 1]
    if sys.argv[index] == '-countryIndex':
        countryIndex = sys.argv[index + 1]
    if sys.argv[index] == '-updateCookie':
        updateCookie = True
    if sys.argv[index] == '-proxy':
        proxyIP = sys.argv[index + 1]
    if sys.argv[index] == '-test':
        testChangeIP = True
    if sys.argv[index] == '-hideWindow':
        hideWindow = True
    if sys.argv[index] == '-fakeURL':
        fakeURL = sys.argv[index + 1]
    if sys.argv[index] == '-keyActive':
        keyActive = sys.argv[index + 1]
    if sys.argv[index] == '-checkKey':
        checkKey = True
    if sys.argv[index] == '-auto50':
        auto50 = True
    if sys.argv[index] == '-typeAcc':
        typeAcc = sys.argv[index + 1]
    if sys.argv[index] == '-shareAccountAds':
        shareAccountAds = True
    if sys.argv[index] == '-pathExcel':
        pathExcel = sys.argv[index + 1]
    if sys.argv[index] == '-mainID':
        mainID = sys.argv[index + 1]
    if sys.argv[index] == '-auto50.changeMoney':
        if sys.argv[index + 1] == 'true':
            auto50ChangeMoney = True
        else:
            auto50ChangeMoney = False
    if sys.argv[index] == '-numberThread':
        numberThread = sys.argv[index + 1]
    if sys.argv[index] == '-totalThread':
        totalThread = sys.argv[index + 1]
# share account Ads
if shareAccountAds:
    result = {
        'status': 'fail',
        'msg': 'unknown error',
    }
    if typeAcc == 'main':
        
        fbMain = autofb(proxyIP, hideWindow, fakeURL, keyActive, 'left')
        fbMain.login(account)
        fbInfo = fbMain.getInfo()
        if fbInfo:
            #add to database
            mainDB = TinyDB('mainDB.json')
            Main = Query()
            checkUID = mainDB.search((where('uid') == fbInfo['uid']) & (where('name') ==  fbInfo['name']))

            if len(checkUID) <= 0:
                mainDB.insert({
                    'uid': fbInfo['uid'],
                    'name': fbInfo['name']
                })
            #find infor

            while (True):
                cloneDB = TinyDB('cloneDB.json')
                
                #add friends 
                waitingList = cloneDB.search((where('mainID') == fbInfo['uid']) & (where('status') == 'WAITING'))
                print('waiting add')
                print(waitingList)
                for cloneInfo in waitingList:
                    #add friend to 
                    print('add friend to ')
                    print(cloneInfo)
                    fbMain.addFriends(cloneInfo['cloneUID'])
                    #update status 
                    cloneDB.update({'status': 'ADDED'}, (where('mainID') == fbInfo['uid']) & (where('cloneUID') == cloneInfo['cloneUID']))
                
                
                waitingImport = cloneDB.search((where('mainID') == fbInfo['uid']) & (where('status')== 'WAITING_IMPORT'))
                print('wwaiting import')
                print(waitingImport)
                for cloneInfo in waitingImport:
                    print('clone infor')
                    print(cloneInfo)
                    fbMain.importAdsExcel(cloneInfo['campID'], pathExcel)
                    cloneDB.update({'status': 'DONE'}, (where('mainID') == fbInfo['uid']) & (where('cloneUID') == cloneInfo['cloneUID']))
                time.sleep(3)
                print('repeat---------')
        else:
            result['msg'] = 'login fail'
    else:
        fbClone = autofb(proxyIP, hideWindow, fakeURL, keyActive, 'right', numberThread, totalThread)
        account['loginType'] = 'account'
        fbClone.login(account)
        fbInfo = fbClone.getInfo()
        if fbInfo:
            #fbClone.shareAccountAdsCloneAuto(fbInfo['uid'], moneyIndex, timeIndex, countryIndex)
            #search info of main uid
            mainDB = TinyDB('./mainDB.json')
            mainAccount = mainDB.search(where('uid') == mainID)
            cloneDB = TinyDB('./cloneDB.json')
            Clone = Query()
            if len(mainAccount) > 0:
                
                cloneDB.insert({
                    'cloneUID': fbInfo['uid'],
                    'mainID'  : mainID,
                    'campID'  : '',
                    'status'  : 'WAITING'
                })
                while(True):
                    cloneDB = TinyDB('cloneDB.json')
                    
                    checkAdded = cloneDB.search((where('cloneUID') == fbInfo['uid']) & (where('status') == 'ADDED') & (where('mainID') == mainID))


                    if len(checkAdded) > 0:
                        fbClone.acceptFriends(mainID)
                        fbClone.addAdsAccount(moneyIndex, timeIndex, countryIndex)
                        idCamp = fbClone.addMainCloneAds(mainAccount[0]['name'])
                        #update camp
                        cloneDB.update({'status' : 'WAITING_IMPORT', 'campID': idCamp}, Clone.cloneUID == fbInfo['uid'])
                        break
                    time.sleep(1)
                time.sleep(15)
                fbClone.quit()
            # update message
            result['status'] = 'success'
            result['msg'] = ''
        else:
            result['msg'] = 'login fail'

    print(json.dumps(result, indent=4, sort_keys=True))
    exit()


# share account Ads
if auto50:
    result = {
        'status': 'fail',
        'msg': 'unknown error',
    }
    if typeAcc == 'main':
        fbMain = autofb(proxyIP, hideWindow, fakeURL, keyActive, 'left')
        fbMain.login(account)
        fbInfo = fbMain.getInfo()
        print(fbInfo)
        if fbInfo:
            #add to database
            mainDB = TinyDB('./mainDB.json')
            Main = Query()
            checkUID = mainDB.search((where('uid') == fbInfo['uid']) & (where('name') ==  fbInfo['name']))

            if len(checkUID) <= 0:
                mainDB.insert({
                    'uid': fbInfo['uid'],
                    'name': fbInfo['name']
                })
            #find infor

            while (True):
                cloneDB = TinyDB('./cloneDB.json')
                fbMain.executeScript('console.log("run ne")')
                #add friends 
                waitingList = cloneDB.search((where('mainID') == fbInfo['uid']) & (where('status') == 'WAITING'))
                print('waiting add')
                print(waitingList)
                for cloneInfo in waitingList:
                    #add friend to 
                    print('add friend to ')
                    print(cloneInfo)
                    fbMain.addFriends(cloneInfo['cloneUID'])
                    #update status 
                    cloneDB.update({'status': 'ADDED'}, (where('mainID') == fbInfo['uid']) & (where('cloneUID') == cloneInfo['cloneUID']))
                
                
                waitingImport = cloneDB.search((where('mainID') == fbInfo['uid']) & (where('status')== 'WAITING_IMPORT'))
                

                for cloneInfo in waitingImport:
                    fbMain.importAdsExcel(cloneInfo['campID'], pathExcel)
                    cloneDB.update({'status': 'DONE'}, (where('mainID') == fbInfo['uid']) & (where('cloneUID') == cloneInfo['cloneUID']))
                time.sleep(15)
                print('repeat---------')
        else:
            result['msg'] = 'login fail'
            fbMain.executeScript('alert("login that bai do loi, chay acc chinh lai")')
            fbMain.quit()
    else:
        fbClone = autofb(proxyIP, hideWindow, fakeURL, keyActive, 'right', numberThread, totalThread)
        account['loginType'] = 'account'
        fbClone.login(account)
        fbInfo = fbClone.getInfo()
        if fbInfo:
            
            #fbClone.shareAccountAdsCloneAuto(fbInfo['uid'], moneyIndex, timeIndex, countryIndex)
            #search info of main uid
            mainDB = TinyDB('mainDB.json')
            mainAccount = mainDB.search(where('uid') == mainID)
            cloneDB = TinyDB('cloneDB.json')
            Clone = Query()
            if len(mainAccount) > 0:
                cloneDB.insert({
                    'cloneUID': fbInfo['uid'],
                    'mainID'  : mainID,
                    'campID'  : '',
                    'status'  : 'WAITING'
                })
                while(True):
                    cloneDB = TinyDB('cloneDB.json')
                    
                    checkAdded = cloneDB.search((where('cloneUID') == fbInfo['uid']) & (where('status') == 'ADDED') & (where('mainID') == mainID))
                    

                    if len(checkAdded) > 0:
                        fbClone.acceptFriends(mainID)
                        if auto50ChangeMoney:
                            addCredit = fbClone.addCredit(creditCard)
                            idCamp = fbClone.addMainCloneAds(mainAccount[0]['name'])
                        else:
                            idCamp = fbClone.addMainCloneAds(mainAccount[0]['name'])
                            addCredit = fbClone.addCredit(creditCard)
                        #update camp
                        cloneDB.update({'status' : 'WAITING_IMPORT', 'campID': idCamp}, Clone.cloneUID == fbInfo['uid'])
                        break
                    time.sleep(2)
                time.sleep(5)
                fbClone.quit()
            # update message
            if addCredit:
                result['status'] = 'success'
                result['msg'] = ''
            else:
                result['status'] = 'fail'
                result['msg'] = 'add credit error'
        else:
            result['msg'] = 'login fail'

    print(json.dumps(result, indent=4, sort_keys=True))
    exit()




if testChangeIP:
    fb.testChangeIP()
    time.sleep(10000)
    exit()
if checkKey:
    check = requests.get('http://199.34.16.50/checkKeys.php?key='+keyActive+'')
    print(check.text)
    exit()
fb = autofb(proxyIP, hideWindow, fakeURL, keyActive)
if updateCookie:
    fb.login(account)
    if fb.checkLogin():
        cookies = fb.getCookie()
        result = {
            'status': 'success',
            'msg': 'ok',
            'cookie': cookies
        }
    else:
        result = {
            'status': 'fail',
            'msg': 'Login fail'
        }
    print(json.dumps(result, indent=4, sort_keys=True))
    fb.quit()

else:
    result = {
        'status': 'fail',
        'msg': 'connect fail ! retry '
    }
    fb.login(account)
    try:
        # check login account
        if fb.checkLogin():
            if createAdsAccount:
                addAdsAction = fb.addAdsAccount(
                    moneyIndex, timeIndex, countryIndex)
                if addAdsAction:
                    result = {
                        'status': 'success',
                        'msg': ''
                    }
                else:
                    result = {
                        'status': 'fail',
                        'msg': 'checkpoint'
                    }
            else:
                fb.addCredit(creditCard)
                result = {
                    'status': 'success',
                    'msg': 'action call success'
                }
        else:
            result = {
                'status': 'fail',
                'msg': 'login fail'
            }
    except:
        pass

    fb.quit()
    print(json.dumps(result, indent=4, sort_keys=True))
