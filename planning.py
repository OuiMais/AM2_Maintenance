"""
    Projet : AM2_Auto / Planning
    Date Creation : 07/12/2022
    Date Revision : 28/08/2023
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Recupere les demandes restantes
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
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
browser.get('https://www.airlines-manager.com/network/planning')

# Your  credentials
name = 'flohofbauer@icloud.com'
mdp = 'Flo17Titi!'

# Fill credentials
browser.find_element(by=By.NAME, value='_username').send_keys(name)
browser.find_element(by=By.NAME, value='_password').send_keys(mdp)

# Click Log In
browser.find_element(by=By.ID, value='loginSubmit').click()
time.sleep(5)

# Click accept cookies
browser.find_element(by=By.CLASS_NAME, value='cc-compliance').click()
time.sleep(5)

# List of aircraft with number of line
elements = browser.find_elements(By.CLASS_NAME, "aircraftListMiniBox")

# Parcourez les éléments et récupérez les valeurs de l'attribut "id"
aircraftsIds = [element.get_attribute("id") for element in elements]
aircraftsIds.pop()

nomAvion = []

for aircraftId in aircraftsIds:
    nomAvion.append([aircraftId, 0])

jour = ['Lundi', 'Mardi', 'Mecredi', 'Jeudi', 'Vendredi', 'Samedi', 'Diamnche']

ligneRecupere = []

printProgressBar(0, len(nomAvion), prefix='Progress:', suffix='Complete', length=50)

# Copy info and start a CSV doc
fichiercsv = open('demandePlanning.csv', 'w', newline='')

writer = csv.writer(fichiercsv)
data = ['Ligne; Classe; Lundi; Mardi; Mercredi; Jeudi; Vendredi; Samedi; Dimanche']
writer.writerow(data)  # Start CSV

for avion in range(len(nomAvion)):
    if avion % 6 == 0:
        if avion != 0:
            # Each plane box contain 6 planes so if you have more than 6 planes, you need to change the page every 6 planes
            browser.find_element(by=By.XPATH,
                                 value="//div[@class='sliderRight' and @id='aircraftSliderRight']").click()
            time.sleep(1)
    if avion != 0:
        # Access plane
        accessAvion = "//div[@class='aircraftListMiniBox' and @id='" + str(nomAvion[avion][0]) + "']"
        browser.find_element(by=By.XPATH, value=accessAvion).click()
        time.sleep(2)

    recupLigne = browser.find_element(by=By.XPATH, value="//div[@id='lineList']").text
    nbLigne = 0
    for position in range(len(recupLigne)):
        if recupLigne[position] == '-':
            nbLigne = nbLigne + 1
    nomAvion[avion][1] = nbLigne

    for nLigne in range(nbLigne):
        # Select line
        access = "//div[@id='lineList']/span[" + str(nLigne + 1) + ']'
        browser.find_element(by=By.XPATH, value=access).click()
        ligne = browser.find_element(by=By.XPATH, value=access).text

        indexLigne = ligne.find('-')
        taille = len(ligne) - indexLigne
        for ligneN in range(taille):
            ligne = ligne[:-1]

        dejaPresent = 0

        if len(ligneRecupere) != 0:
            for ligneRecupereATester in ligneRecupere:
                if ligne == ligneRecupereATester:
                    dejaPresent = 1
                    break

        if not dejaPresent:
            ligneRecupere.append(ligne)
            writeTab = [[ligne + ';Eco'], [ligne + ';Affaire'], [ligne + ';First'], [ligne + ';Cargo']]

            # Line informations for each day
            demand = browser.find_element(by=By.ID, value='demand').text
            index = [demand.find('Lundi'), demand.find('Mardi'), demand.find('Mercredi'), demand.find('Jeudi'), demand.find('Vendredi'), demand.find('Samedi'), demand.find('Dimanche'), len(demand)]

            placeEcoMin = 1000000000
            placeAffaireMin = 1000000000
            placeFirstMin = 1000000000
            placeCargoMin = 1000000000

            # Change format for CSV
            for semaine in range(7):
                P = []
                for pos in range(index[semaine + 1] - index[semaine]):
                    if demand[index[semaine] + pos] == ' ':
                        P.append(index[semaine] + pos)

                Neco = P[1] - P[0]
                placeEco = ''
                for position in range(Neco - 1):
                    placeEco = placeEco + demand[P[0] + 1 + position]

                if int(placeEco) < placeEcoMin:
                    placeEcoMin = int(placeEco)

                Naffaire = P[3] - P[2]
                placeAffaire = ''
                for position in range(Naffaire - 1):
                    placeAffaire = placeAffaire + demand[P[2] + 1 + position]

                if int(placeAffaire) < placeAffaireMin:
                    placeAffaireMin = int(placeAffaire)

                Nfirst = P[5] - P[4]
                placeFirst = ''
                for position in range(Nfirst - 1):
                    placeFirst = placeFirst + demand[P[4] + 1 + position]

                if int(placeFirst) < placeFirstMin:
                    placeFirstMin = int(placeFirst)

                Ncargo = P[6] - P[5]
                placeCargo = ''
                for position in range(Ncargo - 1):
                    placeCargo = placeCargo + demand[P[6] + 1 + position]

                if int(placeCargo) < placeCargoMin:
                    placeCargoMin = int(placeCargo)

                writeTab[0].append(';' + str(placeEco))
                writeTab[1].append(';' + str(placeAffaire))
                writeTab[2].append(';' + str(placeFirst))
                writeTab[3].append(';' + str(placeCargo))

            writeTab[0].append(';' + str(placeEcoMin))
            writeTab[1].append(';' + str(placeAffaireMin))
            writeTab[2].append(';' + str(placeFirstMin))
            writeTab[3].append(';' + str(placeCargoMin))

            # Print on CSV
            for y in range(4):
                stringTest = []
                for z in range(9):
                    stringTest.append(writeTab[y][z])

                writer.writerow(stringTest)
    printProgressBar(avion + 1, len(nomAvion), prefix='Progress:', suffix='Complete', length=50)

fichiercsv.close()
browser.close()
