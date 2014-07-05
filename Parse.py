import re
import sys

from gram_rules import ter, nonter, terminals, nonterminals, parse_table, rules, stack

class tree(object):
    def __init__(self,data,index,parent):
        self.data = data
        self.index=index
        self.no_of_children=0
        self.children=[]
        self.parent=parent
        self.text=''
    def insert_children(self,rule):
        for r in rule:
            (tagtype,tagvalue,tag)=r
            temp_tree=tree(tag,self.no_of_children,self)
            self.children.append(temp_tree)
            self.no_of_children+=1
        
def parser(tokens,no_of_tokens_in_line):
    position=0
    parse_tree=tree('program',0,None)
    parse_tree.parent=parse_tree
    curr_tree=parse_tree
    while len(stack)>0:
        #print(curr_tree.data)
        (tagtype, tagvalue,tag) = stack.pop()
        (toktext,toktag)=tokens[position]
        if tagtype==ter:
            if tagvalue==terminals['eps']:
                index=curr_tree.index
                while curr_tree.parent.no_of_children<=curr_tree.index+1 and curr_tree!=parse_tree:
                    curr_tree=curr_tree.parent
                    index=curr_tree.index
                if curr_tree!=parse_tree:
                    curr_tree=curr_tree.parent.children[index+1]
            elif tagvalue==terminals[toktag]:
                position+=1
                curr_tree.text=toktext
              #  print('pop', tag)
                index=curr_tree.index
                while curr_tree.parent.no_of_children<=curr_tree.index+1 and curr_tree!=parse_tree:
                    curr_tree=curr_tree.parent
                    index=curr_tree.index
                if curr_tree!=parse_tree:
                    curr_tree=curr_tree.parent.children[index+1]
            else:
                a=0
                lin_no=0
                while a<position:
                 #  print(str(lin_no),str(no_of_tokens_in_line[lin_no]))
                   a+=no_of_tokens_in_line[lin_no]
                   lin_no+=1
                lin_no+=1
                sys.stderr.write('Syntax error : line no '+str(lin_no)+' token '+toktext)
                a=re.compile("TK_*")
                if a.match(toktag)!=None:
                    sys.stderr.write(' expects '+tag)
                sys.exit(1)
        elif tagtype==nonter:
           # print('svalue', tag, 'token', toktag)
            ruleno=parse_table[tagvalue][terminals[toktag]]
           # print('rule', ruleno)
            for r in reversed(rules[ruleno]):
                stack.append(r)
            curr_tree.insert_children(rules[ruleno])
            if curr_tree.no_of_children>0:
                curr_tree=curr_tree.children[0]
            else:
                index=curr_tree.index
                while curr_tree.parent.no_of_children<=curr_tree.index+1:
                    curr_tree=curr_tree.parent
                    index=curr_tree.index
                curr_tree=curr_tree.parent.children[index]
            #print('stack', stack)
    return parse_tree

def print_tree(parse_tree):
    print(parse_tree.data)#,parse_tree.text)
    i=0
    while i<parse_tree.no_of_children:
        print_tree(parse_tree.children[i])
        i+=1