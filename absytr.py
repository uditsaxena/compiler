from Parse import tree

def find_arithmetic_tree(ast,parent,index):
    if ast.children[0].data=='TK_OP':
        if ast.children[3].children[0].data=='operator':
            new_ast=tree(ast.children[3].children[0].children[0].data,index,parent)
            new_ast1=find_arithmetic_tree(ast.children[1],new_ast,0)
            new_ast2=find_arithmetic_tree(ast.children[3].children[1],new_ast,1)
            new_ast.children.append(new_ast1)
            new_ast.children.append(new_ast2)
            new_ast.no_of_children=2
        else:
            new_ast=find_arithmetic_tree(ast.children[1],parent,index)
    elif ast.children[0].data=='variable':
        if ast.children[1].children[0].data=='arithmeticExpression':
            if ast.children[0].children[0].data=='TK_ID' or ast.children[0].children[0].data=='TK_NUM' or ast.children[0].children[0].data=='TK_RNUM' or ast.children[0].children[0].data=='TK_CHR':
                new_ast=tree(ast.children[0].children[0].text,index,parent)
            elif ast.children[0].children[0].data=='TK_ARRAYID':
                new_ast=tree(ast.children[0].children[0].text,index,parent)
                new_ast.text=ast.children[0].children[2].children[0].text
            elif ast.children[0].children[0].data=='TK_RECORDID':
                new_ast=tree(ast.children[0].children[0].text,index,parent)
                new_ast.text=ast.children[0].children[2].text
            elif ast.children[0].children[0].data=='TK_MAPID':
                new_ast=tree(ast.children[0].children[0].text,index,parent)
                new_ast.text=ast.children[0].children[2].text
        elif ast.children[1].children[0].data=='operator':
            new_ast=tree(ast.children[1].children[0].children[0].data,index,parent)
            if ast.children[0].children[0].data=='TK_ID' or ast.children[0].children[0].data=='TK_NUM' or ast.children[0].children[0].data=='TK_RNUM' or ast.children[0].children[0].data=='TK_CHR':
                new_ast1=tree(ast.children[0].children[0].text,0,new_ast)
            elif ast.children[0].children[0].data=='TK_ARRAYID':
                new_ast1=tree(ast.children[0].children[0].text,0,new_ast)
                new_ast1.text=ast.children[0].children[2].children[0].text
            elif ast.children[0].children[0].data=='TK_RECORDID':
                new_ast1=tree(ast.children[0].children[0].text,0,new_ast)
                new_ast1.text=ast.children[0].children[2].text
            elif ast.children[0].children[0].data=='TK_MAPID':
                new_ast1=tree(ast.children[0].children[0].text,0,new_ast)
                new_ast1.text=ast.children[0].children[2].text
            new_ast2=find_arithmetic_tree(ast.children[1].children[1],new_ast,1)
            new_ast.children.append(new_ast1)
            new_ast.children.append(new_ast2)
            new_ast.no_of_children=2
    return new_ast

def find_boolean_tree(ast,parent,index):
    if ast.children[0].data == 'TK_OP':
        if ast.children[2].children[0].data == 'Op': # <- using Op,booleanExpression,TK_CL expansion now.
            new_ast2=tree(ast.children[2].children[0].children[0].children[0].data,0,parent)
            new_ast1=find_boolean_tree(ast.children[1],new_ast2,0) # new_ast1 to be inserted first, 
            new_ast3=find_boolean_tree(ast.children[2].children[1],new_ast2,1)
            new_ast2.children.append(new_ast1)
            new_ast2.children.append(new_ast3)
            new_ast2.no_of_children=2
            return new_ast2
        else:
            new_ast1=find_boolean_tree(ast.children[1],parent,0)
            return new_ast1 # expression was of the form : (booleanExpression)
    elif ast.children[0].data == 'variable':
        if ast.children[0].children[0].data=='TK_ID' or ast.children[0].children[0].data=='TK_NUM' or ast.children[0].children[0].data=='TK_RNUM' or ast.children[0].children[0].data=='TK_CHR':
            new_ast=tree(ast.children[0].children[0].text,index,parent)
        elif ast.children[0].children[0].data=='TK_ARRAYID':
            new_ast=tree(ast.children[0].children[0].text,index,parent)
            new_ast.text=ast.children[0].children[2].children[0].text
        elif ast.children[0].children[0].data=='TK_RECORDID':
            new_ast=tree(ast.children[0].children[0].text,index,parent)
            new_ast.text=ast.children[0].children[2].text # some error overcoming the variable record id here
        elif ast.children[0].children[0].data=='TK_MAPID':
            new_ast=tree(ast.children[0].children[0].text,index,parent)
            new_ast.text=ast.children[0].children[2].text
        return new_ast
    elif ast.children[0].data == 'TK_NOT':
        new_ast1=tree('TK_NOT',index,parent) # needs to have the same index as parent as it is being pulled up and reduced at the same time.
        new_ast2=find_boolean_tree(ast.children[1],new_ast1,0)
        new_ast1.children.append(new_ast2)
        new_ast1.no_of_children+=1
        return new_ast1

