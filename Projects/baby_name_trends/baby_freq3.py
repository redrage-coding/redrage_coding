'''
Erik Bacsa
part3
Baby Name Frequencies
'''
from baby_freq2 import *
from graphics import *
import pprint

def display_graph(name_dict:dict) -> None:
    name_person = input("Enter a name: ").title()
    if not name_dict.get(name_person, False):
        print("Person not found")
        return
    
    win = GraphWin(name_person, 1000, 600)
    
    #Call on Milestone 2 project for my sort years function. 
    #It will return a dictionary of that name with years as keyword
    #And the values will have frequencies and gender as values in a list
    #Example {'Erik': {1980: [[23, 'Boy'], [0, 'Girls]] } }
       
    year_dict = {}
    year_dict.setdefault(name_person, sort_years(name_dict[name_person]))
    year_dict = year_dict_fill_in_blanks(name_person,year_dict)
    
    
    #Pixel to work with will be from x : 40 to 960, total 920 pixels
    #                                y : 40 to 560, total 520 pixels
     
    #____________________________
    #Display starting graphics
    graph_title(win, name_person)
    #Display graph vertical and horizontal
    graph_axis(win)
    
    #Get biggest frequency
    highest_frequency = find_highest_frequency(name_dict, name_person)
    
    #If frequency is bigger than max height of 520 pixels, use a percentage to downsize
    if highest_frequency > 520:
        #Convert to percent total to use
        percent_pixel_to_frequency = 520 / highest_frequency
        pixel_to_frequency = 1
    else:   
        percent_pixel_to_frequency = 1
        pixel_to_frequency = 520 / highest_frequency

    #Convertion ratio
    #percent_pixel_to_frequency * pixel_to_frequency * current frequency of name used
    
    
    #Plot Vertical axis
    plot_vertical(highest_frequency, pixel_to_frequency,percent_pixel_to_frequency, win)
    #Plot Horizontal axis
    plot_horizontal(year_dict, name_person, win)
    #Plot data
    plot_data(year_dict, name_person, percent_pixel_to_frequency, pixel_to_frequency, win)


    #----------------------------TESTING STUFF-----------------------------
    # print(name_dict.get(name_person), '\n')
    # print(year_dict)
    # print(highest_frequency, "Highest Frequency")
    # print(percent_pixel_to_frequency * pixel_to_frequency, "How many pixels per point")
    #----------------------------TESTING STUFF------------------------------

    #Pause for click
    try:
        win.getMouse()
        win.close()
    except:
        win.close()


def year_dict_fill_in_blanks(name_person, year_dict):
    years_list = []
    for x in range(1980, 2022):
        years_list.append(x)
    for year in years_list:
        if not year_dict[name_person].get(year, False):
            year_dict[name_person][year] = [[0, "Boy"],[0, "Girl"]]

    return year_dict

def graph_title(win, name_person:str):
    #Set-up graphics for graph
    #Title
    title_graph = Text(Point(500,20), f"Trend for the name {name_person}")
    title_graph.setSize(18)
    title_graph.setStyle("bold")
    title_graph.draw(win)
    
    #Set-up graphics for graph
    title_graph1 = Text(Point(500,40), "Click anywhere to close window")
    title_graph1.setSize(13)
    title_graph1.setStyle("bold")
    title_graph1.setTextColor("red")
    title_graph1.draw(win)
    
    #blue for boy, red for girl
    title_graph1 = Text(Point(800,40), "Blue for men\n Red for women")
    title_graph1.setSize(12)
    title_graph1.setStyle("bold")
    title_graph1.setTextColor("black")
    title_graph1.draw(win)
    
def graph_axis(win):
    #graph will start 100 pixel from the left and 100 pixel from the bottom.
    #x total value = 1000
    #y total value = 600
    # x,y
    vertical_line = Line(Point(40,40), Point(40, 560))
    horizontal_line = Line(Point(40,560), Point(960,560))
    vertical_line.draw(win)
    horizontal_line.draw(win)
    
    #Pixel to work with will be from x : 40 to 960, total 920 pixels
    #                                y : 40 to 560, total 520 pixels
     

def find_highest_frequency(name_dict:dict, name:str):
    highest_value = 1
    for values in name_dict[name]:
        if values[0] > highest_value:
            highest_value = values[0]
            
    return highest_value

