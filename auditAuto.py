"""
    Projet : AM2_Auto / auditAuto
    Date Creation : 07/12/2022
    Date Revision : 28/08/2023
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Audit interne auto et mise à jour des prix
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd=""):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


# Option for website (no screen open)
options = Options()
options.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(options=options)

# Open the Website
browser.get('http://www.airlines-manager.com/marketing/pricing/')

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

howFindLast = browser.find_element(By.CLASS_NAME, "last").find_element(By.TAG_NAME, "a").get_attribute("href")
tamponLast = howFindLast.split("=")
last = int(tamponLast[-1])

for tour in range(last):

    linked = browser.find_elements(By.TAG_NAME, "a")

    links = [element.get_attribute("href") for element in linked]

    # Donnée précise avec laquelle les liens doivent commencer
    debut_donnee = "http://www.airlines-manager.com/marketing/pricing/"

    # Extraire les liens qui commencent par la donnée précise
    liens_extraits = [lien for lien in links if lien is not None and lien.startswith(debut_donnee)]

    nbLink = len(liens_extraits) - 3

    liens_extraits = liens_extraits[5:nbLink]
    prefixTour = "Process tour n° " + str(tour + 1)

    printProgressBar(0, len(liens_extraits), prefix=prefixTour, suffix="Complete", length=50)
    iteration = 0
    for link in liens_extraits:
        browser.get(link)

        tampon = link.split('/')
        newLink = tampon[0] + "//" + tampon[2] + "/" + tampon[3] + "/internalaudit/line/" + tampon[-1] + "?fromPricing=1"

        browser.get(newLink)

        recup = browser.find_element(By.CLASS_NAME, "box1").text
        recup = recup.split("\n")

        tarif = [elmt for elmt in recup if elmt.startswith("Tarif idéal")]

        tarifEco = int(tarif[0].split(" : ")[1][:-1])
        tarifAffaire = int(tarif[1].split(" : ")[1][:-1])
        tarifFirst = int(tarif[2].split(" : ")[1][:-1])
        tarifCargo = int(tarif[3].split(" : ")[1][:-1])

        input_element = browser.find_element(By.ID, "line_priceEco")
        input_element.clear()
        nouvelle_valeur = tarifEco
        input_element.send_keys(nouvelle_valeur)

        input_element = browser.find_element(By.ID, "line_priceBus")
        input_element.clear()
        nouvelle_valeur = tarifAffaire
        input_element.send_keys(nouvelle_valeur)

        input_element = browser.find_element(By.ID, "line_priceFirst")
        input_element.clear()
        nouvelle_valeur = tarifFirst
        input_element.send_keys(nouvelle_valeur)

        input_element = browser.find_element(By.ID, "line_priceCargo")
        input_element.clear()
        nouvelle_valeur = tarifCargo
        input_element.send_keys(nouvelle_valeur)

        browser.find_element(by=By.CLASS_NAME, value='validBtn validBtnBlue').click()
        time.sleep(5)

        iteration += 1
        printProgressBar(iteration, len(liens_extraits), prefix=prefixTour, suffix="Complete", length=50)

    if tour != last - 1:
        browser.find_element(By.CLASS_NAME, "next").click()

browser.close()
