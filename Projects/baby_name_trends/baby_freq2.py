'''
Erik Bacsa
part2
Baby Name Frequencies
'''

import pickle
from baby_freq1 import *

def print_top_ten(top_ten:dict, last_year, first_year) -> None:
    
    #Find the year to search for top 10 baby names
    year = 0
    while year > last_year or year < first_year:
        year = input(f"Enter year ({first_year} to {last_year}): ")
        if year.isalnum():
            year = int(year)
        else:
            year = 0

    #Create 2 seperate dictionaries to better iterate and organize names and multiple instances
    boy_dict = {}
    girl_dict = {}
    #Set default empty list for how many baby names as keyword, add multiple number of babies to same list
    #person[1] == name, person[2] is how many instances of the name, person[3] is the gender
    for person in top_ten[year]:
        if person[3] == "Boy":
            boy_dict.setdefault(person[2], []).append(f"{person[1]}: {person[2]}")
        
        #Or if it is a girl
        else:
            girl_dict.setdefault(person[2], []).append(f"{person[1]}: {person[2]}")
    
    #Create list to iterate through
    list_to_iterate = [girl_dict, boy_dict]
    print_dict_top_ten(list_to_iterate, girl_dict, boy_dict, year)
    
    # for gender in list_to_iterate:
    #     iterate = 0
    #     if gender == boy_dict:
    #         print(f"Top 10 names for baby boys given in Alberta in {year}")
    #     else:
    #         print(f"\nTop 10 names for baby girls given in Alberta in {year}")
        
    #     for value in gender.values():
    #         iterate += 1
            
    #         if len(value) > 1:
    #             print(f"{iterate:<5} {' '.join(value)}")
    #             for i in range(len(value)-1):
    #                 iterate += 1
    #                 print(f"{iterate}")
    #         else:
    #             print(f"{iterate:<5} {' '.join(value)}")
    #     print()
    return

def print_dict_top_ten(list_to_iterate:list, girl_dict:dict, boy_dict:dict, year:int) -> None:
    #Iterate through list and print
    for gender in list_to_iterate:
        iterate = 0
        if gender == boy_dict:
            print(f"Top 10 names for baby boys given in Alberta in {year}")
        else:
            print(f"\nTop 10 names for baby girls given in Alberta in {year}")
        
        for value in gender.values():
            iterate += 1
            
            if len(value) > 1:
                print(f"{iterate:<5} {' '.join(value)}")
                for i in range(len(value)-1):
                    iterate += 1
                    print(f"{iterate}")
            else:
                print(f"{iterate:<5} {' '.join(value)}")
        print()
    return   
    

def wildcard_search(name_dict:dict) -> None:
    #Prompts user to enter a name with asterik, if no asterik exists loop request
    name = input("Enter name with * indicating missing letters: ").lower()

    while name.count("*") != 1:
        print("There must be one and only one asterisk entered")
        name = input("Enter name with * indicating missing letters: ").lower()
    
    #Find position of asterik
    select_name = create_astr_dict(name, name_dict)
    
    #print select_name, which contains dictionary of information
    print_wildcard(select_name)
   
    return

def create_astr_dict(name:str, name_dict:dict) -> dict:
    #Using the asterik will
    select_name = {}
    pos_astr = name.find('*')
    
    #If is starts with asterik will find names with the ending
    if pos_astr == 0:
        for key,value in name_dict.items():
            if name[pos_astr+1:] in key:
                pos_start = key.lower().find(name[pos_astr+1:])
                if key[pos_start:] == name[pos_astr+1:]:
                    select_name.setdefault(key, sort_years(value))
                    
    #if it ends with asterik will find names beginning with the letters
    elif name[pos_astr] == name[-1]:
        for key,value in name_dict.items():
            if name[:pos_astr].lower() == key[:pos_astr].lower():
                    select_name.setdefault(key, sort_years(value))
    
    #names with an asterisk not at the beginning or the end, e.g. moh*had?????
    #Super confusing instructions, do not understand if they want me to find names containing the letters???
    #Else if asterik is in middle
    #Starts with letters before asterik, and ends with letters after asteriks
    else:
        first_word = name[:pos_astr].lower()
        second_word = name[pos_astr+1:].lower()
        for key,value in name_dict.items():
            ending_pos = len(key) - len(second_word)
            if first_word == key[0:len(first_word)].lower() and second_word == key[ending_pos:].lower():
                select_name.setdefault(key, sort_years(value))
                                        
    return select_name
              
def sort_years(value:list) -> dict:
    #Organize the values of the dictionary into years as keys and then those values will be information about boys and girls in that year
    #It will return a dictionary of that name with years and keyword
    #And the values will have frequencies and gender as values 
    year_dict = {}
    for data in value:
        year_dict.setdefault(data[2], []).append([data[0],data[1]])
    
    for key,data in year_dict.items():
        if len(data) != 2:
            if data[0][1] == 'Boy':
                temp = data[0]
                data = [temp, [0, 'Girl']]
                
            elif data[0][1] == 'Girl':
                temp = data[0]
                data = [[0, 'Boy'], temp]
            year_dict[key] = data

    return year_dict

def print_wildcard(names:dict) -> None:
    #Will print and display wildcard results
    for key1, value1 in names.items():
        print(f"{'Boys':>14} Girls")
        print(key1)
        for key2, value2 in value1.items():
            #print(value2)
            print(f"{key2}{':':<5} {value2[0][0]:<4} {value2[1][0]}")
        print()

    return

def main()->None:
    #Main loop
    name_dict = {}
    top_ten_dict = {}
    first_year = None
    last_year = None
    options = ['0', '1', '2', '3', '4','5', '6']
    message = ['(0) Quit \n', 
               '(1) Load and process spreadsheet file\n',
               '(2) Save processed data\n',
               '(3) Open processed data\n',
               '(4) Search for a name\n',
               '(5) Print top ten list for a year\n',
               '(6) Search for names with specific letters\n']
    
    while True:
        command = display_menu(options, message)
        
        #Quit
        if command == '0':
            print("Goodbye")
            return
        
        #Load file
        elif command == '1':
            filename = input("Enter a file name [baby-names-frequency_1980_2021.csv]: ")
            #If a datatype is blank, python sets it to False
            name_dict, top_ten_dict, first_year, last_year = load_file(filename, name_dict, top_ten_dict)

        #Save pickled file
        elif command == '2':
            if not name_dict:
                print("There is no data\n")
            else:
                pickle_dicts(name_dict, top_ten_dict, first_year, last_year)
        
        #Load pickled file 
        elif command == '3':
            name_dict, top_ten_dict, first_year, last_year = load_pickle()
           
        #Search names through name_dict 
        elif command == '4':
            if not name_dict:
                print("There is no data\n")
            else:
                name_search(name_dict, first_year, last_year)
        
        #Search top 10 list for babies 
        elif command == '5':
            if not name_dict:
                print("There is no data\n")
            else:
                print_top_ten(top_ten_dict, last_year, first_year)
                
        elif command == '6':
            if not name_dict:
                print("There is no data\n")
            else:
                wildcard_search(name_dict)        
                
        

if __name__ == "__main__":
    main()