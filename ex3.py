from collections import deque

####################################################
#  Node object that contains tree information
#  Class static counter gives each node a unique id
#  Class static value also can keep longest Branch 
#  Each node, when duplicated, increments a counter
#      so it defaults to one in the constructor
#  Position is the nodes position from the start of Text
#  fromRoot is chars position in that specific path
#      or the number of loops since the start 
#  Aside from constructor, a member function find_child
#      looks thru list of children for match or returns 0 
####################################################
class TrieNode(object):
    # Function to initialize the node
    Node_counter=0
    LongestB=0
    def __init__(self, char: str, pnode, charp: str, pos=0,pPath=0):
        self.char=char
        self.pnode=pnode
        self.parent=charp
        self.children = []
        self.word_finished=False
        self.counter=1
        self.position=pos
        self.path=pPath
        self.id=TrieNode.Node_counter
        TrieNode.Node_counter+=1

    def find_child(self,asymbol):
        for i in self.children: 
            if i.char==asymbol:
                return i 
        return 0 

    def show_children(self):
        aList=[]
        for i in self.children: 
            aList.append(i.char)
        return aList 

def printNodeList(nodeList):
    nodeList.reverse()
    for j in nodeList:
       print(j.char,end="")
    print()

#----------------------------------------------------------------
#  Utility to print a Tree of sorts, other node info as needed 
#  Ex. Start->End:Value   Position
#  Note roots value char is a *, and its parent is itself
#  Prints in dept first using a stack, add children as 
#  encountered by each parent node to the stack 
#----------------------------------------------------------------
def printNodeDepthWise(root):
    if root is None:
        return
    #  get started with just the root
    stack=[]
    stack.insert(0,root)  # in front, a stack
    while(len(stack) > 0):
        n=len(stack)
        while (n > 0):
            p=stack.pop(0)  # take off the front
            str="{} {}->{}"
            print(str.format(p.id,p.char,p.show_children()))
            #print(str.format(p.parent,p.id,p.char,p.path,p.position))
            #print(p.word_finished)
            #print(str.format(p.parent,p.id,p.char))
            
            for index, value in enumerate(p.children):
                stack.insert(0,value)  # stack them all on the front
            n -=1
            print("------")

        print("============")
#----------------------------------------------------------------
#  Utility to print a Tree of sorts, other node info as needed 
#  Ex. Start->End:Value   Position
#  Note roots value char is a *, and its parent is itself
#  Prints in breadth first using a queue, add children as 
#  encountered by each parent node to the queue
#----------------------------------------------------------------
def printNodeLevelWise(root):
    if root is None:
        return
    queue=[]
    queue.append(root)
    while(len(queue) > 0):
        n=len(queue)
        while (n > 0):
            p = queue[0]
            queue.pop(0)
            #fullstr="{}->{}:{} {} {} {}"
            str="{}>{}"
            if p.char !='?': 
               #fish
               print(str.format(p.char,p.show_children()))
            
            for index, value in enumerate(p.children):
                queue.append(value)
            n -=1

###################################################################
#   Tree walk looking for edges defined by:
#        $ to backtrack through 
#        or multi-child node to backtrack trough to parent multichild node
#        or single child node? 
#   
#       self.position=pos    distance from the root, distinguish duplicate
#       self.path=pPath      string or path number
#       self.id=TrieNode.Node_counter  unique node number
#       self.pnode        parents node, full object` 
#       self.parent      char in parent
###################################################################
def edgeLabels(root):
    if root is None:
        return
    queue=[]
    queue.append(root)
    while(len(queue) > 0):
        n=len(queue)
        while (n > 0):
            #p = queue[0]
            p=queue.pop(0)
            if p.char !='*':
               #fish
               #print(str.format(p.char,p.id,p.position,p.path))
               if p.char=='$':
                   dinks=backTrack(p)
                   printNodeList(dinks)
               elif len(p.children) >=2:
                   #print(p.char)
                   dinks=backTrack2(p)
                   printNodeList(dinks)

            for index, value in enumerate(p.children):
                queue.append(value)
            n -=1

def backTrack(aNode):
    ##### given a node, backtrack all singly visited nodes creating a list
    #####
    # lizard
    rList=[]
    x=len(aNode.children)
    while (len(aNode.children) <= 1):
       rList.append(aNode) 
       aNode=aNode.pnode
       #print("backtracking...")
    #print("End of the line")
    return rList

def backTrack2(aNode):
    ##### given a node, backtrack all singly visited nodes creating a list
    #####
    # lizard
    rList=[]
    rList.append(aNode)
    aNode=aNode.pnode
    x=len(aNode.children)
    while (len(aNode.children) <= 1):
       rList.append(aNode) 
       aNode=aNode.pnode
       #print("backtracking...")
    #print("End of the line")
    return rList
