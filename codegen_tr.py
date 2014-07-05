# Code Generator

readProc = "\
_read proc\n\
    mov dx, offset inputbuf\n\
    mov bx, dx\n\
    mov byte ptr[bx], 10\n\
    mov ah, 0ah\n\
    int 21h\n\
    \n\
    mov ah, 02h\n\
    mov dl, 10\n\
    int 21h\n\
    \n\
    mov bx, offset inputbuf + 1\n\
    mov cx, 0\n\
    mov cl, [bx]\n\
    mov ax, 0\n\
    _getdigitfrombuf:\n\
        inc bx\n\
        mov dx, 10\n\
        mul dx\n\
        mov dh, 0\n\
        mov dl, [bx]\n\
        sub dx, 48\n\
        add ax, dx\n\
        \n\
        loop _getdigitfrombuf\n\
    ret\n\
_read endp"

writeProc = "\
_write proc\n\
    mov bx, ax\n\
    and bx, 8000h\n\
    cmp bx, 0\n\
    je _writesignhandled\n\
    not ax\n\
    add ax, 1\n\
    mov bx, ax\n\
    mov ah, 02h\n\
    mov dl, 45\n\
    int 21h\n\
    mov ax, bx\n\
    \n\
    _writesignhandled:\n\
    mov cx, 0\n\
    mov bx, 10\n\
    mov dx, 0\n\
    _getdigitfromnum:\n\
        div bx\n\
        \n\
        push dx\n\
        inc cx\n\
        \n\
        mov dx, 0\n\
        \n\
        cmp ax, 0\n\
        jne _getdigitfromnum\n\
        \n\
        mov ah, 02h\n\
    \n\
    _writedigit:\n\
        pop dx\n\
        add dl, 48\n\
        int 21h\n\
        \n\
        dec cx\n\
        cmp cx, 0\n\
        jne _writedigit\n\
    ret\n\
_write endp"

#Counting loops and if into buffers


