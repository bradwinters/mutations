import numpy as np
from typing import Tuple

class TrieNode(object):
    # Function to initialize the node
    Node_counter=0
    LongestB=0
    def __init__(self, char: str, charp: str):
        self.char=char
        self.parent=charp
        self.children = []
        self.word_finished=False
        self.counter=1
        self.id=TrieNode.Node_counter
        TrieNode.Node_counter+=1

    def find_child(self,asymbol):
        for i in self.children: 
            if i.char==asymbol:
                return i 
        return 0 



def add(root, word: str):
    node=root
    for char in word:
        found_in_child=False
        # search for the char
        for child in node.children:
            if child.char==char:
                #found it
                child.counter+=1
                #point the node to the child
                node=child
                found_in_child=True
                break
        # we did not find it so add a new child
        if not found_in_child:
            new_node=TrieNode(char,node.id)
            node.children.append(new_node)
            # now pont the node to the new children
            node=new_node
    # everything finished, mark it as the end of the word
    node.word_finished = True

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
            str="{}->{}:{}"
            if p.char !='*': 
               print(str.format(p.parent,p.id,p.char))
               print(p.word_finished)
            #print(str.format(p.parent,p.id,p.char))
            
            for index, value in enumerate(p.children):
                queue.append(value)
            n -=1
            #print ("")

def readFile():
    """  include any needed header processing or stripping 
                  
    """
    #f=open("ex2s.dat","r")
    #f=open("ex2.dat","r")
    f=open("test.dat","r")
    j=[]
    for l in f:
       l=l.strip() 
       j.append(l)
    return j

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
        # check if vNodes.char matches symbol.  If so progress both down the child that has that symbol and in text
        nextVnode=vNode.find_child(symbol)
        if nextVnode !=0: 
            #print("Found match ",symbol)
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


def printList(aList):
    str="{} "
    #    print(str.format(root.id,x.id,x.char))
    for j in aList:
        print(str.format(j),end="")


if __name__ == "__main__":

    #create the root by constructing the root node, parent of itself
    root=TrieNode('*','0')
    #open and read the file, returning a list of lists, line 0 is the text, the others are patterns
    lines=readFile()
    cntr=0
    for line in lines:
       if cntr==0:  # line 0 is the big text line
          Text=line
          cntr+=1
       else:
          #create a Trie with remaining lines of patterns
          add(root,line)


    #str="{}->{}:{}"
    #for x in root.children:
    #    print(str.format(root.id,x.id,x.char))
    #print("--------------------------")
    #printNodeLevelWise(root)

    daPath=TrieMatching(Text,root)
    printList(daPath)

