from Node import Node


def filter_uppercase_and_spaces(input_string: str) -> str:
    """
    Filters the input string to retain only uppercase letters and spaces.
    """
    return "".join(
        char for char in input_string.upper() if char.isalpha() or char == " "
    )


def count_frequencies(inMessage: str) -> list[int]:
    """
    Counts the frequency of each uppercase letter in the input string.
    Returns a list of 26 integers, where index 0-25 correspond to 'A'-'Z'.
    You can assume the input string contains only uppercase letters and spaces.
    And that spaces are the most frequent character, so really we dont need
    to count them.
    """

    #Creates an array equal to the amount of ASCII symbols
    ASCII_SYMBOLS:int = 256
    frequencies = [0] * ASCII_SYMBOLS

    #It then takes the input string and iterates over each character
    for char in inMessage:
        ascii_value = ord(char)
        frequencies[ascii_value] += 1

    return frequencies



def initialize_forest(frequencies: list[int]) -> list[Node]:
    """
    Initializes a forest (list) of Node objects for each character with a non-zero frequency.
    """
    forest = []

    #iterate over the input array
    for ascii in range (len(frequencies)):
        #adds tree nodes to the forest if the frequency is greater than 0
        if frequencies[ascii] > 0:
         newNode = Node(frequencies[ascii], chr(ascii))  
         forest.append(newNode)
    return forest

def getSmallest(forest):
    smallestIndex = 0

    for node in range(1, len(forest)):
        if forest[node] < forest[smallestIndex]:
            smallestIndex = node

    return forest.pop(smallestIndex)

def build_huffman_tree(frequencies: list[int]) -> Node:
    """
    Builds the Huffman tree from the list of frequencies and returns the root Node.
    """
    forest = initialize_forest(frequencies)
    # Your code here
    while len(forest) > 1:
        #Checks the smallest two nodes in the forest
        s1 = getSmallest(forest)
        s2 = getSmallest(forest)

        #Creates a new node with the sum of the two smallest nodes
        newNode = Node(s1.get_frequency() + s2.get_frequency())
        newNode.set_left(s1)
        newNode.set_right(s2)

        #Adds the new node back into the forest
        forest.append(newNode)
    return forest[0]


def build_encoding_table(huffman_tree_root: Node) -> list[str]:
    """
    Builds the encoding table from the Huffman tree.
    Returns a list of 27 strings, where index 0-25 correspond to 'A'-'Z'
    and index 26 corresponds to space.
    Each string is the binary encoding for that character.
    """
    #Uses a stack to traverse the tree iteratively and creates an encoding table
    traverseStack = [(huffman_tree_root, "")]
    encodeTable = [""] * 27

    while traverseStack:
        #takes items off the stack to use
        node, coded = traverseStack.pop()
        
        #variables use to hold the character and size of the table
        char = node.get_symbol()
        tableSize = len(encodeTable) - 1

        #Checks if the node is a leaf node
        if node.get_left() == None and node.get_right() == None:
            #if the character is a space adds it to the last index of the table
            if char == " ":
                encodeTable[tableSize] = coded
            #If its a letter adds it to the corresponding index
            else:
                #adds characters using the ASCII value to find the index
                encodeTable[ord(char) - ord("A")] = coded
        #Otherwise it traverses instead
        else:
            # Traverse right child
            if node.get_right() is not None:
                traverseStack.append((node.get_right(), coded + "1"))
            # Traverse left child
            if node.get_left() is not None:
                traverseStack.append((node.get_left(), coded + "0"))

    return encodeTable


    
def encode(input_string: str, encoding_table: list[str]) -> str:
    """
    Encodes the input string using the provided encoding table. Remember
    that the encoding table has 27 entries, one for each letter A-Z and
    one for space. Space is at the last index (26).
    """
    #Return variable and magic number avoider
    spaceIndex = len(encoding_table) - 1
    encodeStr = ""

    #iterates over each character in the input string
    for char in input_string:
        #adds the corresponding encoding to the return variable
        if char == " ":
            encodeStr += encoding_table[spaceIndex]
        else:
            encodeStr += encoding_table[ord(char) - ord("A")]

    return encodeStr

def decode(encoded_string: str, huffman_root: Node) -> str:
    """
    Decodes the encoded string using the Huffman table as a key.
    """
    decodeStr = ""
    traverseNode = huffman_root

    #iterates over each bit in the encoded string
    for bit in encoded_string:
        #1s are interpreted as right, 0s are left
        if bit == "1":
            traverseNode = traverseNode.get_right()
        else:
            traverseNode = traverseNode.get_left()

        #Once it hits a leaf, it takes the symbol, adds it to the return, and resets traversal
        if traverseNode.get_left() is None and traverseNode.get_right() is None:
            decodeStr += traverseNode.get_symbol()
            traverseNode = huffman_root

    return decodeStr


#Test variables

#Portion of Frankenstein by Mary Shelly used to test
testStr = filter_uppercase_and_spaces("It was on a dreary night of November that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, " \
"I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. " \
"It was already one in the morning; the rain pattered dismally against the panes, and my candle was nearly burnt out, when, " \
"by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open; it breathed hard, and a convulsive motion agitated its limbs.")

#Frequencies array test
frequencies = count_frequencies(testStr)
print("frequencies: ")
print(frequencies)

tree = build_huffman_tree(frequencies)

#encoding table build test
encodingTable = build_encoding_table(tree)
print("encoding table: " )
print(encodingTable)

#encode and decode tests
encodeTest = encode(testStr, encodingTable)
print("test 1: ")
print(encodeTest)

decodeTest = decode(encodeTest, tree)
print("test 2: ")
print(decodeTest)

