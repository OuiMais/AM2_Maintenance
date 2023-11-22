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
import time

# Option for website (no screen open)
options = Options()
# options.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(options=options)

# Open the Website
# browser.get('https://www.airlines-manager.com/home/wheeltcgame')
#
# # Your  credentials
# name = 'flohofbauer@icloud.com'
# mdp = 'Flo17Titi!'
#
# # Fill credentials
# browser.find_element(by=By.NAME, value='_username').send_keys(name)
# browser.find_element(by=By.NAME, value='_password').send_keys(mdp)
#
# # Click Log In
# browser.find_element(by=By.ID, value='loginSubmit').click()
# time.sleep(5)
#
# #Click accept cookies
# browser.find_element(by=By.CLASS_NAME, value='cc-compliance').click()
# time.sleep(5)
#
# browser.find_element(By.CLASS_NAME, 'validBtnBlue').click()
# time.sleep(5)
#
# browser.find_element(By.LINK_TEXT, 'Je récupère mon gain').click()
# time.sleep(5)

browser.get('https://www.airlines-manager.com/shop/workshop')

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

browser.find_element(By.LINK_TEXT, 'Gratuit').click()
time.sleep(5)
# Ajouter la détecteion des avions pour les envoyer au garage

browser.close()
