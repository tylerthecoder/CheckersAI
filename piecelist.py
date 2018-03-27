class piecenode:
    def __init__(self,id,type,color,row,col,moves):
        self.id = id
        self.type = type
        self.color = color
        self.row = row
        self.col = col
        self.moves = moves

        self.next = None

    #getters
    def getID(self):
        return self.id

    def getType(self):
        if (self.type == 'b') or (self.type == 'w'):
            return "piece"
        else:
            return "king"

    def getColor(self):
        if (self.color == 'b') or (self.color == 'B'):
            return "black"
        else:
            return "white"

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def getMoves(self):
        return self.moves

    def getNext(self):
        return self.next

    #setter
    def setNext(self,newNext):
        self.next = newNext

    #print node
    def print_node(self):
        print("Id is",self.id)
        print("Type is",self.getType())
        print("Color is",self.getColor())
        print("Position is",self.row,self.col)
        print("Possible moves are",self.moves)

class piecelist:
    def __init__(self):
        self.head = None

    def insert(self,id,type,color,row,col,moves):
        temp = piecenode(id,type,color,row,col,moves)
        temp.setNext(self.head)
        self.head = temp

    def print_list(self):
        current_node = self.head

        while (current_node is not None):
            current_node.print_node()

            current_node = current_node.next

    def search(self,id):
        current_node = self.head

        while (current_node != None) and (current_node.getID() != id):
            current_node = current_node.getNext()
        if (current_node == None):
            print ("That piece does not exist.")
            return False
        if (current_node != None):
            return current_node.getID()

    def p_search(self,id):
        current_node = self.head

        while (current_node != None) and (current_node.getID() != id):
            current_node = current_node.getNext()
        if (current_node == None):
            print ("That piece does not exist.")
            return False
        if (current_node != None):
            return current_node.getRow(),current_node.getCol()

    def m_search(self,id):
        current_node = self.head

        while (current_node != None) and (current_node.getID() != id):
            current_node = current_node.getNext()
        if (current_node == None):
            print ("That piece does not exist.")
            return False
        if (current_node != None):
            return current_node.getMoves()


    def delete(self,id):
        current_node = self.head
        previous_node = None

        while (current_node != None) and (current_node.id != id):
            previous_node = current_node
            current_node = current_node.getNext()

        if current_node == self.head:
            self.head.setNext(current_node.getNext())
        elif current_node == None:
            print("Couldn't find that piece.")
        else:
            previous_node.setNext(current_node.getNext())
