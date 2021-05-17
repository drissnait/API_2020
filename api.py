# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:31:44 2020

@author: driss
"""

from flask import Flask
from flask import jsonify
import re
import sys
import json

app=Flask(__name__)

fname="C:/Wamp/www/stage/app/parser/test2.php";

def write(liste):
     for i in liste:
         print(i)

"""
Accueil
"""
@app.route("/")
def dummy_api():
    listeCode=[]
    with open(fname, 'r') as f:
        listeCode.append([line.rstrip() for line in f])
    #print(liste)
    return jsonify(listeCode)

"""
Modules importes
"""
@app.route("/modules")
def isModuleImportedAndRenamed():
    listeModules=[]
    moduleRegex= re.compile("^use.*;$")
    for i, line in enumerate(open(fname)):
        for match in re.finditer(moduleRegex, line):
            listeModules.append("ligne : " + str(i+1) + " => " + match.group())
           
    return ("<p>" + "</p><p>".join(listeModules) + "</p>")

"""
Liste des classes
"""
@app.route("/classes")
def getClasses():
    listeClasses=[]
    classesRegex= re.compile("^class.*([a-z]\w*).*?({)?$")
    for i, line in enumerate(open(fname)):
        for match in re.finditer(classesRegex, line):
            listeClasses.append("ligne : " + str(i+1) + " => " + re.split("{",match.group())[0])
           
    return ("<p>" + "</p><p>".join(listeClasses) + "</p>")

"""
Liste des variables
"""
@app.route("/variables")
def getVariables():
    listeVariables=[]
    variablesRegex= re.compile("\$([a-z]\w*)\s*=\s*(.*?);$")
    for i, line in enumerate(open(fname)):
        for match in re.finditer(variablesRegex, line):
            listeVariables.append("ligne : " + str(i+1) + " => " +line)
           
    return ("<p>" + "</p><p>".join(listeVariables) + "</p>")

"""
Liste des fonctions
"""
@app.route("/functions")
def getFunctions():
    listeFunctions=[]
    functionsRegex= re.compile(".*function.*([a-z]\w*).*[()|(){]$")
    for i, line in enumerate(open(fname)):
        for match in re.finditer(functionsRegex, line):
            listeFunctions.append("ligne : " + str(i+1) + " => " +  re.split("{",line)[0])
           
    return ("<p>" + "</p><p>".join(listeFunctions) + "</p>")

"""
Les boucles for par fonction
"""
@app.route("/functions/Loops")
def getForLoops():
    listeRes=[]
    functionsRegex= re.compile(".*function.*([a-z]\w*).*[()|(){]$")
    forLoopRegex=re.compile("^\s*for.*;.*;.*{")
    whileLoopRegex=re.compile("^\s*while(.*)?({)?$");
    inFunction=False
    for i, line in enumerate(open(fname)):
        for match in re.finditer(functionsRegex, line):
            listeRes.append("Fonction =>ligne : " + str(i+1) + " => " +  match.group())
            inFunction=True
              
        for match in re.finditer(forLoopRegex, line):
                variable="-Boucle For"
                listeRes.append(variable +" => " +  re.split("{",match.group())[0])
                
        for match in re.finditer(whileLoopRegex, line):
                variable="-Boucle While"
                listeRes.append(variable +" => " +  re.split("{",match.group())[0])
          
    return ("<p>" + "</p><p>".join(list(listeRes)) + "</p>")
   
"""
Les affectations par fonction
"""
@app.route("/functions/affectations")
def getAffectations():
    listeRes=[]
    functionsRegex= re.compile(".*function.*([a-z]\w*).*[()|(){]$")
    affectationRegex=re.compile("\$.*=.*;$")
    inFunction=False
    for i, line in enumerate(open(fname)):
        for match in re.finditer(functionsRegex, line):
            listeRes.append("Fonction =>ligne : " + str(i+1) + " => " +  match.group())
            inFunction=True
              
        for match in re.finditer(affectationRegex, line):
                variable="-Affectation"
                listeRes.append(variable +" => " +  match.group())
                
    return ("<p>" + "</p><p>".join(list(listeRes)) + "</p>")

"""
Les conditions par fonction
"""
@app.route("/functions/conditions")
def getConditions():
    listeRes=[]
    functionsRegex= re.compile(".*function.*([a-z]\w*).*[()|(){]$")
    conditionRegex=re.compile(".*(?:if|else).*?((.*))??({)?")
    
    inFunction=False
    for i, line in enumerate(open(fname)):
        for match in re.finditer(functionsRegex, line):
            listeRes.append("Fonction =>ligne : " + str(i+1) + " => " +  match.group())
            inFunction=True
              
        for match in re.finditer(conditionRegex, line):
                variable="-Condition"
                listeRes.append(variable +" => " +  re.split("{",line)[0])
                
    return ("<p>" + "</p><p>".join(list(listeRes)) + "</p>")

"""
les retours de chaque fonction
"""
@app.route("/functions/returns")
def getFunctionsReturns():
    listeRes=[]
    functionsRegex= re.compile(".*function.*([a-z]\w*).*[()|(){]$")
    returnRegex= re.compile("^\s*return.*;")
    
    inFunction=False
    for i, line in enumerate(open(fname)):
        for match in re.finditer(functionsRegex, line):
            listeRes.append("Fonction =>ligne : " + str(i+1) + " => " +  match.group())
            inFunction=True
              
        for match in re.finditer(returnRegex, line):
                listeRes.append("-"+line)
                
    return ("<p>" + "</p><p>".join(list(listeRes)) + "</p>")

"""
Les variables par fonction
"""
@app.route("/functions/declaredVariables")
def getFunctionsVariables():
    listeRes=[]
    functionsRegex= re.compile(".*function.*([a-z]\w*).*[()|(){]$")
    variablesRegex= re.compile("\$([a-z]\w*)\s*=\s*(.*?);$")
    returnRegex= re.compile("^\s*return.*;")
    
    inFunction=False
    for i, line in enumerate(open(fname)):
        for match in re.finditer(functionsRegex, line):
            listeRes.append("Fonction =>ligne : " + str(i+1) + " => " +  match.group())
            inFunction=True
              
        for match in re.finditer(variablesRegex, line):
            if (inFunction==True):
                listeRes.append("-"+line)
                
        for match in re.finditer(returnRegex, line):
            inFunction=False
                
    return ("<p>" + "</p><p>".join(list(listeRes)) + "</p>")


@app.route("/test")
def funTest():
    return "hello"
               


if __name__=="__main__":
    app.run(debug=False)
    """listeVariables={}
    variablesRegex= re.compile("^class.*([a-z]\w*).*?({)?$")
    for i, line in enumerate(open(fname)):
        for match in re.finditer(variablesRegex, line):
            print ('Found on line ' + str(i+1) +'  '+  match.group())"""
    
    
    
    #print("ok")