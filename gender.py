# file that creates a model for genders based on the two features
# Last letter of name vowel
# Last two letters: VV VC CC CV
# 5 column vector with 1 extra field for M/F binary representation
# <VV, VC, CC, CV, V/C, M/F>
from __future__ import division
import sys

def reformat_training_txt():
    
    f = open("babynames.txt")
    for line in f.readlines():
        oldPos = 0;
        yearPos = line.find("2008", oldPos)
        while (yearPos != -1):
            oldPos = yearPos + 2
            line = line[:yearPos] + "\n" + line[yearPos:]
            yearPos = line.find("2008", oldPos)
        print line

def isVowel(char):
    return char.lower() in 'aeiouy'

def create_model():
    
    # reads in formatted training text and outputs a file with the
    # model matrix in its place
    # Row format: VV, VC, CC, CV, V/C (Last), M/F>
    
    f = open("babynames-formatted.txt")
    for line in f.readlines():
        split = line.split()
        if len(split) != 5:
            continue
        isMale = 1 if split[1] == "MALE" else 0
        name = split[2]
        (vv, vc, cc, cv, vowelEnding) = construct_vector(name)
        print name + ", " + str(vv) + ", " + str(vc) + ", " + str(cc) + ", " + str(cv) + ", " + str(vowelEnding) + ", " + str(isMale)
        
def construct_vector(name):
    vv = 1 if isVowel(name[len(name) - 2]) and isVowel(name[len(name) - 1]) else 0
    vc = 1 if isVowel(name[len(name) - 2]) and not isVowel(name[len(name) - 1]) else 0
    cc = 1 if not isVowel(name[len(name) - 2]) and not isVowel(name[len(name) - 1]) else 0
    cv = 1 if not isVowel(name[len(name) - 2]) and isVowel(name[len(name) - 1]) else 0
    vowelEnding = 1 if isVowel(name[len(name) - 1]) else 0
    
    return (vv, vc, cc, cv, vowelEnding)
    
def get_all_vectors(array, position, value):
    # return all the vectors that have the given value in the given position
    retArray = []
    for t in array:
        if int(t[position]) == value:
            retArray.append(t)
    
    return retArray

def run_program(model):
    new = raw_input("Enter a name for classification: ")
    
    # vectorize the name
    vectorTuple = construct_vector(new)
    
    # classify male / female based on bayes_naiive classifier techniques
    allMaleVectors = get_all_vectors(model, 5, 1)
    maleVectorLen = len(allMaleVectors)
    probMale = len(allMaleVectors) / len(model)
    
    # calculate the probability for each field
    allVVInMale = get_all_vectors(allMaleVectors, 0, vectorTuple[0])
    allVCInMale = get_all_vectors(allMaleVectors, 1, vectorTuple[1])
    allCCInMale = get_all_vectors(allMaleVectors, 2, vectorTuple[2])
    allCVInMale = get_all_vectors(allMaleVectors, 3, vectorTuple[3])
    allVoCInMale = get_all_vectors(allMaleVectors, 4, vectorTuple[4])
    
    field_product = (len(allVVInMale) / maleVectorLen) * (len(allVCInMale) / maleVectorLen) * (len(allCCInMale) / maleVectorLen)
    field_product = field_product * (len(allCVInMale) / maleVectorLen) * (len(allVoCInMale) / maleVectorLen)
    finalProb = field_product * probMale
    
    print finalProb
    print "male" if finalProb > 0.01 else "female"
    actual = raw_input("What gender is it actually? ")
    formatted_actual = actual.strip().lower()
    
    while formatted_actual != "male" and formatted_actual != "female":
        actual = raw_input("Only male and female are valid answers! What gender is it actually? ")
        formatted_actual = actual.strip().lower()
        
    is_actual_male = 1 if formatted_actual == "male" else 0
    
    with open("babynames-model.txt", "a") as model_file:
        model_file.write(new.upper() + ', ' + ', '.join(str(v) for v in vectorTuple) + ", " + str(is_actual_male) + '\n')
    
    model.append((vectorTuple[0], vectorTuple[1], vectorTuple[2], vectorTuple[3], vectorTuple[4], is_actual_male))

def bayes_classifier():
    
    # read the model, build a list of tuples
    model = []
    f = open("babynames-model.txt")
    for line in f.readlines():
        split = line.split(",")
        model.append((split[1].strip(), split[2].strip(), split[3].strip(), split[4].strip(), split[5].strip(), split[6].strip()))
    
    # wait for input
    while(True):
        run_program(model)
    
bayes_classifier()
        
                    
    