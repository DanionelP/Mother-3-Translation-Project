import ast, os
from enum import Enum


#variables and shit
SAMEWORD = {}
BETWEENWORDS = {}
DOT = "•"
Directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
#Directory = "."
Type = None
UTF8FILES = ["script.txt", "0-8E.txt", "0-15E.txt", "0-16E.txt", "0-41E.txt", "0-42E.txt"]
SMALLFONTFILES = ["charnames.txt", "defaultnames.txt", "enemydescriptions.txt", "enemynames_short.txt"]
SMALLFONTEXCEPTIONS = "j"
class SubstitutionType(Enum):
    NORMAL = 1
    FORMATTED = 2


#functions and shit
def create_dict_from_file(fileName):
    dictionary = {}
    with open(fileName, 'r', encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split(':')
            dictionary[key] = ast.literal_eval(value)
    return dictionary

def do_replacement(line, smallFont=False):
    for key, value in SAMEWORD.items():
        for i in value[1]:
            if smallFont and i in SMALLFONTEXCEPTIONS: #perdón pero es que no estaba funcionando como quería y no quería romperme tanto el coco
                pass
            else:
                normal = str(key + i)
                formatted = str(value[0] + i)
                if Type == SubstitutionType.NORMAL:
                    line = line.replace(formatted, normal)
                elif Type == SubstitutionType.FORMATTED:
                    line = line.replace(normal, formatted)
    for key, value in BETWEENWORDS.items():
        for i in value:
            normal = str(key + " " + i)
            formatted = str(key + DOT + i)
            if Type == SubstitutionType.NORMAL:
                line = line.replace(formatted, normal)
            elif Type == SubstitutionType.FORMATTED:
                line = line.replace(normal, formatted)
    return line

def substitute(line, smallFont=False):
    global Type
    if "[ALTERNATEFONT]" in line:
        parts = line.split('[ALTERNATEFONT]')
        return do_replacement(parts[0]) + '[ALTERNATEFONT]' + parts[1]
    if line[0] == "/":
        return line
    return do_replacement(line, smallFont)

def replaceFile(fileName):
    realFile = Directory + "//" + fileName
    try:
        with open(realFile, 'r', encoding=set_file_type(fileName)) as skibidi:
            texto = skibidi.readlines()
            for line in texto:
                texto[texto.index(line)] = substitute(line, fileName in SMALLFONTFILES)
            newText = "".join(texto)
        with open(realFile, 'w', encoding=set_file_type(fileName)) as textFile:
            textFile.write(newText)
    except Exception as e:
        print(f"Error processing file {fileName}: {e}")

def set_substitution_type():
    elpepe = input("¿Quieres normalizar el texto (N) o formatearlo (F)?")
    global Type
    if elpepe in ["N", "n"]:
        Type = SubstitutionType.NORMAL
    elif elpepe in ["F", "f"]:
        Type = SubstitutionType.FORMATTED
    else:
        print("ira yo ya me via cagá en to tu muerto sunormá ponlo bien")
        set_substitution_type()

def set_file_type(fileName):
    return "utf-8" if fileName in UTF8FILES else "windows-1252"

def add_sameword_characters():
    for key, value in SAMEWORD.items():
        for i in value[1]:
            if i in SAMEWORD.keys():
                SAMEWORD[key][1].append(SAMEWORD[i][0])
    for key, value in BETWEENWORDS.items():
        for i in value:
            if i in SAMEWORD.keys():
                BETWEENWORDS[key].append(SAMEWORD[i][0])


#shit and shit
set_substitution_type()
SAMEWORD = create_dict_from_file("sameword.txt")
BETWEENWORDS = create_dict_from_file("betweenwords.txt")
add_sameword_characters()
for file in os.listdir(Directory):
    fileExtension = os.path.splitext(file)[1]
    if fileExtension == ".txt" and file not in ["texttable.txt", "M3FontEditor.txt"]:
        replaceFile(file)
        print("Se ha hecho el reemplazo en " + file)
os.system('pause')