def make_elif_ast(el_tree,if_ast):
    i=2
    if el_tree.children[0].data != 'eps':
        temp_tree=el_tree.children[0]        
        while(temp_tree.children[0].data != 'eps'):
            #print(temp_tree.data)
            new_ast=tree('ELSEIF',i,if_ast)
            if_ast.children.append(new_ast)
            if_ast.no_of_children+=1
            bool_tree=temp_tree.children[0].children[1]
            new_ast1=find_boolean_tree(bool_tree,new_ast,0)
            new_ast.children.append(new_ast1)
            new_ast.no_of_children+=1
            #
            new_ast1=tree('THEN',1,new_ast)
            new_ast.children.append(new_ast1)
            new_ast.no_of_children+=1
            #
            a_stmt=temp_tree.children[0].children[2]
            a_otherStmt=temp_tree.children[0].children[3]
            a_big_otherStmt=tree(a_otherStmt.data,0,new_ast)
            a_stmt.index=0
            a_stmt.parent=a_big_otherStmt
            a_otherStmt.index=1
            a_otherStmt.parent=a_big_otherStmt
            a_big_otherStmt.children.append(a_stmt)
            a_big_otherStmt.children.append(a_otherStmt)
            a_big_otherStmt.no_of_children=2
            # ^ merged, above
            make_otherStmt_ast(a_big_otherStmt,new_ast1)
            # ^ done one elsif above
            # now, increment i, temp_tree and move on.
            i+=1
            temp_tree=temp_tree.children[1]
        #check whether else condition exists or not.
    if(el_tree.children[1].data != 'eps'):
        new_ast=tree('ELSE',i,if_ast)
        if_ast.children.append(new_ast)
        if_ast.no_of_children+=1
        a_stmt=el_tree.children[1].children[1]
        a_otherStmt=el_tree.children[1].children[2]
        a_big_otherStmt=tree(a_otherStmt.data,0,new_ast)
        a_stmt.index=0
        a_stmt.parent=a_big_otherStmt
        a_otherStmt.index=1
        a_otherStmt.parent=a_big_otherStmt
        a_big_otherStmt.children.append(a_stmt)
        a_big_otherStmt.children.append(a_otherStmt)
        a_big_otherStmt.no_of_children=2
        # ^ merged, above
        make_otherStmt_ast(a_big_otherStmt,new_ast)

def make_list_ast(curr_tree,curr_ast):
    i=0
    temp_tree=curr_tree.children[0]
    id_tree=tree(temp_tree.text,i,curr_ast)
    id_tree.text=temp_tree.text
    curr_ast.children.append(id_tree)
    curr_ast.no_of_children+=1
    i+=1
    temp_tree=curr_tree.children[1]
    while(temp_tree.children[0].data != 'eps'):
        curr_tree=temp_tree.children[1]
        temp_tree=curr_tree.children[0]
        id_tree=tree(temp_tree.text,i,curr_ast)
        id_tree.text=temp_tree.text
        curr_ast.children.append(id_tree)
        curr_ast.no_of_children+=1
        i+=1
        temp_tree=curr_tree.children[1]

