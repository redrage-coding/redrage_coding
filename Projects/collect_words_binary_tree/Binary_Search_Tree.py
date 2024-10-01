'''
lab 7
Erik Bacsa
Binary Search Tree
'''
import string

class BinarySearchTree:
    class _Node:
        def __init__(self, word, count=1, left=None, right=None, depth = 0, parent = None):
            #may add other attributes
            self._word = word
            self._count = count
            self._left = left
            self._right = right
            self._depth = depth
            self._parent = parent
            #keep track of the depth of each node in the tree
            pass
        
        def __str__(self): #return value and count
            str_to_print = f"{self._word}[{self._count}]"
            return str_to_print
        
    #may add other method to show inforatmion needed by print
    
    def __init__(self): #create empty tree
        self._root=None
        
        #may add other attributes to make functionality more efficient
        self._total_words = 0
        self._distinct_words = 0
        
    def insert(self, target):
        #If root is none, add a value for root
        if self._root == None:
            self._root = self._Node(target)
            self._total_words += 1
            self._distinct_words += 1
            return
        
        parent = None
        probe = self._root
        depth = probe._depth
        
        while (probe != None) and (probe._word != target):
            if target < probe._word:
                parent = probe
                probe = probe._left
            else:
                parent = probe
                probe = probe._right
                
            depth += 1
                
        #if value is in tree, increment count
        if probe != None and probe._word == target:
            probe._count += 1
            self._total_words += 1
            return
        
        #otherwise a new _Node object will be inserted with a value for word 
        if target < parent._word:
            parent._left = self._Node(target, 1, None, None, depth, parent)
        else:
            parent._right = self._Node(target, 1, None, None, depth, parent)

        self._total_words += 1
        self._distinct_words += 1
        return
    
    def search(self, value):
        if self._root == None:
            return None
        
        probe = self._root
        while (probe != None):
            if probe._word == value:
                break
            if probe._word > value:
                probe = probe._left
            
            else:
                probe = probe._right
            
        #will perform binary search to find value
        if probe == None:
            print(f"{value} not found")
            return 
        
        if probe._word == value:
            return probe

    
    def most(self):
        #visit node with most occurances recursively
        if self._root == None:
            print("Tree is empty")
            return
        
        probe = self._root
        #recursive method, will find highest count
        most_probe = self._most_helper(probe, probe)
        most = most_probe._count
        print(f"The most occurances is {most}")
        #recursive method, print every probe with equal occurances
        self._most_printer(probe, most)

    
    def _most_helper(self, probe, most_probe):
        #Base case, when probe is none will return most_probe
        if probe == None:
            return most_probe
        current_probe_count = probe._count
        #Change the most_probe if the current probe has higher count than most_probe
        if current_probe_count > most_probe._count:
            most_probe = probe
            
        most_probe = self._most_helper(probe._left, most_probe)
        #print(most_probe)
        most_probe = self._most_helper(probe._right, most_probe)
        #print(most_probe)
        
        return most_probe
        
    def _most_printer(self, probe, most):
        if probe == None:
            return
        if probe._count == most:
            print(f"{probe._word}, count = {probe._count}")
        self._most_printer(probe._left, most)
        self._most_printer(probe._right, most)
        return
    
    def first(self):
        #go as far left as possible 
        #interatively or recursively possible
        if self._root == None:
            return
        probe = self._root
        while probe._left != None:
            probe = probe._left
        return probe._word
    
    def last(self):
        #go as far right as possible 
        #interatively or recursively possible
        if self._root == None:
            return
        probe = self._root
        while probe._right != None:
            probe = probe._right
        return probe._word
    
    def print(self):
        #Will perform inorder recursive traversal for this operation
        print("Printing the tree")
        if self._root == None:
            return
        probe = self._root
        self._print_helper(probe)
    
    def _print_helper(self, probe):
        if probe == None:
            return
        self._print_helper(probe._left)
        if probe._parent == None:
            parent_print = None
        else:
            parent_print = probe._parent._word
        print_statement = f"{probe}, depth = {probe._depth}, parent = {parent_print}"
        print(print_statement)
        self._print_helper(probe._right)
        return
    
    def summary(self):
        #print summary of tree
        max_height = self.height()
        first_word = self.first()
        last_word = self.last()
        total_words = self._total_words
        distinct_words = self._distinct_words
        #Total number read
        #number of distinct words
        print("** Tree Statistics **")
        print(f"\t Height of tree: {max_height}")
        print(f"\t Total words: {total_words}, Distinct words: {distinct_words}")
        print(f"\t First word: {first_word}")
        print(f"\t Last word: {last_word}")
        return
    
    def height(self):
        #find max height of tree, which will be height of root
        if self._root == None:
            return 0
        
        probe = self._root
        height = probe._depth
        max_height = self._height_helper(probe, height)
        return max_height
    
    def _height_helper(self, probe, height):
        #Base base
        if probe == None:
            return height
        
        current_height = probe._depth
        if current_height > height:
            height = current_height
        
        height = self._height_helper(probe._left, height)
        height = self._height_helper(probe._right, height)

        return height
    
    def delete(self, value):
        #Find node to delete
        if self._root == None:
            print("No tree to delete values")
            return
        
        node = self.search(value)
        if node == None:
            return
        
        parent = node._parent
        #update self._total_words and self._distinct_words
        self._total_words -= node._count
        self._distinct_words -= 1

        print(f"Deleted word: '{node._word}' had {node._count} occurances")
        
        if (node._left is not None) and (node._right is not None):
            self._delete_node_with_two_children(node)
        else:
            self._delete_node_with_one_child_or_none(node, parent)
            
        return
    
    def _delete_node_with_one_child_or_none(self, node, parent):
        #Replace node with a child
        #Find if its left or right node
        #successor = node._left if node._left is not None else node._right

        if node._left != None:
            successor = node._left
        else:
            successor = node._right
            
        if node == self._root:
            #Possibility of deleting all entries, root will be none
            if successor == None:
                self._root = None
                return 
            self._root = successor
            self._root._parent = None
            #Delete_update_depth will minus one to all nodes depths below it.
            #Must set self._root._depth to 1 because all nodes are below it.
            self._root._depth = 1
            self.delete_update_depth(self._root)
            return
        
        elif node == parent._left:
            parent._left = successor
        
        elif node == parent._right:
            parent._right = successor
            
        #the successor could be NONE (when assigning the succesor = node._right)
        #Will need to account for NONE not having attributes of node
        #if successor == None: return
        if successor != None:
            successor._parent = parent
            #Update the depth of each node under this node including this node.
            self.delete_update_depth(successor)
        
    def _delete_node_with_two_children(self, node):
        #Find successor
        successor, parent = self._parent_and_successor(node)
        
        node._word = successor._word
        node._count = successor._count
        #Delete the successor's old positon by calling delete with one or none node
        self._delete_node_with_one_child_or_none(successor, parent)

        return
    
    def _parent_and_successor(self, node):
            #Will probe right and then as far left as possible to replace original node
        probe = node._right
        while probe._left != None:
            probe = probe._left
        parent = probe._parent
        return probe, parent
    
    def delete_update_depth(self, node):
        if node == None:
            return
        node._depth -= 1
        self.delete_update_depth(node._left)
        self.delete_update_depth(node._right)
 
    def levelprint(self):
        #Find height of tree and multiply a list by it.
        height = self.height()
        #print(height)
        level_list = [[] for n in range(height + 1)]
        #Recursively iterate through binary tree and insert words based onto a list of list based on depth of word
        node = self._root
        self._levelprint_helper(node, level_list)
        print("Level print of the tree")
        for level in level_list[::-1]:
            level = ", ".join(level)
            print(f"Depth {height}: {level}")
            height -= 1
            
        return
    
    def _levelprint_helper(self, probe, level_list):
        if probe == None:
            return
        depth = probe._depth
        tmpStr = str(probe)
        level_list[depth].append(tmpStr)
        self._levelprint_helper(probe._left, level_list)
        self._levelprint_helper(probe._right, level_list)
        return
        
    
