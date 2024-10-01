'''
Erik Bacsa
part1
Baby Name Frequencies
'''

import pickle

# class display_menu1:
#     def __init__(self,commands:dict):
#         for keys, values in commands.items():
#             self.commands = commands
#         def display_menu(self):
            

def display_menu(options:list, message:list) -> str:
    while True:
        print(f"{'-'*30}\nAlberta Baby names\n{'-'*30}")
        message = "".join(message)
        print(message)
        
        command = input("Enter command: ")
        if command in options:
            return command
        
def open_file(filename:str) -> list:
    #Try to open file csv, if it doesn't exist none is returned
    #If file exists then split information into list of lists
    try:
    #Opens csv file
        with open(filename,'r', encoding="utf8") as infile:
            infile = infile.read()
        infile = infile.splitlines()
        new_list = []
        for line in infile[4:]:
            line = line.split(",")
            for x in range(len(line)):
                if line[x].isdigit():
                    line[x] = int(line[x])
            new_list.append(line)
        
        return new_list
        
    except FileNotFoundError:
        print("\nFile does not exist")
        return None

def create_names_dict(data_list:list, names_dict={}) -> dict:
    #Creates dictionary with babie's name as keyword, and containing a list of babies born a year

    for names in data_list:
        names_dict.setdefault(names[1], []).append(names[2:])
    return names_dict 

    
def create_top_ten_dict(data_list:list, top_dict={}) -> dict:
    #Simply adds top name frequency by checking if their rank is in the top10 values
    #Returns the top dict with keys matching a list [rank, name, frequency, sex]
    ranks = [1,2,3,4,5,6,7,8,9,10]
    for entry in data_list:
        if entry[0] in ranks:
            top_dict.setdefault(entry[-1], []).append(entry[:-1])
    return top_dict


def load_file(filename:str, name_dict:dict, top_ten_dict:dict):
    #If a datatype is blank, python sets it to False
    #Loads data list
    #Returns name_dict, top_ten_dict and latest year

    #If blank list use default name
    if not filename:
            filename = 'baby-names-frequency_1980_2021.csv'
    data_list = open_file(filename)
    
    #Error check
    if not data_list:
        return {}, {}, -1, -1
    
    name_dict = create_names_dict(data_list)
    top_ten_dict = create_top_ten_dict(data_list)
    first_year = list(top_ten_dict)[0]
    latest_year = list(top_ten_dict)[-1]
    
    return name_dict, top_ten_dict, first_year, latest_year



def pickle_dicts(name_dict:dict, top_ten_dict:dict, first_year:int, last_year:int):
    #Saves name_dict and top_ten_dict to binary files containing data
    #Uses default filename
    pickle_name = input("Enter a file name [baby_names.pk1]: ")
    if not pickle_name:
        pickle_name = 'baby_names.pk1'

    try:
        with open(pickle_name, 'wb') as file:
            pickle.dump((name_dict, top_ten_dict, first_year, last_year), file)
        return None
    except:
        print("File Could Not Save")
        return None

def load_pickle() -> None:
    #loads pickled data, if the file exists, and returns the data
    
    pickle_name = input("Enter a file name [baby_names.pk1]: ")
    if not pickle_name:
        pickle_name = 'baby_names.pk1'
    try:
        with open(pickle_name, 'rb') as file:
            name_dict, top_ten_dict, first_year, last_year = pickle.load(file)
        return name_dict, top_ten_dict, first_year, last_year
    except:
        print(f"Error, could not load pickle from {pickle_name}")
        return {}, {}, None, None

def name_search(name_dict, first_year, last_year):
    
    #Search baby names and make a string if it is a boy, or different string if it is a girl
    name = input("Enter a name: ").title()
    print_boy = ""
    print_girl = ""

    if name_dict.get(name, False):
        print(f"{name}:")
        for frequencies in name_dict[name]:
            if frequencies[1] == 'Boy':
                print_boy += f'{frequencies[2]:<10}{frequencies[0]:<5}\n'
            elif frequencies[1] == 'Girl':
                print_girl += f'{frequencies[2]:<10}{frequencies[0]:<5}\n'           
        print(f"{'':<10}Boys")
        print(print_boy)
        print(f"{'':<10}Girls")
        print(print_girl)

    else:
        print(f'There were no babies named {name} born in Alberta between {first_year} and {last_year}')
    
    return

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
    for gender in list_to_iterate:
        iterate = 0
        if gender == boy_dict:
            print(f"Top 10 names for baby boys given in Alberta in {year}")
        else:
            print(f"Top 10 names for baby girls given in Alberta in {year}")
        
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
              
              
              

def main()->None:
    #Main loop
    name_dict = {}
    top_ten_dict = {}
    first_year = None
    last_year = None
    options = ['0', '1', '2', '3', '4']
    message = ['(0) Quit \n', '(1) Load and process spreadsheet file\n', '(2) Save processed data\n', '(3) Open processed data\n', '(4) Search for a name\n']
    
    while True:
        command = display_menu(options, message)
        
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
        
        # #Search top 10 list for babies 
        # elif command == '5':
        #     if not name_dict:
        #         print("There is no data\n")
        #     else:
        #         print_top_ten(top_ten_dict, last_year, first_year)
                
        

if __name__ == "__main__":
    main()