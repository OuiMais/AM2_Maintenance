"""
    Projet : AM2_Auto / flightResult
    Date Creation : 07/12/2022
    Date Revision : 28/08/2023
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Recupere toutes les données des vols permettant de retirer les vols dont qui font perdre de l'argent
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time
import re


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


def final(anoter, volParDate, tableauDate):
    tampon = 0
    for journee in range(13):
        date = tableauDate[journee]
        tampon = tampon + volParDate[journee]
        for rangement in range(volParDate[journee + 1]):
            arentrer = anoter[tampon + rangement]
            espace = [0]
            text = []
            for rentrer in range(len(arentrer)):
                if arentrer[rentrer] == ' ':
                    espace.append(rentrer + 1)
            espace.append(len(arentrer))
            for talent in range(len(espace) - 1):
                string = ''
                for lettre in range(espace[talent + 1] - espace[talent]):
                    string = string + arentrer[espace[talent] + lettre]
                text.append(string)
            avion = text[0] + text[1] + text[2] + text[3]
            ligne = text[4] + text[5]
            heure = text[7]
            pax = text[8] + text[9]
            money = ''
            for dol in range(len(text) - 10):
                money = money+text[10 + dol]
                
            dollar = []
            for argent in range(len(money)):
                if money[argent] == '$':
                    dollar.append(argent)
                    
            CA = ''
            for echange in range(dollar[0]):
                if money[echange] != " ":
                    CA = CA+money[echange]

            res = ''
            for reachFinal in range(dollar[1]-dollar[0]-1):
                if money[dollar[0] + reachFinal + 1] != " ":
                    res = res+money[dollar[0] + reachFinal + 1]

            sortie.append(date+''+avion+''+ligne+''+heure+''+pax+''+CA+''+res+'')
            
    return sortie


# Option for website (no screen open)
options = Options()
options.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(options=options)

# Open the Website
browser.get('https://www.airlines-manager.com/network/showhub/6836614/flights')

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

sortie = []
tableauDate = []
volParDate = [0]
tampon = 0
with open('flightResult.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv)
    data = ['Jour Avion Ligne Depart/Arrivee Pax CA Resultats']
    writer.writerow(data)
    demand = ''
    iteration = 0
    printProgressBar(iteration, 14, prefix='Progress:', suffix='Complete', length=50)
    for tourner in range(3):
        browser.find_element(by=By.CLASS_NAME, value='silverArrowLeft').click()
        time.sleep(1)
    for jour in range(6, 0, -1):
        recherche = "//div[@class='blue' and 'J-" + str(jour) + "']"
        rechercheDate = "J-" + str(jour)
        rechercheData = browser.find_element(by=By.ID, value='showHubFlights').text

        date = ''
        dateJour = rechercheData.find(rechercheDate)
        for i in range(10):
            date = date + rechercheData[dateJour + 4+i]
        
        site = 'https://www.airlines-manager.com/network/showhub/6836614/flights?date=' + date
        browser.get(site)
        tableauDate.append(date)
        
        demand = demand+browser.find_element(by=By.ID, value='showHubFlights').text
        boucle = int(demand[len(demand)-6]) - 1
        
        for echo in range(boucle):
            site = 'https://www.airlines-manager.com/network/showhub/6836614/flights?date=' + date + '&page=' + str(echo+2)
            browser.get(site)
            time.sleep(2)
            demand = demand + browser.find_element(by=By.ID, value='showHubFlights').text
            
        result = [_.start() for _ in re.finditer('OMG-', demand)] 
        resultTot = [_.start() for _ in re.finditer('Total', demand)] 
        for retour in range(len(resultTot)-1):
            result.append(resultTot[retour])
        result.sort()
        
        anoter = []
        for t in range(len(result)-1):
            tps = result[t+1] - result[t]
            st = " "
            for tn in range(tps):
                st = st + demand[result[t]+tn]
            if len(st) < 100:
                anoter.append(st)
        
        tps = resultTot[len(resultTot)-1] - result[len(result)-1]
        st = ' '
        
        for tn in range(tps):
            st = st + demand[result[len(result)-1]+tn]
        if len(st) < 100:
            anoter.append(st)
        tampon = tampon + volParDate[len(volParDate)-1]
        volParDate.append(len(anoter)-tampon)
        iteration = iteration + 1
        printProgressBar(iteration, 14, prefix='Progress:', suffix='Complete', length=50)
        
    recherche = "//div[@class='blue' and 'Aujourd'hui]"
    rechercheDate = "AUJOURD'HUI"
    rechercheData = browser.find_element(by=By.ID, value='showHubFlights').text

    date = ''
    dateJour = rechercheData.find(rechercheDate)
    for i in range(10):
        date = date + rechercheData[dateJour + 12+i]
    
    site = 'https://www.airlines-manager.com/network/showhub/6836614/flights?date=' + date
    browser.get(site)
    tableauDate.append(date)
    
    demand = demand+browser.find_element(by=By.ID, value='showHubFlights').text
    boucle = int(demand[len(demand)-6]) - 1
    
    for echo in range(boucle):
        site = 'https://www.airlines-manager.com/network/showhub/6836614/flights?date=' + date + '&page=' + str(echo+2)
        browser.get(site)
        time.sleep(2)
        demand = demand + browser.find_element(by=By.ID, value='showHubFlights').text
        
    result = [_.start() for _ in re.finditer('OMG-', demand)] 
    resultTot = [_.start() for _ in re.finditer('Total', demand)] 
    for retour in range(len(resultTot) - 1):
        result.append(resultTot[retour])
    result.sort()
    
    anoter = []
    for t in range(len(result) - 1):
        tps = result[t+1] - result[t]
        st = ' '
        for tn in range(tps):
            st = st + demand[result[t]+tn]
        if len(st) < 100:
            anoter.append(st)
    
    tps = resultTot[len(resultTot) - 1] - result[len(result) - 1]
    st = " "
    for tn in range(tps):
        st = st + demand[result[len(result) - 1] + tn]
    if len(st) < 100:
        anoter.append(st)
    tampon = tampon + volParDate[len(volParDate) - 1]
    volParDate.append(len(anoter)-tampon)

    iteration = iteration + 1
    printProgressBar(iteration, 14, prefix='Progress:', suffix='Complete', length=50)
    
    for tourner in range(3):
        browser.find_element(by=By.CLASS_NAME, value='silverArrowRight').click()
        time.sleep(1)
    for jour in range(1, 7, +1):
        recherche = "//div[@class='blue' and 'J-" + str(jour) + "']"
        rechercheDate = "J+" + str(jour)
        rechercheData = browser.find_element(by=By.ID, value='showHubFlights').text

        date = ''
        dateJour = rechercheData.find(rechercheDate)
        for i in range(10):
            date = date + rechercheData[dateJour + 4+i]
        
        site = 'https://www.airlines-manager.com/network/showhub/6836614/flights?date=' + date
        browser.get(site)
        tableauDate.append(date)
        
        demand = demand+browser.find_element(by=By.ID, value='showHubFlights').text
        boucle = int(demand[len(demand)-6]) - 1
        
        for echo in range(boucle):
            site = 'https://www.airlines-manager.com/network/showhub/6836614/flights?date=' + date + '&page=' + str(echo+2)
            browser.get(site)
            time.sleep(2)
            demand = demand + browser.find_element(by=By.ID, value='showHubFlights').text
            
        result = [_.start() for _ in re.finditer('OMG-', demand)] 
        resultTot = [_.start() for _ in re.finditer('Total', demand)] 
        for retour in range(len(resultTot)-1):
            result.append(resultTot[retour])
        result.sort()
        
        anoter = []
        for t in range(len(result)-1):
            tps = result[t+1] - result[t]
            st = " "
            for tn in range(tps):
                st = st + demand[result[t]+tn]
            if len(st) < 100:
                anoter.append(st)
        
        tps = resultTot[len(resultTot)-1] - result[len(result)-1]
        st = ' '
        for tn in range(tps):
            st = st + demand[result[len(result)-1]+tn]
        if len(st) < 100:
            anoter.append(st)
        tampon = tampon + volParDate[len(volParDate)-1]
        volParDate.append(len(anoter)-tampon)
        iteration = iteration + 1
        printProgressBar(iteration, 14, prefix='Progress:', suffix='Complete', length=50)

    final(anoter, volParDate, tableauDate)
    for out in range(len(sortie)):
        writer.writerow(sortie[out])

time.sleep(5)
browser.close()