def codegen(ast,f):
    #f is already open
    #main: generating code
    if(ast.data=='program'):
        f.write('.model small\n.stack\n\n.code\n\n'+readProc+'\n\n'+writeProc+'\n\n')
        codegen(ast.children[2],f)
        # now look for the main function and we enter it and code it
        f.write('.data\n')
        f.write('inputbuf db 12 dup(0)\n')
        # this is for declarations
        #codegen((ast.children[1].children[1].children[1]),f)
        f.write('\nend main')
    elif(ast.data=='global'):
        i=0
        while(i<ast.no_of_children):
            codegen(ast.children[i],f)
            i+=1

    elif(ast.data=='MAIN'):
        f.write('main proc\n\nmov ax, seg inputbuf\nmov ds, ax\n\n')
        i=0
        while(i<ast.no_of_children):
            codegen(ast.children[i],f)
            i+=1
            #^ go through the children of main
    elif(ast.data=='TK_ASSIGN'):
        if(ast.children[1].no_of_children != 1):
            codegen(ast.children[1],f)
        else:
            f.write('mov ax, '+ast.children[1].data+'\n')
        f.write('mov bx, '+ast.children[0].data+'\n\n')
    elif(ast.data=='TK_PLUS'):
        f.write('mov ax,'+ast.children[0].data+'\n')
        f.write('push ax\n')
        if(ast.children[1].no_of_children != 0):
            codegen(ast.children[1],f)
        else:
            f.write('mov ax,'+ast.children[1].data+'\n')
        f.write('mov bx, ax\npop ax\n')
        f.write('add ax, bx\n\n')
    elif(ast.data=='TK_MINUS'):
        f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('push ax\n')
        if(ast.children[1].no_of_children != 0):
            codegen(ast.children[1],f)
        else:
            f.write('mov ax, '+ast.children[1].data+'\n')
        f.write('mov bx, ax\npop ax\n')
        f.write('sub ax, bx\n\n')
    elif(ast.data=='TK_MUL'):
        f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('push ax\n')
        if(ast.children[1].no_of_children != 0):
            codegen(ast.children[1],f)
        else:
            if(ast.children[1].data==2):
                f.write('mov ax, '+ast.children[1].data+'\n')
                f.write('add ax, ax\n')
            else:    
                f.write('mov ax, '+ast.children[1].data+'\n')
                f.write('mov bx, ax\npop ax\n')
                f.write('mul ax, bx\n')
    elif(ast.data=='TK_DIV'):
        f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('push ax\n')
        if(ast.children[1].no_of_children != 0):
            codegen(ast.children[1],f)
        else:
            f.write('mov ax, '+ast.children[1].data+'\n')
        f.write('mov bx, ax\npop ax\n')
        f.write('div ax, bx\n')
    elif(ast.data=='TK_IF'):
        #conditional statements
        codegen(ast.children[0],f)#boolean condition
        #more code to follow, to traverse the rest of the conditional
        f.write('cmp ax, 0\n')
        if(ast.no_of_children==3):
            f.write('je ELSE\n')
            #now getting 'then'
            i=0
            while(i<ast.children[1].no_of_children):
                codegen(ast.children[1].children[i],f)
                i+=1
        elif(ast.no_of_children>3):
            temp=ast
            ch=2
            while((ch+1)<ast.no_of_children):
                f.write('je '+ast.children[ch].data+str(ch-1)+'\n')
                i=0
                while(i<temp.children[1].no_of_children):
                    codegen(temp.children[1].children[i],f)
                    i+=1
                f.write(ast.children[ch].data+str(ch-1)+':\n')
                codegen(ast.children[ch].children[0],f)
                f.write('cmp ax, 0\n')
                temp=ast.children[ch]
                ch+=1
            f.write('je ELSE\n')
            #now getting 'then'
            i=0
            while(i<temp.no_of_children):
                codegen(temp.children[i],f)
                i+=1
        #
        # code for elseif implementation
        #
        f.write('jmp ENDIF\n')
        if(ast.no_of_children>2):
            f.write('ELSE:\n')
            codegen(ast.children[ast.no_of_children-1].children[0],f)
        f.write('ENDIF:\n\n')
        

    elif(ast.data=='TK_AND'):
        f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('push ax\n')
        if(ast.children[1].no_of_children != 0):
            codegen(ast.children[1],f)
        else:
            f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('pop bx\n')
        f.write('and ax, bx\n\n')

    elif(ast.data=='TK_OR'):
        f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('push ax\n')
        if(ast.children[1].no_of_children != 0):
            codegen(ast.children[1],f)
        else:
            f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('pop bx\n')
        f.write('or ax, bx\n\n')

    elif(ast.data=='TK_NOT'):
        f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('not ax\n\n')

    elif(ast.data== 'TK_LT' or ast.data=='TK_LE' or ast.data=='TK_EQ' or ast.data=='TK_GT' or ast.data=='TK_GE' or ast.data=='TK_NE'):
        f.write('mov ax, '+ast.children[0].data+'\n')
        if(ast.children[1].no_of_children != 0):
            codegen(ast.children[1],f)
        else:
            f.write('\npush ax\nmov ax, '+ast.children[1].data+'\n')
        f.write('\nmov bx, ax\npop ax\ncmp ax, bx\n')
        f.write('pushf\npop ax\n')
        if(ast.data=='TK_LT'):
            f.write('and ax, 0880h\nmov cl, 3\nshr ah, cl\n')
            f.write('mov cl, 7\nshr al, cl\n')
            f.write('xor al, ah\nmov ah, 0\n\n')

        elif(ast.data=='TK_LE'):
            f.write('mov bl, al\nand ax, 0880h\nmov cl, 3\nshr ah, cl\n')
            f.write('mov cl, 7\nshr al, cl\n')
            f.write('xor al, ah\nand bl, 40h\nmov cl, 6\nshr bl, cl\n')
            f.write('or al, bl\nmov ah, 0\n\n')

        elif(ast.data=='TK_EQ'):
            f.write('and ax, 0040h\nmov cl, 6\nshr al, cl\n\n')

        elif(ast.data=='TK_GT'):
            f.write('mov bl, al\nand ax, 0880h\nmov cl, 3\nshr ah, cl\n')
            f.write('mov cl, 7\nshr al, cl\n')
            f.write('xor al, ah\nnot al\nand al, 01h\nnot bl\nand bl, 40h\n')
            f.write('mov cl,6\nshr bl, cl\n')
            f.write('and al, bl\nmov ah, 0\n\n')

        elif(ast.data=='TK_GE'):
            f.write('and ax, 0880h\nmov cl, 3\nshr ah, cl\n')
            f.write('mov cl, 7\nshr al, cl\n')
            f.write('xor al, ah\nnot al\nand ax, 0001h\n\n')

        elif(ast.data=='TK_NE'):
            f.write('and ax, 0040\nmov cl, 6\nshr al, cl\n')
            f.write('not al\nand ax, 0001h\n\n')
    
    elif(ast.data=='PUT'):
        f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('\ncall _write\n')
        f.write('INT 10h ;Print the value of the variable\n')
    elif(ast.data=='PUTS'):
        f.write('mov ax, '+ast.children[0].data+'\n')
        f.write('INT 10h ;Print the string\n')
    elif(ast.data=='GET'):
        f.write('call _read\n')
        f.write('mov ax, '+ast.children[0].data+'\n\n')
    elif(ast.data=='TK_WHILE'):
        f.write('STARTLOOP:\n')
        codegen(ast.children[0].children[0],f)
        f.write('cmp ax, 0\nje ENDLOOP\n')
        i=0
        while(i<ast.no_of_children):
            codegen(ast.children[1].children[i],f)
            i+=1
        f.write('jmp STARTLOOP\nENDLOOP:\n\n')
    # elif(ast.data=='TK_MAPINSERT'):

    # elif(ast.data=='TK+MAPREMOVE'):