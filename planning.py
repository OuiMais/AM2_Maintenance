###############################################################################
#                       Recuperation donnes Plannings AM2
#                           Florian 11/2021
###############################################################################

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
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
opt = Options()
opt.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(ChromeDriverManager().install(), options=opt)

# Open the Website
browser.get('https://www.airlines-manager.com/network/planning')

# Your  credentials
name = 'flohofbauer@icloud.com';
mdp = 'Flo17Titi!';

# Fill credentials
browser.find_element(by=By.NAME, value='_username').send_keys(name);
browser.find_element(by=By.NAME, value='_password').send_keys(mdp);

# Click Log In
browser.find_element(by=By.ID, value='loginSubmit').click();
time.sleep(5)

# Click accept cookies
browser.find_element(by=By.CLASS_NAME, value='cc-compliance').click();
time.sleep(5)

# List of aircraft with number of line
nomAvion = [['aircraftId_81623210', 0],  # OMG-000
            ['aircraftId_79307909', 0],  # OMG-1
            ['aircraftId_79979223', 0],  # OMG-10
            ['aircraftId_80297916', 0],  # OMG-11
            ['aircraftId_80421251', 0],  # OMG-12
            ['aircraftId_80548530', 0],  # OMG-13

            ['aircraftId_80498689', 0],  # OMG-14
            ['aircraftId_80715955', 0],  # OMG-15
            ['aircraftId_80836906', 0],  # OMG-16
            ['aircraftId_80933120', 0],  # OMG-17
            ['aircraftId_80984015', 0],  # OMG-18
            ['aircraftId_81035341', 0],  # OMG-19

            ['aircraftId_79308208', 0],  # OMG-2
            ['aircraftId_81115528', 0],  # OMG-20
            ['aircraftId_81140070', 0],  # OMG-21
            ['aircraftId_81236944', 0],  # OMG-22
            ['aircraftId_81237106', 0],  # OMG-23
            ['aircraftId_81563818', 0],  # OMG-24

            ['aircraftId_81673508', 0],  # OMG-25
            ['aircraftId_81857176', 0],  # OMG-26
            ['aircraftId_82443557', 0],  # OMG-27
            ['aircraftId_82836198', 0],  # OMG-28
            ['aircraftId_82880587', 0],  # OMG-29
            ['aircraftId_79311875', 0],  # OMG-3

            ['aircraftId_82959740', 0],  # OMG-30
            ['aircraftId_89137698', 0],  # OMG-31
            ['aircraftId_95606277', 0],  # OMG-32
            ['aircraftId_95809128', 0],  # OMG-33
            ['aircraftId_95879249', 0],  # OMG-34
            ['aircraftId_96287622', 0],  # OMG-35

            ['aircraftId_96486823', 0],  # OMG-36
            ['aircraftId_96939940', 0],  # OMG-37
            ['aircraftId_106505199', 0],  # OMG-38
            ['aircraftId_107015513', 0],  # OMG-39
            ['aircraftId_79336039', 0],  # OMG-4
            ['aircraftId_107291673', 0],  # OMG-40

            ['aircraftId_107508743', 0],  # OMG-41
            ['aircraftId_79440221', 0],  # OMG-5
            ['aircraftId_79440218', 0],  # OMG-6
            ['aircraftId_79710828', 0],  # OMG-7
            ['aircraftId_79730109', 0],  # OMG-8
            ['aircraftId_79796961', 0]]  # OMG-9

jour = ['Lundi', 'Mardi', 'Mecredi', 'Jeudi', 'Vendredi', 'Samedi', 'Diamnche'];

# Copy info and start a CSV doc
with open('demandePlanning.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv)
    data = ['Ligne; Classe; Lundi; Mardi; Mercredi; Jeudi; Vendredi; Samedi; Dimanche']
    writer.writerow(data)  # Start CSV
    printProgressBar(0, len(nomAvion), prefix='Progress:', suffix='Complete', length=50)
    for avion in range(len(nomAvion)):
        if avion % 6 == 0:
            if avion != 0:
                # Each plane box contain 6 planes so if you have more than 6 planes, you need to change the page every 6 planes
                browser.find_element(by=By.XPATH,
                                     value="//div[@class='sliderRight' and @id='aircraftSliderRight']").click();
                time.sleep(1)
        if avion != 0:
            # Access plane
            accessAvion = "//div[@class='aircraftListMiniBox' and @id='" + str(nomAvion[avion][0]) + "']";
            browser.find_element(by=By.XPATH, value=accessAvion).click();
            time.sleep(2);

        recupLigne = browser.find_element(by=By.XPATH, value="//div[@id='lineList']").text;
        nbLigne = 0;
        for position in range(len(recupLigne)):
            if recupLigne[position] == '-':
                nbLigne = nbLigne + 1;
        nomAvion[avion][1] = nbLigne;

        for nLigne in range(nbLigne):
            # Select line
            access = "//div[@id='lineList']/span[" + str(nLigne + 1) + ']';
            browser.find_element(by=By.XPATH, value=access).click();
            ligne = browser.find_element(by=By.XPATH, value=access).text;

            indexLigne = ligne.find('-');
            taille = len(ligne) - indexLigne;
            for ligneN in range(taille):
                ligne = ligne[:-1]

            writeTab = [[ligne + ';Eco'], [ligne + ';Affaire'], [ligne + ';First'], [ligne + ';Cargo']]

            # Line informations for each day
            demand = browser.find_element(by=By.ID, value='demand').text;
            index = [];
            index.append(demand.find('Lundi'));
            index.append(demand.find('Mardi'));
            index.append(demand.find('Mercredi'));
            index.append(demand.find('Jeudi'));
            index.append(demand.find('Vendredi'));
            index.append(demand.find('Samedi'));
            index.append(demand.find('Dimanche'));
            index.append(len(demand));

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

                Naffaire = P[3] - P[2]
                placeAffaire = ''
                for position in range(Naffaire - 1):
                    placeAffaire = placeAffaire + demand[P[2] + 1 + position]

                Nfirst = P[5] - P[4]
                placeFirst = ''
                for position in range(Nfirst - 1):
                    placeFirst = placeFirst + demand[P[4] + 1 + position]

                Ncargo = P[6] - P[5]
                placeCargo = ''
                for position in range(Ncargo - 1):
                    placeCargo = placeCargo + demand[P[6] + 1 + position]

                writeTab[0].append(';' + placeEco)
                writeTab[1].append(';' + str(placeAffaire))
                writeTab[2].append(';' + str(placeFirst))
                writeTab[3].append(';' + str(placeCargo))

            # Print on CSV
            for y in range(4):
                stringTest = []
                for z in range(8):
                    stringTest.append(writeTab[y][z])

                writer.writerow(stringTest)
        printProgressBar(avion + 1, len(nomAvion), prefix='Progress:', suffix='Complete', length=50)

browser.close()