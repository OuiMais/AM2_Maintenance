"""
    Projet : AM2_Auto / autoDailyGift
    Date Creation : 22/11/2023
    Date Revision : 22/11/2023
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Permet d'obtenir tous les cadeaux quotidiens
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

# Option for website (no screen open)
options = Options()
# options.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(options=options)

# Open the Website
browser.get('https://www.airlines-manager.com/home/wheeltcgame')
# browser.get('https://www.airlines-manager.com/shop/cardholder')

# Your  credentials
name = 'flohofbauer@icloud.com'
mdp = 'Flo17Titi!'

# Fill credentials
browser.find_element(by=By.NAME, value='_username').send_keys(name)
browser.find_element(by=By.NAME, value='_password').send_keys(mdp)

# Click Log In
browser.find_element(by=By.ID, value='loginSubmit').click()
time.sleep(5)

#Click accept cookies
browser.find_element(by=By.CLASS_NAME, value='cc-compliance').click()
time.sleep(5)

browser.find_element(By.ID, 'play').click()
time.sleep(5)

gainWheel = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH,
                                                                               "//span[@class='purchaseButton
                                                                               validateWinPopup']")))

# Effectuez des actions sur mon_element
gainWheel.click()

time.sleep(5)

browser.get('https://www.airlines-manager.com/shop/workshop')
time.sleep(5)

browser.find_element(By.XPATH, "//a[@class='purchaseButton useAjax']//div[contains(text(), 'Gratuit')]").click()
time.sleep(5)

yesButton = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.ID, "form_purchase")))
yesButton.click()
time.sleep(5)

# Ajouter la détecteion des avions pour les envoyer au garage

browser.get('https://www.airlines-manager.com/shop/cardholder')

try:
    freeCard = browser.find_element(By.XPATH, "//button[@class='cardholder-cardinfo-button validBtnBlue' and 'Gratuit']")
except NoSuchElementException:
    freeCard = ''
    time.sleep(1)

if freeCard != '':
    freeCard.click()
    time.sleep(2)
    try:
        gratuit_button = browser.find_element(By.XPATH, "//div[@class='buyCardHolder-containCard-buy']//a[contains(text(), 'Gratuit')]")
    except NoSuchElementException:
        gratuit_button = ''

    if gratuit_button != '':
        ActionChains(browser).move_to_element(gratuit_button).click().perform()
        time.sleep(5)
        yesButton = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.ID, "form_purchase")))
        yesButton.click()
        time.sleep(5)

        cards = browser.find_elements(By.CLASS_NAME, 'placeholderCards') # 17102000
        cardsNumber = len(cards)

        for i in range(cardsNumber):
            browser.find_element(By.XPATH, "//div[@class='showCards-card back-card']").click()
            time.sleep(5)

        browser.find_element(By.XPATH, "//button[@class='validBtnBlue closeGift' and 'Continuer']").click()
        time.sleep(5)

browser.close()
