import pandas as pd
import string
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
import os

# Sets the nltk data path depending on where this application is saved on the users' machine
cwd = os.getcwd()
nltk_data_directory = cwd
nltk_data_directory += "\\nltk_data"

nltk.data.path.append(nltk_data_directory)

def removePunctuation(text):
    
    """
    Input: text (string)

    Returns: string with no punctuation
    """

    no_punct_list = [char for char in text if char not in string.punctuation]
    no_punct_string = ''.join(no_punct_list)
    return no_punct_string

def clean(text):

    """
    Input: text (string)

    Removes punctuation and special characters from string
    and converts it to lower case

    Returns cleaned text (string)

    """
    if isinstance(text,str):
        text = removePunctuation(text)
        text = text.lower()
        text = word_tokenize(text)
        return ' '.join(text)
    

def preProcessText(df,text_col_name):

    """
    Input: pandas dataframe containing the read in CSV file (df)
           the name of the column containing the raw free text (text_col_name)
    
    For each entry in the data frame, it cleans the text in the free_text cell.
    The full list of cleaned text is then added as a new column of the dataframe
    as "cleaned_txt"

    Returns: the dataframe with the new "cleaned_txt" column

    """

    proccesed_list = []
    for _,row in df.iterrows():
        proccesed_list.append(clean(row[text_col_name]))
    
    df["cleaned_txt"] = proccesed_list
    return df


def findPhraseInText(phrase, window, df, query_list):

    """
    Input phrase (string): the phrase to be searched in text 
          window (int): how many words either side of the phrase to display
          df (pd dataframe): contains the dataframe with the free text
          query_list (list): contains the additional information to be returned along with the text

    Searches the cleaned_text for the phrase (exact matches only)

    Returns the found text plus additional queries about that user (if any)

    """

    for _,row in df.iterrows():
        current_txt = row["cleaned_txt"]
        print_str, new_txt = getPhraseInString(current_txt,phrase,window)

        if print_str == "":
            continue
        
        occurence_found = True

        # If button pressed again
        if new_txt != "finish":
            print_str, new_txt = getPhraseInString(new_txt,phrase,window)

        while(new_txt!= "finish"):
            
            print_str,new_txt = getPhraseInString(new_txt,phrase,window)



def getPhraseInString(text,phrase,window):
    
    if not isinstance(text,str):
        return "","finish"
    
    start_pos = text.find(phrase)

    if start_pos == -1:
        return "","finish"
    
    start,_,end_str = text.partition(phrase)
    f1 = False
    f2 = False

    if start == "":
        f1 = True
        start=[""]
    else:
        start = word_tokenize(start)

    if end_str == "":
        f2 = True
        end = [""]
    else:
        end = word_tokenize(end_str)
    
    phrase = word_tokenize(phrase)

    start_len = len(start)
    end_len = len(end)

    if start_len <= window:
        f1 = True
    if end_len <= window:
        f2 = True
    
    if f1 and f2:
        start += phrase+end
    elif f1:
        end = end[:window]
        start += phrase+end
    elif f2:
        start = start[-window:]
        start += phrase+end
    else:
        start = start[-window:]
        end = end[:window]
        start += phrase+end
    
    print_str = " ".join(start)

    return print_str,end_str



        
    





