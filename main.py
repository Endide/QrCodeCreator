import qrcode
import sys
import pandas as pd
import json

FILL_COLOR = 'black'
BACKGROUND_COLOR = 'white'
VERSION = 1
BOX_SIZE = 10
BORDER = 4
ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_L


def get_error_correction_level(error_correction_level):
    if error_correction_level == 'L':
        return qrcode.constants.ERROR_CORRECT_L
    elif error_correction_level == 'M':
        return qrcode.constants.ERROR_CORRECT_M
    elif error_correction_level == 'Q':
        return qrcode.constants.ERROR_CORRECT_Q
    elif error_correction_level == 'H':
        return qrcode.constants.ERROR_CORRECT_H
    else:
        return qrcode.constants.ERROR_CORRECT_L

def create_qr(text, filename):
    qr = qrcode.QRCode(
        version=VERSION,
        error_correction=ERROR_CORRECTION,
        box_size=BOX_SIZE,
        border=BORDER,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=FILL_COLOR, back_color=BACKGROUND_COLOR)
    img.save('qrcode/' + filename + '.png')
    print("Creation du QrCode " + text + " terminée")


def generateTable_qr(file, type, columnName, columnText, SheetName):
    count = 0
    if type == "xlsx":
        df = pd.read_excel(file, sheet_name=SheetName)
        for i in df.index:
            print("Génération du QrCode " + "" + ": " + str(count) + " / " + str(len(df.index)))
            create_qr(df[columnText][i], df[columnName][i])
            count += 1
    elif type == "csv":
        df = pd.read_csv(file)
        for i in df.index:
            print("Génération du QrCode " + "" + ": " + str(count) + " / " + str(len(df.index)))
            create_qr(df[columnText][i], df[columnName][i])
            count += 1



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Bienvenue dans le créateur de QR code")
        mode = input("Voulez-vous créer un seul QR code ou Plusieurs QR code ? (1/2) ")
        if mode == "1":
            base = input("Voulez-vous utiliser les paramètres par défaut ou choisir chaque paramètres ? (1/2) ")
            if base == "1":
                text = input("Veuillez entrer le texte à convertir en QR code : ")
                create_qr(text, "result")
            if base == "2":
                text = input("Veuillez entrer le texte à convertir en QR code : ")
                FILL_COLOR = input("Veuillez entrer la couleur de remplissage du QR code : ")
                BACKGROUND_COLOR = input("Veuillez entrer la couleur de fond du QR code : ")
                VERSION = input("Veuillez entrer la version du QR code : ")
                BOX_SIZE = input("Veuillez entrer la taille des cases du QR code : ")
                BORDER = input("Veuillez entrer la taille du bord du QR code : ")
                create_qr(text, "result")
        if mode == "2":
            type = input("Quel est le type de fichier contenant les données ? (XLSX/JSON/CSV) ")
            if type.lower() == "xlsx" or type.lower() == "csv":
                file = input("Veuillez entrer le chemin du fichier contenant les données : ")
                sheetName = input("Veuillez entrer le nom de la feuille CSV : ")
                columnName = input("Veuillez entrer le nom de la colonne contenant les noms : ")
                columnText = input(
                    "Veuillez entrer le nom de la colonne contenant les textes à convertir en QR code : ")
                generateTable_qr(file, type.lower(), columnName, columnText, sheetName)

    else:
        file = sys.argv[1]
        data = open(file)
        config = json.load(data)
        print("Génération des QR codes d'après la configuration")
        VERSION = str(config.get("version"))
        BOX_SIZE = str(config.get("box-size"))
        BORDER = str(config.get("border"))
        FILL_COLOR = config.get("fill-color")
        BACKGROUND_COLOR = config.get("background-color")
        ERROR_CORRECTION = get_error_correction_level(config.get("error-correction"))
        if(config.get("mode") == "direct"):
            create_qr(config.get("text"), "result")
        if(config.get("mode") == "multiple"):
            if(config.get("storage") == "xlsx" or config.get("storage") == "csv"):
                generateTable_qr(config.get("file"), config.get("storage"), config.get("tableSetting")["Name"], config.get("tableSetting")["Text"], config.get("tableSetting")["Sheet"])
            if(config.get("storage" == "json")):
                print("Implementation en cours")