def make_otherStmt_ast(curr_tree,curr_ast):
    while curr_tree.children[0].data != 'eps':
        temp_index=0
        sub_tree=curr_tree.children[0].children[0] # <-OtherStmts ka stmt ka child = sub_tree
        if sub_tree.data=='assignStmt':
            new_ast=tree('TK_ASSIGN',temp_index,curr_ast)
            curr_ast.children.append(new_ast)
            curr_ast.no_of_children+=1
            temp_index+=1
            a_tree=sub_tree.children[1]
            if a_tree.children[0].data=='TK_ID':
                new_ast1=tree(a_tree.children[0].text,new_ast,0)
            elif a_tree.children[0].data=='TK_RECORDID':
                new_ast1=tree(a_tree.children[0].text,new_ast,0)
                new_ast1.text=a_tree.children[2].text
            elif a_tree.children[0].data=='TK_ARRAYID':
                new_ast1=tree(a_tree.children[0].text,new_ast,0)
                new_ast.text=a_tree.children[2].children[0].text
            new_ast.children.append(new_ast1)
            new_ast.no_of_children+=1    
            a_tree=sub_tree.children[3]
            new_ast1=find_arithmetic_tree(a_tree,new_ast,1)
            new_ast.children.append(new_ast1)
            new_ast.no_of_children+=1
            curr_tree=curr_tree.children[1]
        elif sub_tree.data=='iterativeStmt':
            new_ast=tree('TK_WHILE',temp_index,curr_ast)
            curr_ast.children.append(new_ast)
            curr_ast.no_of_children+=1
            temp_index+=1
            new_ast1=tree('TK_WHILE_CONDITION',0,new_ast)
            new_ast.children.append(new_ast1)
            new_ast.no_of_children+=1
            a_tree=sub_tree.children[1]# <- booleanExpression is in a_tree
            new_ast2=find_boolean_tree(a_tree,new_ast1,0)
            #now insert into new_ast1
            new_ast1.children.append(new_ast2)
            new_ast1.no_of_children+=1
            #now the stmt,otherStmts
            # inserting a new node, while body
            new_ast1=tree('TK_WHILE_BODY',1,new_ast)
            new_ast.children.append(new_ast1)
            new_ast.no_of_children+=1
            #now we have stmt,otherStmt; Merge them into a bigger otherStmt
            a_stmt=sub_tree.children[2]
            a_otherStmt=sub_tree.children[3]
            a_big_otherStmt=tree(a_otherStmt.data,2,sub_tree)
            a_stmt.index=0
            a_stmt.parent=a_big_otherStmt
            a_otherStmt.index=1
            a_otherStmt.parent=a_big_otherStmt
            a_big_otherStmt.children.append(a_stmt)
            a_big_otherStmt.children.append(a_otherStmt)
            a_big_otherStmt.no_of_children=2
            #
            # ^ merged, above.
            #
            make_otherStmt_ast(a_big_otherStmt,new_ast1)
            curr_tree=curr_tree.children[1]
        elif sub_tree.data == 'conditionalStmt':
            #print('Conditional !')
            new_ast=tree('TK_IF',temp_index,curr_ast)
            curr_ast.children.append(new_ast)
            curr_ast.no_of_children+=1
            temp_index+=1
            bool_tree = sub_tree.children[1]
            #print(bool_tree.data)
            new_ast1=find_boolean_tree(bool_tree,new_ast,0)
            new_ast.children.append(new_ast1)
            new_ast.no_of_children+=1
            new_ast1=tree('THEN',1,new_ast)
            new_ast.children.append(new_ast1)
            new_ast.no_of_children+=1
            a_stmt=sub_tree.children[2]
            a_otherStmt=sub_tree.children[3]
            a_big_otherStmt=tree(a_otherStmt.data,2,sub_tree)
            a_stmt.index=0
            a_stmt.parent=a_big_otherStmt
            a_otherStmt.index=1
            a_otherStmt.parent=a_big_otherStmt
            a_big_otherStmt.children.append(a_stmt)
            a_big_otherStmt.children.append(a_otherStmt)
            a_big_otherStmt.no_of_children=2
            # ^ merged, above
            make_otherStmt_ast(a_big_otherStmt,new_ast1)
            #now dealing with else and elseifs
            elif_el_tree = sub_tree.children[4]
            make_elif_ast(elif_el_tree,new_ast)
            curr_tree=curr_tree.children[1]
        elif sub_tree.data == 'ioStmt':
            if(sub_tree.children[0].data == 'TK_GET'):
                new_ast=tree('GET',temp_index,curr_ast)
                curr_ast.children.append(new_ast)
                curr_ast.no_of_children+=1
                temp_index+=1
                if sub_tree.children[1].children[0].data=='TK_ID' :
                    new_ast1=tree(sub_tree.children[1].children[0].text,0,new_ast)
                elif sub_tree.children[1].children[0].data=='TK_ARRAYID':
                    new_ast1=tree(sub_tree.children[1].children[2].children[0].text,0,new_ast)
                    new_ast1.text=sub_tree.children[1].children[2].children[0].text
                elif sub_tree.children[1].children[0].data=='TK_RECORDID':
                    new_ast1=tree(sub_tree.children[1].children[2].text,0,new_ast)
                    new_ast1.text=sub_tree.children[1].children[2].text 
                new_ast.children.append(new_ast1)
                new_ast.no_of_children+=1

            elif(sub_tree.children[0].data == 'TK_PUT'):
                new_ast=tree('PUT',temp_index,curr_ast)
                curr_ast.children.append(new_ast)
                curr_ast.no_of_children+=1
                temp_index+=1
                if sub_tree.children[1].children[0].data=='TK_ID' :
                    new_ast1=tree(sub_tree.children[1].children[1].text,0,new_ast)
                elif sub_tree.children[1].children[0].data=='TK_ARRAYID':
                    new_ast1=tree(sub_tree.children[1].children[2].text,0,new_ast)
                    new_ast1.text=sub_tree.children[1].children[2].children[0].text
                elif sub_tree.children[1].children[0].data=='TK_RECORDID':
                    new_ast1=tree(sub_tree.children[1].children[2].text,0,new_ast)
                    new_ast1.text=sub_tree.children[1].children[2].text 
                new_ast.children.append(new_ast1)
                new_ast.no_of_children+=1
            else:
                # data = TK_PUTS
                new_ast=tree('PUTS',temp_index,curr_ast)
                curr_ast.children.append(new_ast)
                curr_ast.no_of_children+=1
                temp_index+=1
                new_ast1=tree(sub_tree.children[1].text,0,new_ast)
                new_ast1.text=sub_tree.children[1].text
                new_ast.children.append(new_ast1)
                new_ast.no_of_children+=1
                
            curr_tree=curr_tree.children[1]
        elif sub_tree.data == 'funCallStmt':
            new_ast=tree('funCall',temp_index,curr_ast)
            curr_ast.children.append(new_ast)
            curr_ast.no_of_children+=1
            temp_index+=1
            new_ast.text=sub_tree.children[1].text 
            # ^ in data, we store funCall, while in text, we store the name of the function being called
            i=0
            if(sub_tree.children[3].children[0].data!='eps'):
                ast_l=tree('input',i,new_ast)
                make_list_ast(sub_tree.children[3],ast_l)
                new_ast.children.append(ast_l)
                new_ast.no_of_children+=1
                i+=1
            if(sub_tree.children[6].children[0].data!='eps'):
                ast_r=tree('output',i,new_ast)
                make_list_ast(sub_tree.children[6],ast_r)
                new_ast.children.append(ast_r)
                new_ast.no_of_children+=1
                i+=1
            curr_tree=curr_tree.children[1]
        elif sub_tree.data == 'mapStmt':
            new_ast=tree(sub_tree.children[0].children[0].data,temp_index,curr_ast)
            curr_ast.children.append(new_ast)
            curr_ast.no_of_children+=1
            temp_index+=1
            if(sub_tree.children[0].data == 'mapAdd'):
                #mapAdd stuff now
                new_ast1=tree(sub_tree.children[0].children[1].text,0,new_ast)
                new_ast.children.append(new_ast1)
                new_ast.no_of_children+=1
                new_ast1=tree(sub_tree.children[0].children[3].text,1,new_ast)
                new_ast.children.append(new_ast1)
                new_ast.no_of_children+=1
                if sub_tree.children[0].children[5].children[0].data=='TK_ID' or sub_tree.children[0].children[5].children[0].data=='TK_NUM' or sub_tree.children[0].children[5].children[0].data=='TK_RNUM' or sub_tree.children[0].children[5].children[0].data=='TK_CHR':
                    new_ast2=tree(sub_tree.children[0].children[5].children[0].text,2,new_ast)
                elif sub_tree.children[0].children[5].children[0].data=='TK_ARRAYID':
                    new_ast2=tree(sub_tree.children[0].children[5].children[0].text,2,new_ast)
                    new_ast2.text=sub_tree.children[0].children[5].children[0].text
                elif sub_tree.children[0].children[5].children[0].data=='TK_RECORDID':
                    new_ast2=tree(sub_tree.children[0].children[5].children[0].text,2,new_ast)
                    new_ast2.text=sub_tree.children[0].children[5].children[2].text # some error overcoming the variable record id here
                elif sub_tree.children[0].children[5].children[0].data=='TK_MAPID':
                    new_ast2=tree(sub_tree.children[0].children[5].children[0].text,2,new_ast)
                    new_ast2.text=sub_tree.children[0].children[5].children[2].text
                new_ast.children.append(new_ast2)
                new_ast.no_of_children+=1
            else:#mapDelete stuff now
                new_ast1=tree(sub_tree.children[0].children[1].text,0,new_ast) 
                new_ast.children.append(new_ast1)
                new_ast.no_of_children+=1
                new_ast1=tree(sub_tree.children[0].children[3].text,1,new_ast) 
                new_ast.children.append(new_ast1)
                new_ast.no_of_children+=1
                
            curr_tree=curr_tree.children[1]
        else:
            curr_tree=curr_tree.children[1]

