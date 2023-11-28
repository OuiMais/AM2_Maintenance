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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Option for website (no screen open)
options = Options()
# options.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(options=options)

# Open the Website
browser.get('https://www.airlines-manager.com/home/wheeltcgame')

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

# browser.find_element(By.CLASS_NAME, 'validBtnBlue').click()
# time.sleep(5)
#
# gainWheel = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.ID, "Je récupère mon gain")))
#
# # Effectuez des actions sur mon_element
# gainWheel.click()

# time.sleep(5)
#
# browser.get('https://www.airlines-manager.com/shop/workshop')
# time.sleep(5)
#
# browser.find_element(By.LINK_TEXT, 'Gratuit').click()
# time.sleep(5)
#
# yesButton = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.ID, "form_purchase")))
# yesButton.click()
# time.sleep(5)
#
# # Ajouter la détecteion des avions pour les envoyer au garage

browser.get('https://www.airlines-manager.com/shop/cardholder')

freeCard = ''
freeCard = browser.find_element(By.XPATH, "//button[@class='cardholder-cardinfo-button validBtnBlue' and 'Gratuit']")

if freeCard != '':
    freeCard.click()
    time.sleep(5)
    browser.find_element(By.XPATH, "//a[@class='purchaseButton useAjax' and 'Gratuit']").click()
    time.sleep(5)
    yesButton = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.ID, "form_purchase")))
    yesButton.click()
    time.sleep(5)

    cards = browser.find_elements(By.ID, 'placeholderCards')
    cardsNumber = len(cards)

    for i in range(cardsNumber):
        browser.find_element(By.CLASS_NAME, 'showCards-crad back-card').click()
        time.sleep(5)

    browser.find_element(By.XPATH, "//button[@class='validBtnBlue closeGift' and 'Continuer']").click()
    time.sleep(5)

browser.close()