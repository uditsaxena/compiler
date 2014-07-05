import re
import sys

from token_exp import token_exprs

def lexeme(characters):
    pos=0
    error_line=1; #line no where error occured
    tokens=[]
    no_of_tokens_in_line=[]
    no_of_tok=0
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag != 'SKIP' and tag != 'NEWLINE' and tag!= 'COMMENT':
                    token = (text, tag)
                    tokens.append(token)
                    no_of_tok+=1
                pos=match.end(0)
                if tag=='NEWLINE':
                    error_line+=1
                    pos_prev_line=pos
                    no_of_tokens_in_line.append(no_of_tok)
                  # print(no_of_tok)
                    no_of_tok=0
                break
        #if not match:
            #error_pos=pos-pos_prev_line+1
            #sys.stderr.write('Illegal character: {} at line {} and position{}\n'.format(characters[pos],error_line,error_pos))
            #pos+=1
    return tokens,no_of_tokens_in_line