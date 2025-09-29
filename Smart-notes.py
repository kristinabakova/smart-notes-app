# Spustenie je v terminale 
# cd cesta-k-suboru
# python3 nazov-suboru.py

# importovanie potrebnych kniznic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QMessageBox
import json

app = QApplication([]) # inicializacia aplikacie

# nacitanie ulozenych poznamok zo suboru, alebo vytvorenie noveho suboru, ak neexistuje
try:
    with open("notes_data.json", "r", encoding='utf-8') as file:
        notes = json.load(file)
except FileNotFoundError:
    notes = {
        "Welcome!": {
            "text": "This is the best note taking app in the world!",
            "tags": ["good", "instructions"]
        }
    } # prednastavena poznamka
    # ulozenie prednastavenej poznamky do suboru
    with open("notes_data.json", "w", encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False)

# vytvorenie hlavneho okna aplikacie
notes_win = QWidget()
notes_win.setWindowTitle('Smart Notes')
notes_win.resize(900, 600)

# vytvorenie zoznamu poznamok a popisu
list_notes = QListWidget()
list_notes_label = QLabel('List of notes')

# vytvorenie tlacidiel na spravu poznamok
button_note_create = QPushButton('Create note')
button_note_del = QPushButton('Delete note')
button_note_save = QPushButton('Save note')

# pole na zadavanie tagov a textova oblast pre obsah poznamok
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')
field_text = QTextEdit()

# tlacidla na spravu tagov
button_add = QPushButton('Add to note')
button_del = QPushButton('Untag from note')
button_search = QPushButton('Search notes by tag')

# zoznam tagov a popis
list_tags = QListWidget()
list_tags_label = QLabel('List of tags')

# rozvrhnutie okna - hlavne rozlozenie a rozdelenie na stlpce
layout_notes = QHBoxLayout()

# stlpec pre obsah poznamky
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

# stlpec pre zoznam poznamok a tagov
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

# rozlozenie pre tlacidla na spravu poznamok
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

