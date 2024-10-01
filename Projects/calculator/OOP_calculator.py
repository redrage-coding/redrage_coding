#OOP Calculator
'''
RedRage-Coding
tkinter Graphic User Interface
11/30/2022
'''

import tkinter as tk

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGIT_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25255E"
WHITE = "#FFFFFF"
OFF_WHITE = "#F8FAFF"
LIGHT_BLUE = "#CCEDFF"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        #Standard iPhone size
        self.window.geometry("300x500")
        self.window.resizable(0,0)
        self.window.title("Calculator")
        
        #Intialize starting booleans and expressions
        self.first_run = True
        self.repeating = False
        self.save_expression = ""
        self.operator_boolean = False
        
        #What to display in small display_frame and
        self.total_expression = "0"
        self.current_expression = "0"
        
        #Display frame current and total
        self.display_frame = self.create_display_frame()
        self.total_label, self.current_label = self.create_display_labels()
        
        #Buttons frame
        #digits dictionary
        self.digits = {
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            0:(4,2), ".":(4,1)
        }
        #Operator dictionary
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-":"-", "+":"+"}
        #Creates frame for buttons
        self.buttons_frame = self.create_buttons_frame()
        
        #Increases size of rows and column to fit
        self.buttons_frame.rowconfigure(0,weight=1)
        for x in range(1,5):
            self.buttons_frame.rowconfigure(x,weight=1)
            self.buttons_frame.columnconfigure(x,weight=1)
            
        #Creates digit buttons
        self.create_digit_buttons()
        #Creates operator buttons
        self.create_operator_buttons()
        #Equals and clear buttons
        self.create_special_buttons()
        
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        
    def create_display_labels(self):
        #Creates the two displays of numbers in display_frame
        #total, small font
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor = tk.E, 
                               bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")
        #current, big font
        current_label = tk.Label(self.display_frame, text=self.current_expression, anchor = tk.E, 
                               bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        current_label.pack(expand=True, fill="both")
        
        return total_label, current_label        
        
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY )
        frame.pack(expand=True, fill="both")
        return frame
    
    def add_to_expression(self, value): #Takes care of digits
        if self.first_run == False and self.repeating == False: #If it has been run add str
            self.current_expression += (str(value))
            if self.save_expression != "":
                self.save_expression += str(value)
        
        #Executes if repeating but not first run. It will add numbers to current_expression and make save expression equal nothing
        #
        elif self.first_run == False and self.repeating == True: 
            self.current_expression += (str(value))
            self.save_expression = ""
                
            self.operator_boolean = True
            
        else: #If first_run is True and self.repeating is False, resets
            self.current_expression = (str(value))
            self.total_expression = ""
            self.save_expression = ""
            self.repeating = False
            self.first_run = False 
            
        self.update_current_label()

        
    def append_operator(self, operator): #Takes care of operators
        self.current_expression += operator
        
        #For if repeating = true, if number is entered after statement was evaluated and then operator is applied
        if self.operator_boolean == True:
            self.total_expression = self.current_expression
            self.operator_boolean = False
        else:
            self.total_expression += self.current_expression
        #Adds current evaluation to total, and than resets current_expression and changes save_expression
        self.save_expression = operator
        self.current_expression = ""
        self.update_total_label()
        self.update_current_label()
        self.repeating = False

        
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            #buttons_frame is the frame it's placed in
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGIT_FONT_STYLE,
                               borderwidth=0,
                               command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
            
    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, font=DEFAULT_FONT_STYLE, 
                               borderwidth=0, command = lambda x=operator: self.append_operator(x))
            button.grid(row = i, column=4, sticky=tk.NSEW)
            i += 1
            
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame
    
    def clear(self):
        self.current_expression = "0"
        self.total_expression = "0"
        self.update_total_label()
        self.update_current_label()
        self.current_expression = ""
        self.first_run = True
        self.save_expression = ""
        self.repeating = False
        self.operator_boolean = False
        
    def Error(self):
        self.current_expression = "Error"
        self.total_expression = ""
        self.update_total_label()
        self.update_current_label()
        self.total_expression = "0"
        self.update_total_label()
        self.current_expression = ""
        self.save_expression = ""
        
        self.first_run = True
        self.repeating = False
        self.operator_boolean = False
        
    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, font=DEFAULT_FONT_STYLE, 
                            borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, columnspan=3, sticky=tk.NSEW)
        
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, font=DEFAULT_FONT_STYLE, 
                            borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)
    
    def evaluate(self):
        #Will add current number in current_expression, for repeating
        try:
            if self.repeating == True:
                self.total_expression += self.save_expression
        #Check if all zeroes
            elif eval(self.current_expression) == "0":
                self.save_expression = "0"
            else: #If not repeating or not all zeroes
                self.total_expression += self.current_expression
                
            self.update_total_label()            
            evaluated_total = str(eval(self.total_expression))
            
            #Makes it look nicer, adds equal sign to total_expression
            self.total_label.config(text=self.total_expression + "=")
            #Makes current_label look like total number
            self.current_label.config(text=evaluated_total)
            
            self.current_expression = ""
            self.total_expression = evaluated_total
            self.repeating = True
            #self.first_run = True
        except:
            self.Error()
        
    def update_total_label(self): #Will change total_label on screen
        self.total_label.config(text=self.total_expression)

    def update_current_label(self): #Will cahnge current_label on screen
        self.current_label.config(text=self.current_expression)
        
    def run(self): #Will loop so calculator does not close after executing
        self.window.mainloop()
        
if __name__ == "__main__":
    calc = Calculator()
    calc.run()