#----------------------------------------------------------------
#  Utility to read a file, change name, header, etc accordingly 
#  Called from main, at start of program, edit open for file name
#  typically returns a list
#  typically uses a counter to get past first lines of meta info
#----------------------------------------------------------------
def readFile():
    """  include any needed header processing or stripping 
                  
    """
    #f=open("ex3s.dat","r")
    #f=open("ex3.dat","r")
    f=open("test.dat","r")
    #f=open("cs.dat","r")
    j=[]
    for l in f:
       l=l.strip() 
       j.append(l)
    return j

##################################################################
#
# Using a suffix of Text, see if it makes it to the end 
# Called by
# symbol is char from Text
# vchar is char from a child of the object Node, init first child
# vNode is the whole object itself, init pts to root
##################################################################
def PrefixTrieMatching(Text,Trie):
    symbol=Text[0]
    vchar=Trie.children[0].char
    vNode=Trie
    i=1   #  Text position marker
    lText=len(Text)
    while True:
        # check if its a leaf.  Could also check for children but this flag should be set
        # if so your done
        if vNode.word_finished==True:
            #print("Done Found a terminal character")
            #this leg of the Trie has parsed.  Maybe print the id of the start node of text 
            return True
        # check all children for vNodes.char matches symbol. Progress down both child and Text
        nextVnode=vNode.find_child(symbol) #  only one child will match, 0 if none
        if nextVnode !=0: 
            #print("Found match ",symbol," follow node/Text)
            vNode=nextVnode 
            symbol=Text[i]
            if i < lText-1:
               i+=1
        else:
            #print("No matches found")
            return False 

##############################################
#   Driver to look at each char in Text and follow it down the Trie as far as possible
#   The first letter of Text need to find the first gen of the Trie and try to match all the way to the end
#   If it does, the starting point is returned, if it doesn't a flag responds that it is not found
#   The start position is stored in a list that is finally printed out at the end
##############################################
def TrieMatching(Text, Trie):
       cntr=0
       paths=[]
       while len(Text) > 1:  #  Text will get shorter each loop as it progresses
           position=PrefixTrieMatching(Text,Trie) # returns either the start position if successful other wise...
           #print("back from PrefixTrieMatcing, move down text")
           if position:
              #print("Bingo, found one ",cntr)
              paths.append(cntr)
              #printList(paths)
           cntr+=1
           Text=Text[1:]
       return paths

#--------------------------------------------
#  Utility to print any list with one space between elements
#--------------------------------------------
def printList(aList):
    str="{} "
    #    print(str.format(root.id,x.id,x.char))
    for j in aList:
        print(str.format(j),end="")

##############################################
#  Add to SuffixTrie builder to include position
#  and path counters.  fromRoot id marks each node
#  and shows the symbols location on Text
#  While position shows which full path it 
#  belongs to.
##############################################
def ModifiedSuffixTrieConstruction(Text):
    #create the root by constructing the root node, parent of itself
    root=TrieNode('*','0','0')
    textPos=0
    path=0
    # loop thru the Text, moving forward one char each time
    # add the line to root, creatine an edge for that string 
    # the add routine will re use starting characters of each suffix as much as it can
    # when each successive suffix differs, it branches off at that point
    # add is the key routine that notes where prefixes overlap and suffixes split off
    while len(Text) >= 1:  #  Text will get shorter each loop as it progresses
       #print(Text)
       add(root,Text,textPos,path)
       Text=Text[1:]
       textPos+=1
       path+=1
    return root

####################################################
#   A key function that adds successive chars to the
#   Trie. Looks for matches from the start, then
#   branches new paths when string differs
#   Assigns new ids and position from the start 
#   This identifies same chars in different positions
# ---------------------------------------------------
#   called by
#   def ModifiedSuffixTrieConstruction(Text): 
#   return root 
####################################################
def add(root, word: str, pos,aPath):
    node=root
    for char in word:
        found_in_child=False
        # search for the char
        for child in node.children:
            if child.char==char:
                #found it
                child.counter+=1
                #point the node to the child
                #continue down this path
                node=child
                found_in_child=True
                break
        # we did not find it so add a new child
        if not found_in_child:
            new_node=TrieNode(char,node,node.id,pos,aPath)
            node.children.append(new_node)
            # now pont the node to the new children
            node=new_node
            pos+=1
    # everything finished, mark it as the end of the word
    node.word_finished = True

##############################################
##############################################
#            Main Program
##############################################
##############################################
if __name__ == "__main__":

    #open and read the file, returning one string, as element 0 of a list, with a $ on the end 
    # This string is the genome, that will be put in a trie where the top part of the tree is shared prefixes, but called a suffix tree
    rawline=readFile()
    #change a list of one string to a list of chars: line
    stri=rawline[0]
    line=[]
    for x in stri:
        line.append(x) 

    Trie=ModifiedSuffixTrieConstruction(line)
    edgeLabels(Trie)