# pridanie zoznamu tagov a ich spravy
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_add)
row_3.addWidget(button_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

# spojenie stlpcov do hlavneho rozlozenia
layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

current_note = None # globalna premenna pre aktualnu poznamku

def add_note():
    """
    funkcia na pridanie novej poznamky
    """
    global current_note  # deklarujeme globalnu premennu pre aktualnu poznamku
    note_name, ok = QInputDialog.getText(notes_win, "Add note", "Note name: ")  # zobrazenie dialogu na zadanie nazvu poznamky
    if ok and note_name != "":  # kontrola, ci bol zadany platny nazov
        if note_name in notes:  # kontrola, ci uz existuje poznamka s rovnakym nazvom
            QMessageBox.warning(notes_win, "Warning", "Note with this name already exists!")  # upozornenie na duplicitny nazov
        else:
            notes[note_name] = {"text": "", "tags": []}  # vytvorenie novej poznamky
            list_notes.addItem(note_name)  # pridanie do zoznamu poznamok
            list_notes.setCurrentItem(list_notes.findItems(note_name, Qt.MatchExactly)[0]) # nastavenie novej poznamky ako vybranej
            list_tags.clear()  # vycistenie zoznamu tagov
            field_text.clear()  # vycistenie textoveho pola
            with open("notes_data.json", "w", encoding='utf-8') as file: # aktualizacia suboru s poznamkami
                json.dump(notes, file, ensure_ascii=False)
            current_note = note_name  # nastavenie novej poznamky ako aktualnej

def show_note():
    """
    funkcia na zobrazenie vybranej poznamky
    """
    global current_note
    if not save_changes_warning(): # kontrola na neulozenej zmeny
        return
    current_note = list_notes.selectedItems()[0].text()  # ziskanie nazvu vybranej poznamky
    field_text.setText(notes[current_note]["text"])  # nastavenie textu do textoveho pola
    list_tags.clear()  # vycistenie zoznamu tagov
    list_tags.addItems(notes[current_note]["tags"])  # pridanie tagov vybranej poznamky

def save_note():
    """
    funkcia na ulozenie aktualnej poznamky
    """
    if list_notes.selectedItems(): # kontrola, ci je vybrana poznamka
        key = list_notes.selectedItems()[0].text() # ziskanie nazvu vybranej poznamky
        notes[key]["text"] = field_text.toPlainText() # ulozenie textu do slovnika
        with open("notes_data.json", "w", encoding='utf-8') as file: # aktualizacia suboru s poznamkami
            json.dump(notes, file, ensure_ascii=False)
    else:
        QMessageBox.warning(notes_win, "Warning", "Note to save is not selected!") # upozornenie, ak nie je vybrana poznamka

def del_note():
    """
    funkcia na odstranenie vybranej poznamky
    """
    global current_note
    if list_notes.selectedItems(): # kontrola, ci je vybrana poznamka
        key = list_notes.selectedItems()[0].text() # ziskanie nazvu vybranej poznamky
        confirm = QMessageBox.question(notes_win, "Confirm delete", f"Do you really want to delete the note '{key}'?") # zobrazenie dialogu na potvrdenie zmazania
        if confirm == QMessageBox.Yes: # ak je potvrdene
            del notes[key] # odstranenie poznamky zo slovnika
            list_notes.clear() # vycistenie zoznamu poznamok
            list_tags.clear() # vycistenie zoznamu tagov
            field_text.clear() # vycistenie textoveho pola
            list_notes.addItems(notes) # obnovenie zoznamu poznamok
            with open("notes_data.json", "w", encoding='utf-8') as file: # aktualizacia suboru s poznamkami
                json.dump(notes, file, ensure_ascii=False)
            current_note = None # reset aktualnej poznamky
    else:
        QMessageBox.warning(notes_win, "Warning", "Note to delete is not selected!") # upozornenie, ak nie je vybrana poznamka

def add_tag():
    """
    funkcia na pridanie tagu k vybranej poznamke
    """
    if list_notes.selectedItems(): # kontrola, ci je vybrana poznamka
        key = list_notes.selectedItems()[0].text() # ziskanie nazvu vybranej poznamky
        tag = field_tag.text() # ziskanie zadaneho tagu
        if tag and tag not in notes[key]["tags"]: # kontrola, ci je tag platny a novy
            notes[key]["tags"].append(tag)  # pridanie tagu do zoznamu
            list_tags.addItem(tag) # zobrazenie tagu v zozname
            field_tag.clear() # vycistenie vstupneho pola
            with open("notes_data.json", "w", encoding='utf-8') as file: # aktualizacia suboru s poznamkami
                json.dump(notes, file, ensure_ascii=False)
    else:
        QMessageBox.warning(notes_win, "Warning", "Note to add a tag is not selected!") # upozornenie, ak nie je vybrana poznamka

def del_tag():
    """
    funkcia na odstranenie vybraneho tagu z poznamky
    """
    if list_tags.selectedItems(): # kontrola, ci je vybrany tag
        key = list_notes.selectedItems()[0].text() # ziskanie nazvu vybranej poznamky
        tag = list_tags.selectedItems()[0].text() # ziskanie vybraneho tagu
        notes[key]["tags"].remove(tag) # odstranenie tagu zo zoznamu
        list_tags.clear() # vycistenie zoznamu tagov
        list_tags.addItems(notes[key]["tags"]) # obnovenie zoznamu tagov
        with open("notes_data.json", "w", encoding='utf-8') as file: # aktualizacia suboru s poznamkami
            json.dump(notes, file, ensure_ascii=False)
    else:
        QMessageBox.warning(notes_win, "Warning", "Tag to delete is not selected!") # upozornenie, ak nie je vybrany tag

def search_tag():
    """
    funkcia na vyhladavanie poznamok podla tagu
    """
    tag = field_tag.text() # ziskanie zadaneho tagu
    if button_search.text() == "Search notes by tag" and tag: # kontrola, ci je stav vyhladavania a ci je zadany tag
        notes_filtered = {} # vytvorenie noveho slovnika pre filtrovanie
        for note in notes: # iteracia cez vsetky poznamky
            if tag in notes[note]["tags"]: # ak poznamka obsahuje zadany tag
                notes_filtered[note] = notes[note] # pridanie poznamky do filtrovaneho slovnika
        button_search.setText("Reset search") # nastavenie tlacidla na reset
        list_notes.clear() # vycistenie zoznamu poznamok
        list_tags.clear() # vycistenie zoznamu tagov
        list_notes.addItems(notes_filtered)  # zobrazenie filtrovanych poznamok
    elif button_search.text() == "Reset search": # ak je tlacidlo nastavené na reset
        field_tag.clear() # vycistenie vstupneho pola
        list_notes.clear() # vycistenie zoznamu poznamok
        list_tags.clear() # vycistenie zoznamu tagov
        list_notes.addItems(notes) # obnovenie povodnych poznamok
        button_search.setText("Search notes by tag") # nastavenie tlacidla na vyhladavanie

def save_changes_warning():
    """
    funkcia na upozornenie na nesaveovane zmeny
    """
    global current_note  # globalna premenna pre aktualnu poznamku
    if current_note and field_text.toPlainText() != notes[current_note]["text"]: # kontrola, ci su neulozene zmeny
        confirm = QMessageBox.question(notes_win, "Unsaved changes", f"Do you want to save changes to '{current_note}'?") # zobrazenie dialogu na potvrdenie ulozenia zmien
        if confirm == QMessageBox.Yes: # ak je potvrdene ulozenie
            notes[current_note]["text"] = field_text.toPlainText()  # ulozenie textu do slovnika
            with open("notes_data.json", "w", encoding='utf-8') as file: # aktualizacia suboru s poznamkami
                json.dump(notes, file, ensure_ascii=False)
        elif confirm == QMessageBox.Cancel: # ak je zrusene ulozenie
            return False
    return True

# prepojenie tlacidiel s funkciami
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_add.clicked.connect(add_tag)
button_del.clicked.connect(del_tag)
button_search.clicked.connect(search_tag)

# pridanie existujucich poznamok do zoznamu
list_notes.addItems(notes)

# zobrazenie okna aplikacie
notes_win.show()
app.exec_()