def plot_vertical(highest_frequency, pixels_to_frequency, perecent_pixel_to_frequency, win):
    #0-520 y-axis
    #Create lines 
    plot_points = [0]
    #if highest_frequency == 1:
    if highest_frequency <= 12:
        iterate_amount = 1
        total = iterate_amount
        while total <= highest_frequency:
            plot_points.append(round(total))
            total += iterate_amount
            
        for y in plot_points:
            temp_y = y*pixels_to_frequency
                
            plot = Line(Point(40,560-temp_y), Point(30,560 - temp_y))
            plot.draw(win)
                
            text_plot = Text(Point(15,560-temp_y), f'{y}')
            text_plot.draw(win)
     
    #If greater than 12, will divide into 4 segments after 0       
    else:
        iterate_amount = (highest_frequency / 4) 
        total = iterate_amount
        
        while total < highest_frequency:
            plot_points.append(round(total))
            total += iterate_amount 
        plot_points.append(highest_frequency)
        
        #print(plot_points)
        
            
        for y in plot_points:
            temp_y = y * pixels_to_frequency * perecent_pixel_to_frequency
            #print(temp_y)
                
            plot = Line(Point(40,560-temp_y), Point(30,560 - temp_y))
            plot.draw(win)
                
            text_plot = Text(Point(15,560-temp_y), f'{y}')
            text_plot.draw(win)
    
    return
        
def plot_horizontal(year_dict:dict, name, win):
    years = []
    
    #For key is the name of the person, second key is the years in the dictionary
    #Will grab all the years into a list
    for num_year in year_dict[name].keys():
        years.append(num_year)
    years.sort()
    pixel_per_year = 920/(len(years)-1)
    start_pixel = 0
    
    #Make a line for every x-axis point and for every even year plot the year.
    for year in range(len(years)):
        line_year = Line(Point(40 + start_pixel, 560), Point(40 + start_pixel, 570))
        line_year.draw(win)
        if year % 2 == 0:
            text_year = Text(Point(40 + start_pixel, 580), f"{years[year]}")
            text_year.draw(win)
        start_pixel += pixel_per_year

    
def plot_data(year_dict, name, percent_pixel_to_frequency, pixel_to_frequency, win):
    #For key is the name of the person, second key is the years in the dictionary
    #Will grab all the years into a list
    year_list = []
    for num_year in year_dict[name].keys():
        year_list.append(num_year)
    year_list.sort()
 
    #pprint.pprint(year_dict)
    #print(year_list)
    

    #percent_pixel_to_frequency * pixel_to_frequency * current frequency of name used  
    x_pixel_per_year = 920/(len(year_list)-1)
    x_start_pixel = 0

    
    for year in range(len(year_list)):
        if year == len(year_list) - 1:
            break
        
        #Get current y values
        #Value will just iterate from 0 to year number
        for value in year_dict[name][year_list[year]]:
            if value[1] == 'Boy':
                boy_current_y = value[0]
            elif value[1] == 'Girl':
                girl_current_y = value[0]       

        # Get Next y values
        for value in year_dict[name][year_list[year+1]]:
            if value[1] == 'Boy':
                boy_next_y = value[0]
            elif value[1] == 'Girl':
                girl_next_y = value[0]
        
        #print(1980+year,"Current year", 1981+year, "Next year", boy_current_y, boy_next_y, 'boy_next_y, girl')
        
        #Plot points using 600-40 as max y range
        boy_current_convert = boy_current_y * percent_pixel_to_frequency * pixel_to_frequency
        boy_next_convert = boy_next_y * percent_pixel_to_frequency * pixel_to_frequency
        girl_current_convert = girl_current_y * percent_pixel_to_frequency * pixel_to_frequency
        girl_next_convert = girl_next_y * percent_pixel_to_frequency * pixel_to_frequency
        


        boy_line = Line(Point(40 + x_start_pixel, 560 - boy_current_convert), Point(40 + x_start_pixel + x_pixel_per_year, 560 - boy_next_convert))
        girl_line = Line(Point(40 + x_start_pixel, 560 - girl_current_convert), Point(40 + x_start_pixel + x_pixel_per_year, 560 - girl_next_convert))
        
        boy_line.setFill("Blue")
        girl_line.setFill("Red")
        
        boy_line.setWidth(3)
        girl_line.setWidth(2)
        
        boy_line.draw(win)
        girl_line.draw(win)
        
        x_start_pixel += x_pixel_per_year


    #print(year_dict)


def main()->None:
    #Main loop
    name_dict = {}
    top_ten_dict = {}
    first_year = None
    last_year = None
    options = ['0', '1', '2', '3', '4','5', '6', '7']
    message = ['(0) Quit \n', 
               '(1) Load and process spreadsheet file\n',
               '(2) Save processed data\n',
               '(3) Open processed data\n',
               '(4) Search for a name\n',
               '(5) Print top ten list for a year\n',
               '(6) Search for names with specific letters\n',
               '(7) Graphically display the trend of a name\n']
    
    while True:
        command = display_menu(options, message)
        
        #Quit
        if command == '0':
            print("Exitting Program")
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
                
                
        #Wild card search
        elif command == '6':
            if not name_dict:
                print("There is no data\n")
            else:
                wildcard_search(name_dict)  
                
        #Print graphics
        elif command == '7':
            if not name_dict:
                print("There is no data\n")
            else:
                display_graph(name_dict)         
                
        

if __name__ == "__main__":
    main()