def main(): #driver
    command_list = []
    intialized = False
    tree_exist = False
    
    while True:
        print(f"Enter a command:\n{"(1)read \"file.txt\"":<20}{"(2)print":<20}(3){"first":<20}\n{"(4)last":<20}{"(5)summary":<20}{"(6)search":<20}\n{"(7)delete":<20}{"(8)levelprint":<20}\n")
        user_input = str((input("Enter input: "))).lower()
        
        #read user input until 'quit'
        if user_input == 'quit':
            print("**BST Program Finished**")
            break
        
    #when user enters read: check that file exists then open file,  (try and except)
    #clean words in file if read and return a list of words
        if user_input[:4] == 'read':
            try:
                filename = user_input[4:].strip()
                with open(filename, 'r') as file:
                    file = clean_file(file)
                intialized = True
            except:
                print("File does not exist")
    
    #create an empty binary search tree(bst), add words into it
        if intialized:
            BST = BinarySearchTree()
            for word in file:
                BST.insert(word)
            intialized = False
            tree_exist = True
        
    #if user types a command before read, display message and wait for command
        if (tree_exist == False) and (user_input[:4] != 'read'):
            print("File not read, command added to queue")
            command_list.append(user_input.strip())
            
        elif tree_exist == True:
            command_list.append(user_input)
            #Iterate through command list and execute each command
            for command in command_list:
                if command[:5] == 'print':
                    BST.print()
                elif command[:5] == 'first':
                    first_word = BST.first()
                    print(f"The first word is {first_word}")
                elif command[:4] == "last":
                    last_word = BST.last()
                    print(f"The last word is {last_word}")
                elif command[:4] == "most":
                    BST.most() 
                elif command[:7] == "summary":
                    BST.summary()
                elif command[:6] == "search":
                    word = command[6:].strip()
                    word_found = BST.search(word)
                    print(f"For this word: {word_found}")
                elif command[:6] == "delete":
                    word = command[6:].strip()
                    BST.delete(word)
                elif command[:10] == "levelprint":
                    BST.levelprint()
                    
            command_list = []
            
def clean_file(file):
    #All punctuation except ' and _ are to be removed
    punctuation = string.punctuation
    file = file.read()
    file = file.replace('\n', ' ')
    file = file.split(" ")
    #Clean the words
    num = 0
    size = len(file)
    while num < size:
        file[num] = file[num].strip().lower()
        if file[num] == '': #Remove entires in list that are empty
            file.pop(num)
            size -= 1
            continue #If the item was removed, dont increase num count, will need to check again
        for letter in file[num]:
            if (letter in punctuation) and (letter != "'") and (letter != "_"):
                #If the letter is a hypon lets add the word to the list
                # if letter == '-':
                #     pos = file[num].find('-')
                #     file.append(file[num][pos:])
                #     file[num] = file[num][:pos]
                #     size += 1
                file[num] = file[num].replace(letter, "")
        num += 1
    return file
    
    
if __name__ == "__main__":
    main()