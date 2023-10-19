

import re
import json
import zipfile 
import nltk

# Download punkt plugin for NLTK
nltk.download('punkt')

# Open source text data - saved as 'sherlock.txt'
# Use NLTK to put it into a list of sentences
with open('sherlock.txt', 'r') as trainingfile:
    trainingdata = trainingfile.read()
    sentences = nltk.sent_tokenize(trainingdata)


# Perform a regex on all sentences to pull out 'useful' sentences which are up to 140 characters in length 
# then strip out all non-alphanumeric characters
shortSentences = []
cleanSentences = []

# match the start of a sentence ('\A') and only alphanumeric symbols '\w' then continue until end
for text in sentences:    
    shortSentences += re.findall('\A\w.+$', text[0:141])

# remove all non alphanumeric characters that may appear
stripChar = '\"\'\.\?\,\!-()'
for s in shortSentences:
    cleanSentences.append(s.translate(str.maketrans("", "", stripChar)))

# Create a list containing only sentences which are greater than 5 words in length
slotEntries = []
nWords = 5
for e in cleanSentences:
    if (len(e.split()) > nWords):
        slotEntries.append(e)

# Create the zipped json file to import into Lex as the slot training data
lexSlotTextFile = 'trainingText.json'
lexSlotZipFile = 'trainingText.zip'
data = {
  "metadata": {
    "schemaVersion": "1.0",
    "importType": "LEX",
    "importFormat": "JSON"
  },
  "resource": {
    "description": "Training text input for custom free flow slot",
    "name": "trainingText",
    "version": "1",
    "enumerationValues": [],
    "valueSelectionStrategy": "ORIGINAL_VALUE"
  }
} 

# populate json with slot values
for slot in slotEntries:  
    data["resource"]["enumerationValues"].append({"value": slot})

# write the json file with the data
with open (lexSlotTextFile, 'w') as f:
    json.dump(data, f)
f.close()

# zip up file ready for import to Lex
with zipfile.ZipFile(lexSlotZipFile, 'w') as myzip:
    myzip.write(lexSlotTextFile)
myzip.close()

print ("Created json zip file for Lex Slot Import as", lexSlotZipFile)