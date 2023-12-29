"""
    Projet : AM2_Auto / maintenance
    Date Creation : 07/12/2022
    Date Revision : 29/12/2023
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Permet de toujours avoir des avions en bon état
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from pushbullet import Pushbullet

# Option for website (no screen open)
options = Options()
options.add_argument('--headless')
options.add_argument("-disable-gpu")

path = '/usr/bin/chromedriver'
service = Service(executable_path=path)

# Initiate the browser
browser = webdriver.Chrome(service=service, options=options)

# Open the Website
browser.get('https://www.airlines-manager.com/maintenance/group')

# Your  credentials
name = 'flohofbauer@icloud.com'
mdp = 'Flo17Titi!'
levelBeforeIncident = 13

# API for notification
api_key = 'o.6RxYZlji3PYG1hlGhezV6pOGoH4VPucu'
pb = Pushbullet(api_key)

# Fill credentials
browser.find_element(by=By.NAME, value='_username').send_keys(name)
browser.find_element(by=By.NAME, value='_password').send_keys(mdp)

# Click Log In
browser.find_element(by=By.ID, value='loginSubmit').click()
time.sleep(5)

#Click accept cookies
browser.find_element(by=By.CLASS_NAME, value='cc-compliance').click()
time.sleep(5)

browser.find_element(By.ID, 'silverArrowLeftMark').click()
time.sleep(5)

checkDLC = int(browser.find_element(By.ID, 'longHaulAircraftsCount').text)
checkDMC = int(browser.find_element(By.ID, 'mediumHaulAircraftsCount').text)
checkDCC = int(browser.find_element(By.ID, 'shortHaulAircraftsCount').text)

checkD = checkDCC + checkDMC + checkDLC

browser.find_element(By.ID, 'silverArrowRightMark').click()

for checkA in range(levelBeforeIncident):
    browser.find_element(By.ID, 'silverArrowLeftWear').click()
time.sleep(5)

checkALC = int(browser.find_element(By.ID, 'longHaulAircraftsCount').text)
checkAMC = int(browser.find_element(By.ID, 'mediumHaulAircraftsCount').text)
checkACC = int(browser.find_element(By.ID, 'shortHaulAircraftsCount').text)

checkA = checkACC + checkAMC + checkALC

if checkA != 0:
    if checkD != 0:
        browser.find_element(By.ID, 'submitCheckD').click()
        time.sleep(5)
        browser.find_element(By.LINK_TEXT, 'Valider').click()
        time.sleep(2)

        # Envoie d'une notification
        notif = "Maintenance: check D de " + str(checkA) + " avion(s)!"
        push = pb.push_note('AM2 Bot', notif)
    else:
        browser.find_element(By.ID, 'submitCheckA').click()
        time.sleep(5)
        browser.find_element(By.LINK_TEXT, 'Valider').click()
        time.sleep(2)

        # Envoie d'une notification
        notif = "Maintenance: check A de " + str(checkA) + " avion(s)!"
        push = pb.push_note('AM2 Bot', notif)
else:
    # Envoie d'une notification
    notif = "Pas de maintenance à effectuer."
    push = pb.push_note('AM2 Bot', notif)

# browser.get('https://www.airlines-manager.com/maintenance/group')
#
# try:
#     # Essayez de trouver l'élément
#     endOfElement = browser.find_element(By.ID, 'rightInfoBoxContent')
# except NoSuchElementException:
#     # Si l'élément n'est pas trouvé, attribuez une valeur spécifique (par exemple, une chaîne vide)
#     endOfElement = ''
#     time.sleep(1)
#
# if endOfElement != '':
#     terminer_links = endOfElement.find_elements(By.CSS_SELECTOR, 'a.useAjax')
#     finish = 0
#
#     for i in range(len(terminer_links)):
#         try:
#             # Essayez de trouver l'élément
#             endOfElement = browser.find_element(By.ID, 'rightInfoBoxContent')
#             link = endOfElement.find_element(By.CSS_SELECTOR, 'a.useAjax')
#         except NoSuchElementException:
#             # Si l'élément n'est pas trouvé, attribuez une valeur spécifique (par exemple, une chaîne vide)
#             link = ''
#             time.sleep(1)
#
#         if link != '':
#             if link.text == "Terminer":
#                 link.click()
#                 time.sleep(5)
#                 browser.get('https://www.airlines-manager.com/maintenance/group')
#                 time.sleep(5)
#                 finish += 1
#
#     notif = str(finish) + " maintenance(s) terminée(s)."
#     push = pb.push_note('AM2 Bot', notif)
# else:
#     # Envoie d'une notification
#     notif = "Pas de maintenance à terminer."
#     push = pb.push_note('AM2 Bot', notif)

browser.get('https://www.airlines-manager.com/maintenance/group')
time.sleep(2)

browser.close()