def make_ast(parse_tree):
    if(parse_tree.data=='program'):
        ast=tree('program',0,None)
        ast.parent=ast
        curr_ast=ast
        curr_index=0
    else:
        ast=tree(parse_tree)
    
    #for global assignments
    temp_tree=parse_tree.children[1]
    if temp_tree.children[0]!='eps':
        temp_tree=temp_tree.children[1]
        if temp_tree.children[0]!='eps':
            new_ast=tree('global',0,curr_ast)
            curr_ast.children.append(new_ast)
            curr_ast.no_of_children+=1
            curr_index+=1
            curr_ast=new_ast
            new_ast=tree('TK_ASSIGN',0,curr_ast)
            curr_ast.children.append(new_ast)
            curr_ast.no_of_children+=1
            curr_ast=new_ast
            new_ast=tree(temp_tree.children[1].text,0,curr_ast)
            curr_ast.children.append(new_ast)
            curr_ast.no_of_children+=1
            new_ast2=tree(temp_tree.children[3].children[0].text,1,curr_ast)
            curr_ast.children.append(new_ast2)
            curr_ast.no_of_children+=1
            
    #for function statements
    temp_tree=parse_tree.children[2]
    while temp_tree.children[0].data!='eps':
        curr_ast=ast
        curr_tree=temp_tree.children[0] #curr_tree=function
        new_ast=tree(curr_tree.children[1].text,curr_index,curr_ast) # <- funID
        curr_ast.children.append(new_ast)
        curr_ast.no_of_children+=1
        curr_index+=1
        curr_ast=new_ast # <- going deeper and deeper into funID
        curr_tree=curr_tree.children[4].children[1] # <- funID's stmt_s's OtherStmts = curr_tree (point 22 in new_gram)
        make_otherStmt_ast(curr_tree,curr_ast)
        temp_tree=temp_tree.children[1]
    
    #for main function statements
    temp_tree=parse_tree.children[3]
    curr_ast=ast
    new_ast=tree('MAIN',curr_index,curr_ast) # <- Main
    curr_ast.children.append(new_ast)
    curr_ast.no_of_children+=1
    curr_index+=1
    curr_ast=new_ast
    curr_tree=temp_tree.children[1].children[1]
    make_otherStmt_ast(curr_tree,curr_ast)

    return ast
