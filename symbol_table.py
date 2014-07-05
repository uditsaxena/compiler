class symbol_info(object):
    def __init__(self,name,type):
        self.name=name
        self.type=type
        self.fields=[]
        self.input=[]
        self.output=[]
        self.scope=''
        self.array_size=''
        
def make_symbol_table(parse_tree):
    symbol_table={}
    
    #for record declaration
    temp_tree=parse_tree.children[0]
    while temp_tree.children[0].data!='eps':
        fields=[]
        curr_tree=temp_tree.children[0]
        info1=symbol_info(curr_tree.children[1].text,'record')
        info1.scope='global'
        for symbol in symbol_table:
            if symbol_table[symbol].name==info1.name and symbol_table[symbol].scope==info1.scope:
                sys.stderr.write('Error : multiple records exist with name '+info1.name+'\n')
        curr_tree=curr_tree.children[2]
        sub_tree=curr_tree.children[0]
        info2=symbol_info(sub_tree.children[2].text,sub_tree.children[1].children[0].data)
        if info2.type=='TK_INT':
            info2.type='int'
        elif info2.type=='TK_REAL':
            info2.type='real'
        elif info2.type=='TK_CHAR':
            info2.type='char'
        type=info2.type
        fields.append(info2)
        sub_tree=sub_tree.children[3]
        while sub_tree.children[0].data!='eps':
            info2=symbol_info(sub_tree.children[1].text,type)
            for field in fields:
                if info2.name==field.name:
                    sys.stderr.write('Error : record '+info1.name+' has multiple fields with name '+info2.name)
            fields.append(info2)
            sub_tree=sub_tree.children[2]
        curr_tree=curr_tree.children[1]
        while curr_tree.children[0].data!='eps':
            sub_tree=curr_tree.children[0]
            info2=symbol_info(sub_tree.children[2].text,sub_tree.children[1].children[0].data)
            if info2.type=='TK_INT':
                info2.type='int'
            elif info2.type=='TK_REAL':
                info2.type='real'
            elif info2.type=='TK_CHAR':
                infi2.type='char'
            type=info2.type
            for field in fields:
                if info2.name==field.name:
                    sys.stderr.write('Error : record '+info1.name+' has multiple fields with name '+info2.name)
            fields.append(info2)
            sub_tree=sub_tree.children[3]
            while sub_tree.children[0].data!='eps':
                info2=symbol_info(sub_tree.children[1].text,type)
                for field in fields:
                    if info2.name==field.name:
                        sys.stderr.write('Error : record '+info1.name+' has multiple fields with name '+info2.name+'\n')
                fields.append(info2)
                sub_tree=sub_tree.children[2]
            curr_tree=curr_tree.children[1]
        info1.fields=fields
        symbol_table[(info1.name,info1.scope)]=info1
        temp_tree=temp_tree.children[1]
        
    #for global declaration
    temp_tree=parse_tree.children[1].children[0]
    text=temp_tree.children[3].text
    temp_tree=temp_tree.children[2].children[0]
    if temp_tree.data=='primitiveDatatype':
        type=temp_tree.children[0].data
        if type=='TK_INT':
            type='int'
        elif type=='TK_REAL':
            type='real'
        elif type=='TK_CHAR':
            type='char'
    elif temp_tree.data=='constructedDatatype':
        type='record '+temp_tree.children[1].text
        flag=0
        for symbol in symbol_table:
            if symbol_table[symbol].type=='record' and symbol_table[symbol].name==temp_tree.children[1].text:
                flag=1
        if flag==0:
            sys.stderr.write('Error : data type record '+temp_tree.children[1].text+' does not exist. Hence cannot declare global variable'+text+'\n')
    info=symbol_info(text,type)
    info.scope='global'
    for symbol in symbol_table:
        if symbol_table[symbol].name==info.name and symbol_table[symbol].scope==info.scope:
            sys.stderr.write('Error : name conflict while declaring global variable '+info.name+'\n')
    symbol_table[(text,info.scope)]=info
    
    #for function definition
    temp_tree=parse_tree.children[2]
    while temp_tree.children[0].data!='eps':
        input=[]
        output=[]
        curr_tree=temp_tree.children[0]
        info=symbol_info(curr_tree.children[1].text,'function')
        info.scope='global'
        for symbol in symbol_table:
            if symbol_table[symbol].name==info.name and symbol_table[symbol].scope==info.scope:
                sys.stderr.write('Error : multiple functions exist with name '+info.name+'\n')
        
        #function input
        curr_tree=curr_tree.children[2].children[2]
        sub_tree=curr_tree
        while sub_tree.children[0].data!='eps':
            text=curr_tree.children[2].text
            curr_tree=curr_tree.children[1].children[0]
            if curr_tree.data=='primitiveDatatype':
                type=curr_tree.children[0].data
                if type=='TK_INT':
                    type='int'
                elif type=='TK_REAL':
                    type='real'
                elif type=='TK_CHAR':
                    type='char'
            elif curr_tree.data=='constructedDatatype':
                type='record '+curr_tree.children[1].text
                flag=0
                for symbol in symbol_table:
                    if symbol_table[symbol].type=='record' and symbol_table[symbol].name==curr_tree.children[1].text:
                        flag=1
                if flag==0:
                    sys.stderr.write('Error : data type record '+curr_tree.children[1].text+' does not exist. Hence cannot declare input variable '+text+'in function '+info.name+'\n')
            info2=symbol_info(text,type)
            for inp in input:
                if inp.name==info2.name:
                    sys.stderr.write('Error : function '+info.name+' has multiple inputs with name '+info2.name+'\n')
            input.append(info2)
            sub_tree=sub_tree.children[3]
            if sub_tree.children[0].data=='eps':
                break
            else:
                sub_tree=sub_tree.children[1]
            curr_tree=sub_tree
        info.input=input
        
        #function output
        curr_tree=temp_tree.children[0]
        curr_tree=curr_tree.children[3].children[2]
        sub_tree=curr_tree
        while sub_tree.children[0].data!='eps':
            text=curr_tree.children[2].text
            curr_tree=curr_tree.children[1].children[0]
            if curr_tree.data=='primitiveDatatype':
                type=curr_tree.children[0].data
                if type=='TK_INT':
                    type='int'
                elif type=='TK_REAL':
                    type='real'
                elif type=='TK_CHAR':
                    type='char'
            elif curr_tree.data=='constructedDatatype':
                type='record '+curr_tree.children[1].text
                flag=0
                for symbol in symbol_table:
                    if symbol_table[symbol].type=='record' and symbol_table[symbol].name==curr_tree.children[1].text:
                        flag=1
                if flag==0:
                    sys.stderr.write('Error : data type record '+curr_tree.children[1].text+' does not exist. Hence cannot declare output variable '+text+'in function '+info.name+'\n')
            info2=symbol_info(text,type)
            for op in output:
                if op.name==info2.name:
                    sys.stderr.write('Error : function '+info.name+' has multiple outputs with name '+info2.name+'\n')
            output.append(info2)
            sub_tree=sub_tree.children[3]
            if sub_tree.children[0].data=='eps':
                break
            else:
                sub_tree=sub_tree.children[1]
            curr_tree=sub_tree
        info.output=output
        
        symbol_table[(info.name,info.scope)]=info

        #function declarations
        curr_tree=temp_tree.children[0]
        curr_tree=curr_tree.children[4].children[0]
        sub_tree=curr_tree
        while sub_tree.children[0].data!='eps':
            curr_tree=curr_tree.children[0].children[0]
            if curr_tree.data=='declaration':
                text=curr_tree.children[2].text
                curr_tree=curr_tree.children[1].children[0]
                if curr_tree.data=='primitiveDatatype':
                    type=curr_tree.children[0].data
                    if type=='TK_INT':
                        type='int'
                    elif type=='TK_REAL':
                        type='real'
                    elif type=='TK_CHAR':
                        type='char'
                elif curr_tree.data=='constructedDatatype':
                    type='record '+curr_tree.children[1].text
                    flag=0
                    for symbol in symbol_table:
                        if symbol_table[symbol].type=='record' and symbol_table[symbol].name==curr_tree.children[1].text:
                            flag=1
                    if flag==0:
                        sys.stderr.write('Error : data type record '+curr_tree.children[1].text+' does not exist. Hence cannot declare variable '+text+'in function '+info.name+'\n')
                info2=symbol_info(text,type)
                info2.scope='function '+info.name
                for symbol in symbol_table:
                    if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                        sys.stderr.write('Error : multiple variables exist with name '+info2.name+' in function '+info.name+'\n')
                symbol_table[(text,info2.scope)]=info2
                curr_tree=sub_tree.children[0].children[0].children[3]
                while curr_tree.children[0].data!='eps':
                    text=curr_tree.children[1].text
                    info2=symbol_info(text,type)
                    info2.scope='function '+info.name
                    for symbol in symbol_table:
                        if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                            sys.stderr.write('Error : multiple variables exist with name '+info2.name+' in function '+info.name+'\n')
                    symbol_table[(text,info2.scope)]=info2
                    curr_tree=curr_tree.children[2]
                
            elif curr_tree.data=='array_declaration':
                type=curr_tree.children[1].children[0].data
                if type=='TK_INT':
                    type='array int'
                elif type=='TK_REAL':
                    type='array real'
                elif type=='TK_CHAR':
                    type='array char'
                text=curr_tree.children[2].text
                info2=symbol_info(text,type)
                info2.scope='function'+info.name
                info2.array_size=curr_tree.children[4].text
                for symbol in symbol_table:
                    if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                        sys.stderr.write('Error : multiple array variables exist with name '+info2.name+' in function '+info.name+'\n')
                symbol_table[(text,info2.scope)]=info2
                curr_tree=curr_tree.children[6]
                if curr_tree.children[0].data!='eps':
                    text=curr_tree.children[1].text
                    info2=symbol_info(text,type)
                    info2.scope='function'+info.name
                    info2.array_size=curr_tree.children[3].text
                    for symbol in symbol_table:
                        if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                            sys.stderr.write('Error : multiple array variables exist with name '+info2.name+' in function '+info.name+'\n')
                    symbol_table[(text,info2.scope)]=info2
                    
            elif curr_tree.data=='map_declaration':
                type=curr_tree.children[1].children[0].data
                if type=='TK_INT':
                    type='map int'
                elif type=='TK_REAL':
                    type='map real'
                elif type=='TK_CHAR':
                    type='map char'
                text=curr_tree.children[2].text
                info2=symbol_info(text,type)
                info2.scope='function'+info.name
                for symbol in symbol_table:
                    if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                        sys.stderr.write('Error : multiple map variables exist with name '+info2.name+' in function '+info.name+'\n')
                symbol_table[(text,info2.scope)]=info2
                curr_tree=curr_tree.children[3]
                while curr_tree.children[0].data!='eps':
                    text=curr_tree.children[1].text
                    info2=symbol_info(text,type)
                    info2.scope='function'+info.name
                    for symbol in symbol_table:
                        if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                            sys.stderr.write('Error : multiple map variables exist with name '+info2.name+' in function '+info.name+'\n')
                    symbol_table[(text,info2.scope)]=info2
                    curr_tree=curr_tree.children[2]
            sub_tree=sub_tree.children[1]
            curr_tree=sub_tree
        temp_tree=temp_tree.children[1]
        
        
    #for main
    temp_tree=parse_tree.children[3]
    curr_tree=temp_tree.children[1].children[0]
    sub_tree=curr_tree
    while sub_tree.children[0].data!='eps':
        curr_tree=curr_tree.children[0].children[0]    
        if curr_tree.data=='declaration':
            text=curr_tree.children[2].text
            curr_tree=curr_tree.children[1].children[0]
            if curr_tree.data=='primitiveDatatype':
                type=curr_tree.children[0].data
                if type=='TK_INT':
                    type='int'
                elif type=='TK_REAL':
                    type='real'
                elif type=='TK_CHAR':
                    type='char'
            elif curr_tree.data=='constructedDatatype':
                type='record '+curr_tree.children[1].text
                flag=0
                for symbol in symbol_table:
                    if symbol_table[symbol].type=='record' and symbol_table[symbol].name==curr_tree.children[1].text:
                        flag=1
                if flag==0:
                    sys.stderr.write('Error : data type record '+curr_tree.children[1].text+' does not exist. Hence cannot declare variable '+text+' in main'+'\n')
            info2=symbol_info(text,type)
            info2.scope='main'
            for symbol in symbol_table:
                if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                    sys.stderr.write('Error : multiple variables exist with name '+info2.name+' in main\n')
            symbol_table[(text,info2.scope)]=info2
            curr_tree=sub_tree.children[0].children[0].children[3]
            while curr_tree.children[0].data!='eps':
                text=curr_tree.children[1].text
                info2=symbol_info(text,type)
                info2.scope='main'
                for symbol in symbol_table:
                    if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                        sys.stderr.write('Error : multiple variables exist with name '+info2.name+' in main\n')
                symbol_table[(text,info2.scope)]=info2
                curr_tree=curr_tree.children[2]
            
        elif curr_tree.data=='array_declaration':
            type=curr_tree.children[1].children[0].data
            if type=='TK_INT':
                type='array int'
            elif type=='TK_REAL':
                type='array real'
            elif type=='TK_CHAR':
                type='array char'
            text=curr_tree.children[2].text
            info2=symbol_info(text,type)
            info2.scope='main'
            info2.array_size=curr_tree.children[4].text
            for symbol in symbol_table:
                if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                    sys.stderr.write('Error : multiple array variables exist with name '+info2.name+' in main\n')
            symbol_table[(text,info2.scope)]=info2
            curr_tree=curr_tree.children[6]
            if curr_tree.children[0].data!='eps':
                text=curr_tree.children[1].text
                info2=symbol_info(text,type)
                info2.scope='main'
                info2.array_size=curr_tree.children[3].text
                for symbol in symbol_table:
                    if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                        sys.stderr.write('Error : multiple array variables exist with name '+info2.name+' in main\n')
                symbol_table[(text,info2.scope)]=info2
                    
        elif curr_tree.data=='map_declaration':
            type=curr_tree.children[1].children[0].data
            if type=='TK_INT':
                type='map int'
            elif type=='TK_REAL':
                type='map real'
            elif type=='TK_CHAR':
                type='map char'
            text=curr_tree.children[2].text
            info2=symbol_info(text,type)
            info2.scope='main'
            for symbol in symbol_table:
                if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                    sys.stderr.write('Error : multiple map variables exist with name '+info2.name+' in main\n')
            symbol_table[(text,info2.scope)]=info2
            curr_tree=curr_tree.children[3]
            while curr_tree.children[0].data!='eps':
                text=curr_tree.children[1].text
                info2=symbol_info(text,type)
                info2.scope='main'
                for symbol in symbol_table:
                    if symbol_table[symbol].name==info2.name and symbol_table[symbol].scope==info2.scope:
                        sys.stderr.write('Error : multiple map variables exist with name '+info2.name+' in main\n')
                symbol_table[(text,info2.scope)]=info2
                curr_tree=curr_tree.children[2]
        sub_tree=sub_tree.children[1]
        curr_tree=sub_tree
    return symbol_table
