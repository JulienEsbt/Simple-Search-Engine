#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 7 07:54:41 2022

@author: ESTERBET Julien and LEGEARD Hugo
"""

import csv
import re
from math import log
import webbrowser
from tkinter import * 

# Open the CSV file
doc = open('/Users/julienesbt/Documents/Etudes/M1/BDA/TP/TP1/TED_transcripts.csv', 'r')
# doc = open('/Users/hugolegeard/Downloads/Fac/M1_EIT/S7/BDA/TP/TED_transcripts.csv', 'r')

########################## Initialisation Interface Graphique ##########################

#Creation of the graphic interface
root = Tk()

#ScrollBar creation
scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill = Y )

#Label Creation 
L1 = Label(root, text="Your keywords : ")
L1.pack( side = LEFT)

#Entry to enter and get the keywords
keywords = StringVar()
keywordInput = Entry(root, textvar=keywords, bd = 5)
keywordInput.pack(side = LEFT)

########################## Fonctions ##########################

def csv_to_dict(csv_file) :
    """Fonction that transform the CSV file to a Dictionnary with the keys as the Transcript and the value as the url (mapping { Transcript --> Url })"""
    myDict = {} 
    with csv_file as infile:
        reader = csv.reader(infile)
        next(reader, None) 
        myDict = {rows[0] : rows[1] for rows in reader}
    return myDict

# Three fonctions that create 3 differents indexs
def index_words_to_urls(dico) :
    """Create an index { words --> Urls }"""
    res = {}
    # For loop to go through the mapping of the csv file. 
    for key, value in dico.items() :
        # Regex use to delete symbols that we don't want and to put every word in lower case.
        pattern = re.compile('\W+')
        val = key
        val = re.sub(pattern, ' ', val)
        val = val.lower()
        # Loop that go through every single word of the key (the transcript)
        for word in val.split() :
            # Add the word and the url if the word is not already in the dict.
            if word not in res :
                res[word] = [value]
            # Add the url to the list of url associate to the word.
            elif value not in res[word] :
                res[word].append(value)
    return res

def index_words_to_idf(index1) : 
    """Create an index { words --> IDF }"""
    idf = {}
    length = len(index1)
    # In here we go through the whole index1, and calculate the IDF score with it.
    for key, value in index1.items() : 
        idf[key] = log(length / len(value))
    return idf

def index_urls_to_words(dico) :
    """Create an index { Urls --> { Words --> TF } }"""
    res = {}
    # Same as the first index for the beginning
    for key, value in dico.items() :
        tab = {}
        pattern = re.compile('\W+')
        val = key
        val = re.sub(pattern, ' ', val)
        val = val.lower()
        length = len(val.split())
        # Loop in which we do the mapping { Word --> Number of Occurence }
        for word in val.split() :
            if word not in tab :
                tab[word] = 1
            else : 
                tab[word] += 1
        # Loop in which we divide by the length to have the TF score
        for x in tab : 
            tab[x] = tab[x]/length
        # We here map the mapping we just created to the Url
        res[value] = tab
    return res

def find_a_word(index1, index2, index3, wordToFind) :
    """Return a dict { Url --> Tf-Idf score }"""
    res = {}
    if wordToFind in index1 :
        urls = index1[wordToFind]
        idf = index2[wordToFind]
        # Loop to go through all the urls that contains the wordToFind
        for x in urls : 
            # Loop to go through the index3 that contains TF score
            for key, value in index3.items() :
                if key == x :
                    # Add the url as a key and calcul the Tf-Idf Score to add it as a value
                    res[key] = value[wordToFind]*idf
    # If the word is not in the CSV file
    else : 
        res[wordToFind] = 'This word is not in the database'
    return res

def find_some_words(index1, index2, index3) :
    """Take an input of some words and call the previous function so return a dict of a dict { word --> { Url --> Tf-Idf score } }"""
    # Input for the words you want to search for
    inputWordsToFind = input("Entrer les mots que vous recherchez : ")
    res = {}
    # Separate the words and put them in lower case
    setWordsToFind = inputWordsToFind.lower().split()
    # For each word, call the previous fonction and add the result on a mapping word --> res
    for x in setWordsToFind :
        res[x] = find_a_word(index1, index2, index3, x)
    return res

def intersection_of_results(dico) :
    """Dico is the result of the previous function, this one return the intersection of all the url associated with all the keywords"""
    n = 0
    tab = {}
    res = {}
    for key, value in dico.items() : 
        # If there is only one word as a result of the previous function 
        if len(dico) == 1 : 
            res = value
        # Add to tab the value of the first key (word)
        elif n == 0 :
            res = value
            n = 1
        # Do the intersection of the values from two words (as the dict is bigger than one)
        else : 
            tab = dict(res)
            res.clear()
            for keyBis, valueBis in value.items() : 
                if keyBis in tab : 
                    x = tab[keyBis] + valueBis
                    # Check if the final score is over 0.0025, if yes, do an addition of the Tf-Idf scores from both
                    if x >= 0.0025 : 
                        res[keyBis] = x
    return sorted(res.items(), key=lambda x: x[1], reverse=True)

########################## Fonction de l'Interface Graphique ######################

#Check if it's an url and open the link when you click on it
def weblink(*args):
    index = lb.curselection()[0]
    item = lb.get(index)
    if 'https://' in item:
        webbrowser.open_new(item)
        
#Insert The url in the list
def printUrl(): 
    tupleUrlTFIDF = intersection_of_results(find_some_words(index1, index2, index3))
    listeUrl = []
    for tupleUrl in tupleUrlTFIDF :
        listeUrl.append(tupleUrl[0])
        
    for url in listeUrl :
        url = url.rstrip('\n')
        lb.insert(END, url)
        
#Clear the list and the input entry
def deleteUrl() :
    lb.delete(0, END)
    keywordInput.delete(0, END)
    
########################## Main ##########################

dictionnaire = csv_to_dict(doc)
print('Index charging...')
index1 = index_words_to_urls(dictionnaire)
index2 = index_words_to_idf(index1)
index3 = index_urls_to_words(dictionnaire)
print('Index charged.')
print(intersection_of_results(find_some_words(index1, index2, index3)))

########################## Fin Initialisation Interface Graphique ##########################

#Creation of a button that will submit the keywords
button= Button(root, text="Enter", command= printUrl)
button.pack(side = LEFT)

buttonDelete = Button(root, text="Do another research", command= deleteUrl)
buttonDelete.pack(side=LEFT)


#Creation of a ListBox where all the urls will be
lb = Listbox(root,  yscrollcommand = scrollbar.set)
lb.bind('<<ListboxSelect>>', weblink)
lb.pack(fill=BOTH, expand=True)
     
root.mainloop()