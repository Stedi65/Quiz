# Programm.....: Quiz.py
# Programmierer: Giacomo Casale
#                Stephan Dick-Rustmeier
#                Sebastian Reisach
#                Stefan Serf
# Erstellt am..: 01.02.2021
# Änderung am..: 05.02.2020 Stephan Dick-Rustmeier
#              : Umstellung von CSV-Datei auf sqlite3-Datenbank
#              : Level eingeführt
#              : Gewinnsumme eingeführt
#              : Intro Sound wird nun abgespielt


import random
from os import system, name, path
import csv
from collections import namedtuple
import sqlite3
from time import sleep
import pygame


def intro():
    clear_screen()
    with open("intro.txt", "r") as fobj:
        text = fobj.read()
    print(text)
    sound_intro()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def clear_screen():
    """ clears the screen and put the cursor to position 0,0
    :param: none
    :return: none
    """
    system('cls' if name == 'nt' else 'clear')


def read_questions_from_db(level):
    vorlage = namedtuple('vorlage', ['frage', 'antworten', 'loesung'])
    datensatz = []
    conn = create_connection("german.db")
    cur = conn.cursor()
    sql = "SELECT * FROM questions WHERE level=" + str(level)
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        # print(row)
        frage = row[1]
        antworten = row[2:6]
        loesung = row[6]
        daten = vorlage(frage, antworten, loesung)
        datensatz.append(daten)
    conn.close()
    return datensatz


def question_choice(datensatz):
    randomQuestionNumber = random.randint(0, len(datensatz)-1)
    question = datensatz[randomQuestionNumber]
    return question, randomQuestionNumber


def answere_question(question):
    antwort = int(input())
    if antwort == question.loesung:
        print("Die Antwort ist richtig!")
        return True
    else:
        print("Die Antwort ist falsch!")
        print("Richtig ist: {}".format(question.loesung))
        return False


def print_question(question):
    print("+" + "-" * (len(question.frage)+4) + "+")
    print("|  " + question.frage + "  |")
    print("+" + "-" * (len(question.frage)+4) + "+")
    print("\n")
    for i in range(len(question.antworten)):
        print(str(i+1) + " " + question.antworten[i])
    print("\nDeine Antwort: ", end="")


def delete_question(datensatz, position):
    datensatz.pop(position)
    return datensatz


def gewinnermittlung(level, sicherheitsstufen, gewinnstufen):
    gewinn = gewinnstufen[level - 1]
    if level < sicherheitsstufen[0]:
        gewinn = 0
    if level > sicherheitsstufen[0] and level < sicherheitsstufen[1]:
        gewinn = gewinnstufen[sicherheitsstufen[0] - 1]
    if level > sicherheitsstufen[1]:
        gewinn = gewinnstufen[sicherheitsstufen[1] - 1]
    return gewinn


def check_sicherheitsstufe(level, sicherheitsstufen):
    ret = 0
    if level == sicherheitsstufen[0]:
        sound_sicherheitsstufe1()
        ret = 1
    if level == sicherheitsstufen[1]:
        sound_sicherheitsstufe2()
        ret = 2
    return ret

def sound_intro():
    play_sound("intro.mp3")


def sound_richtig():
    # play_sound("richtige_anwort.mp3")
    pass


def sound_falsch():
    # play_sound("falsche_anwort.mp3")
    pass


def sound_sicherheitsstufe1():
    play_sound("stufe1.mp3")
	
def sound_sicherheitsstufe2():
    play_sound("stufe2.mp3")	
		

def sound_gewonnen():
    # play_sound("gewonnen.mp3")
    pass


def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
# Main
go = True
max_level = 15
level = 1
sicherheitsstufe = 0
gewinnstufen = [50, 100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 500000, 1000000]
sicherheitsstufen = [5, 10]
waehrung = "€"
gewinn = 0

intro()

while level <= max_level and go:
    clear_screen()
    datensatz = read_questions_from_db(level)
    question, position = question_choice(datensatz)
    print(f"Level: {level} Stufe: {gewinnstufen[level - 1]} Gewinnsumme: {gewinn} {waehrung}")
    print("\n")
    print_question(question)
    result = answere_question(question)
    if result == False:
        gewinn = gewinnermittlung(level, sicherheitsstufen, gewinnstufen)
        print("Das war leider die falsche Antwort!")
        print(f"Sie haben {gewinn} {waehrung} gewonnen")
        sound_falsch()
        break
    if result:
        gewinn = gewinnermittlung(level, sicherheitsstufen, gewinnstufen)
        sicherheitsstufe = check_sicherheitsstufe(level, sicherheitsstufen)
        datensatz = delete_question(datensatz, position)
        level += 1
    go = result
    if level == max_level and result:
        print("Herzlichen Glückwunsch!!!!!")
        print("Sie haben alle Fragen erfolgreich beantwortet!")
        print(f"Sie haben {gewinn} {waehrung} gewonnen")
        
