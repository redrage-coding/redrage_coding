How baby_freq works

REQUIRED FILES 
************************************************************************************************************************************
baby_freq1.py, baby_freq2.py, baby_freq3.py and graphics.py baby-names-frequency_1980_2021.csv
************************************************************************************************************************************


Uses data from the Alberta government about baby names
Imports the data and saves it into a pickle format
Uses tkinter to graphically show the trend of a baby name
Names are split into both girl and boys


************************************************************************************************************************************

(0) Quit //Quit project

(1) Load and process spreadsheet file //loads csv file 

(2) Save processed data 
 //saves file to pickle format Pickling is a way to convert a python object (list, dict, etc.) into a character stream. The idea is that this character stream contains all the information necessary to reconstruct the object in another python script.

(3) Open processed data
//opens pickled data

(4) Search for a name
//search for a name from the csv file

(5) Print top ten list for a year
//prints top 10 list for Alberta names

(6) Search for names with specific letters
//search for many names with their started letters ||| use asterisk indicate the names you want to find
//example er* will print all names that start with er and their frequencies

(7) Graphically display the trend of a name
//End a name to find it's graphical trend