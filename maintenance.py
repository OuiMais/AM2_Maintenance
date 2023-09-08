"""
    Projet : AM2_Auto / maintenance
    Date Creation : 07/12/2022
    Date Revision : 28/08/2023
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Permet de toujours avoir des avions en bon état
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time

# Option for website (no screen open)
options = Options()
options.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(options=options)

# Open the Website
browser.get('https://www.airlines-manager.com/maintenance/book')

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

etatFlotte = browser.find_element(by=By.ID, value='donutchart_div_aircraftNumberByWear_legend').text

ancienneteFlotte = browser.find_element(by=By.ID, value='donutchart_div_aircraftNumberByMark_legend').text

if len(etatFlotte) > 30:
    print('Avion a réparer')
else:
    print("Pas d'avion à réparer")
    
if len(ancienneteFlotte) > 20:
    print("Check D")
else:
    print("Pas de check D à faire")
