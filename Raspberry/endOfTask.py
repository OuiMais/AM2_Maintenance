"""
    Projet : AM2_Auto / endOfTask
    Date Creation : 29/12/2023
    Date Revision : 29/12/2023
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Termine les taches à finir
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

try:
    # Essayez de trouver l'élément
    endOfElement = browser.find_element(By.ID, 'rightInfoBoxContent')
except NoSuchElementException:
    # Si l'élément n'est pas trouvé, attribuez une valeur spécifique (par exemple, une chaîne vide)
    endOfElement = ''
    time.sleep(1)

if endOfElement != '':
    terminer_links = endOfElement.find_elements(By.CSS_SELECTOR, 'a.useAjax')
    finish = 0

    for i in range(len(terminer_links)):
        try:
            # Essayez de trouver l'élément
            endOfElement = browser.find_element(By.ID, 'rightInfoBoxContent')
            link = endOfElement.find_element(By.CSS_SELECTOR, 'a.useAjax')
        except NoSuchElementException:
            # Si l'élément n'est pas trouvé, attribuez une valeur spécifique (par exemple, une chaîne vide)
            link = ''
            time.sleep(1)

        if link != '':
            if link.text == "Terminer":
                link.click()
                time.sleep(5)
                browser.get('https://www.airlines-manager.com/maintenance/group')
                time.sleep(5)
                finish += 1

    if finish != 0:
        notif = str(finish) + " maintenance(s) terminée(s)."
        push = pb.push_note('AM2 Bot', notif)
    else:
        notif = "Pas de maintenance à terminer."
        push = pb.push_note('AM2 Bot', notif)
else:
    # Envoie d'une notification
    notif = "Pas de maintenance à terminer."
    push = pb.push_note('AM2 Bot', notif)

browser.get('https://www.airlines-manager.com/maintenance/group')
time.sleep(2)

browser.close()
