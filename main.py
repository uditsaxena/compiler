import re
import sys

# Data Structures required later.

token_exprs = [#regex for matching the characters to lexemes
        (r';', 'TK_SEM'),
        (r'[ \t]+', 'SKIP'), #matching whitespace
        (r'[\n]', 'NEWLINE'),
        (r'#[^\n]*', 'COMMENT'), #matching comments
        (r':', 'TK_ASSIGNOP'),
        (r'map_insert', 'TK_MAPINSERT'),
        (r'map_remove', 'TK_MAPREMOVE'),
        (r'assign', 'TK_ASSIGN'),
        (r'var', 'TK_VAR'),
        (r'main', 'TK_MAIN'),
        (r'end_main', 'TK_ENDMAIN'),
        (r'int', 'TK_INT'),
        (r'real', 'TK_REAL'),
        (r'if', 'TK_IF'),
        (r'end_if', 'TK_ENDIF'),
        (r'global', 'TK_GLOBAL'),
        (r'input', 'TK_INPUT'),
        (r'output', 'TK_OUTPUT'),
        (r'while', 'TK_WHILE'),
        (r'end_while', 'TK_ENDWHILE'),
        (r'char', 'TK_CHAR'),
        (r'function', 'TK_FUNCTION'),
        (r'end_function', 'TK_ENDFUNCTION'),
        (r'elseif', 'TK_ELSEIF'),
        (r'else', 'TK_ELSE'),
        (r'record', 'TK_RECORD'),
        (r'end_record', 'TK_ENDRECORD'),
        (r'array', 'TK_ARRAY'),
        (r'map', 'TK_MAP'),
        (r'get', 'TK_GET'),
        (r'puts', 'TK_PUTS'),
        (r'put', 'TK_PUT'),
        (r'return', 'TK_RETURN'),
        (r'break', 'TK_BREAK'),
        (r'call', 'TK_CALL'),
        (r'\[', 'TK_SQL'),
        (r'\]', 'TK_SQR'),
        (r'\,', 'TK_COMMA'),
        (r'\.', 'TK_DOT'),
        (r'\(', 'TK_OP'),
        (r'\)', 'TK_CL'),
        (r'\+', 'TK_PLUS'),
        (r'\-', 'TK_MINUS'),
        (r'\*', 'TK_MUL'),
        (r'\/', 'TK_DIV'),
        (r'\%', 'TK_MOD'),
        (r'\&', 'TK_AND'),
        (r'\|', 'TK_OR'),
        (r'!=', 'TK_NE'),
        (r'\!', 'TK_NOT'),
        (r'<=', 'TK_LE'),
        (r'<', 'TK_LT'),
        (r'==', 'TK_EQ'),
        (r'>=', 'TK_GE'),
        (r'>', 'TK_GT'),
        (r'\"[A-Za-z0-9_.,:? ]*"', 'TK_STRING'),
        (r'V_[A-Za-z_][A-Za-z0-9_]*', 'TK_ID'),
        (r'F_[A-Za-z_][A-Za-z0-9_]*', 'TK_FUNID'),
        (r'R_[A-Za-z_][A-Za-z0-9_]*', 'TK_RECORDID'),
        (r'M_[A-Za-z_][A-Za-z0-9_]*', 'TK_MAPID'),
        (r'A_[A-Za-z_][A-Za-z0-9_]*', 'TK_ARRAYID'),
        (r'\'\'\'[A-Za-z_][A-Za-z0-9_]*\'\'\'', 'TK_MAPFIELD'),
        (r'\'[A-Za-z0-9_.,:? ]\'', 'TK_CHR'),
        (r'[0-9]+.[0-9]+', 'TK_RNUM'),
        (r'[0-9]+', 'TK_NUM'), #Integer literals 
        (r'[A-Za-z0-9_,.|:?]', 'TK_CHR'),
]


ter=0
nonter=1

terminals= dict(
                TK_RECORD=0, TK_RECORDID=1, TK_ENDRECORD=2, TK_VAR=3, TK_ID=4, TK_SEM=5, TK_COMMA=6, TK_INT=7, TK_REAL=8, TK_CHAR=9,TK_GLOBAL=10, TK_ASSIGN=11, TK_ASSIGNOP=12,TK_NUM=13, TK_RNUM=14, TK_CHR=15, TK_FUNCTION= 16, TK_FUNID=17,TK_ENDFUNCTION=18, TK_OUTPUT=19, TK_INPUT=20, TK_SQL=21, TK_SQR=22, TK_MAIN=23, TK_ENDMAIN=24, TK_ARRAY=25, TK_ARRAYID=26, TK_MAP=27, TK_MAPID=28, TK_DOT=29, TK_OP=30, TK_CL=31, TK_PLUS=32, TK_MUL=33, TK_MINUS=34, TK_DIV=35, TK_MOD=36, TK_CALL=37, TK_WHILE=38, TK_ENDWHILE=39, TK_IF=40, TK_ENDIF=41, TK_ELSEIF=42, TK_ELSE=43, TK_GET=44, TK_PUT=45, TK_PUTS=46, TK_STRING=47, TK_NOT=48, TK_MAPFIELD=49, TK_AND=50, TK_OR=51, TK_LT=52, TK_LE=53, TK_EQ=54, TK_GT=55, TK_GE=56, TK_NE=57, TK_MAPINSERT=58, TK_MAPREMOVE=59, end=60, eps=61
)

nonterminals=dict(
                  program=0, typeDefinition_s=1, typeDefinition=2, fieldDefinition_s=3, fieldDefinition=4, moreField_ID=5, moreFields=6, primitiveDatatype=7, globalStatements=8, globalDeclare=9, globalAssign=10, var=11, otherFunctions=12, function=13, input_par=14, output_par=15, parameter_list=16, dataType=17, constructedDatatype=18, remaining_list=19, mainFunction=20, stmt_s=21, declaration_s=22, all_declaration=23, declaration=24, array_declaration=25, map_declaration=26, moreMapID=27,more_array_IDs=28, more_IDs=29, otherStmts=30, stmt=31, assignmentStmt=32, SingleOrRecOrArrayId=33, arithmeticExpression=34, more_variables=35, operator=36, funCallStmt=37, idList=38, more_ids=39, iterativeStmt=40, conditionalStmt=41, mod1=42, mod2=43, mod3=44, mod4=45, ioStmt=46, allVar=47, numorid=48,booleanExpression=49, bExp=50, Op=51, variable=52, logicalOp=53, relationalOp=54, mapStmt=55, mapAdd=56, mapDelete=57
)

parse_table=[
[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,-1,-1,-1,-1,-1,0,-1,-1,-1,-1,-1,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[1,-1,-1,-1,-1,-1,-1,-1,-1,-1,2,-1,-1,-1,-1,-1,2,-1,-1,-1,-1,-1,-1,2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[3,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,4,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,7,6,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,9,8,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,10,11,12,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,13,-1,-1,-1,-1,-1,14,-1,-1,-1,-1,-1,-1,14,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,15,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,16,-1,-1,-1,-1,17,-1,-1,-1,-1,-1,-1,17,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,18,19,20,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,21,-1,-1,-1,-1,-1,-1,22,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,23,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,24,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,25,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,26,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,27,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[29,-1,-1,-1,-1,-1,-1,28,28,28,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[30,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,31,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,32,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,33,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,34,-1,-1,-1,-1,-1,-1,-1,34,-1,-1,-1,-1,-1,-1,34,-1,-1,-1,-1,-1,34,34,-1,34,-1,-1,-1,-1,-1,-1,-1,-1,-1,34,34,-1,34,-1,-1,-1,34,34,34,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,34,34,-1,-1],
[-1,-1,-1,35,-1,-1,-1,-1,-1,-1,-1,36,-1,-1,-1,-1,-1,-1,36,-1,-1,-1,-1,-1,36,35,-1,35,-1,-1,-1,-1,-1,-1,-1,-1,-1,36,36,-1,36,-1,-1,-1,36,36,36,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,36,36,-1,-1],
[-1,-1,-1,37,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,38,-1,39,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,40,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,41,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,42,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,44,43,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,46,45,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,48,47,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,49,-1,-1,-1,-1,-1,-1,50,-1,-1,-1,-1,-1,50,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,49,49,50,49,50,50,50,49,49,49,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,49,49,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,51,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,55,52,-1,53,-1,-1,-1,54,54,54,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,56,56,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,57,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,59,-1,-1,58,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,60,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,62,-1,-1,62,63,-1,-1,-1,-1,-1,-1,-1,62,62,62,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,62,-1,61,63,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,64,-1,-1,64,64,-1,-1,-1,-1,-1,-1,-1,64,64,64,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,64,-1,64,-1,64,64,65,65,65,65,65,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,66,67,68,69,70,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,71,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,72,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,73,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,74,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,75,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,76,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,77,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,78,78,78,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,80,79,80,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,81,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,83,-1,82,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,84,85,86,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,88,-1,-1,87,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,89,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,91,-1,-1,-1,-1,-1,-1,-1,-1,90,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,93,-1,-1,93,-1,-1,-1,-1,-1,-1,-1,-1,93,93,93,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,93,-1,93,-1,92,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,94,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,95,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,96,96,96,96,96,96,96,96,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,97,97,98,98,98,98,98,98,-1,-1,-1,-1],
[-1,104,-1,-1,99,-1,-1,-1,-1,-1,-1,-1,-1,100,101,102,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,103,-1,105,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,106,107,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,108,109,110,111,112,113,-1,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,114,115,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,116,-1,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,117,-1,-1]
]
rules=[[(nonter,nonterminals['typeDefinition_s'],'typeDefinition_s'),(nonter,nonterminals['globalStatements'],'globalStatements'),(nonter,nonterminals['otherFunctions'],'otherFunctions'),(nonter,nonterminals['mainFunction'],'mainFunction')],
       [(nonter,nonterminals['typeDefinition'],'typeDefinition'),(nonter,nonterminals['typeDefinition_s'],'typeDefinition_s')],
       [(ter,terminals['eps'],'eps')],
       [(ter,terminals['TK_RECORD'],'TK_RECORD'),(ter,terminals['TK_RECORDID'],'TK_RECORDID'),(nonter,nonterminals['fieldDefinition_s'],'fieldDefinition_s'),(ter,terminals['TK_ENDRECORD'],'TK_ENDRECORD')],
       [(nonter,nonterminals['fieldDefinition'],'fieldDefinition'),(nonter,nonterminals['moreFields'],'moreFields')],
       [(ter,terminals['TK_VAR'],'TK_VAR'),(nonter,nonterminals['primitiveDatatype'],'primitiveDatatype'),(ter,terminals['TK_ID'],'TK_ID'),(nonter,nonterminals['moreField_ID'],'moreField_ID'),(ter,terminals['TK_SEM'],'TK_SEM')],
       [(ter,terminals['TK_COMMA'],'TK_COMMA'),(ter,terminals['TK_ID'],'TK_ID'),(nonter,nonterminals['moreField_ID'],'moreField_ID')],
       [(ter,terminals['eps'],'eps')],
       [(nonter,nonterminals['fieldDefinition'],'fieldDefinition'),(nonter,nonterminals['moreFields'],'moreFields')],
       [(ter,terminals['eps'],'eps')],
       [(ter,terminals['TK_INT'],'TK_INT')],
       [(ter,terminals['TK_REAL'],'TK_REAL')],
       [(ter,terminals['TK_CHAR'],'TK_CHAR')],
       [(nonter,nonterminals['globalDeclare'],'globalDeclare'),(nonter,nonterminals['globalAssign'],'globalAssign')],
       [(ter,terminals['eps'],'eps')],
       [(ter,terminals['TK_GLOBAL'],'TK_GLOBAL'),(ter,terminals['TK_VAR'],'TK_VAR'),(nonter,nonterminals['dataType'],'dataType'),(ter,terminals['TK_ID'],'TK_ID'),(ter,terminals['TK_SEM'],'TK_SEM')],
       [(ter,terminals['TK_ASSIGN'],'TK_ASSIGN'),(ter,terminals['TK_ID'],'TK_ID'),(ter,terminals['TK_ASSIGNOP'],'TK_ASSIGNOP'),(nonter,nonterminals['var'],'var'),(ter,terminals['TK_SEM'],'TK_SEM')],
       [(ter,terminals['eps'],'eps')],
       [(ter,terminals['TK_NUM'],'TK_NUM')],
       [(ter,terminals['TK_RNUM'],'TK_RNUM')],
       [(ter,terminals['TK_CHR'],'TK_CHR')],
       [(nonter,nonterminals['function'],'function'),(nonter,nonterminals['otherFunctions'],'otherFunctions')],
       [(ter,terminals['eps'],'eps')],
       [(ter,terminals['TK_FUNCTION'],'TK_FUNCTION'),(ter,terminals['TK_FUNID'],'TK_FUNID'),(nonter,nonterminals['input_par'],'input_par'),(nonter,nonterminals['output_par'],'output_par'),(nonter,nonterminals['stmt_s'],'stmt_s'),(ter,terminals['TK_ENDFUNCTION'],'TK_ENDFUNCTION')],
       [(ter,terminals['TK_INPUT'],'TK_INPUT'),(ter,terminals['TK_SQL'],'TK_SQL'),(nonter,nonterminals['parameter_list'],'parameter_list'),(ter,terminals['TK_SQR'],'TK_SQR')],
       [(ter,terminals['TK_OUTPUT'],'TK_OUTPUT'),(ter,terminals['TK_SQL'],'TK_SQL'),(nonter,nonterminals['parameter_list'],'parameter_list'),(ter,terminals['TK_SQR'],'TK_SQR')], 
       [(ter,terminals['TK_VAR'],'TK_VAR'),(nonter,nonterminals['dataType'],'dataType'),(ter,terminals['TK_ID'],'TK_ID'),(nonter,nonterminals['remaining_list'],'remaining_list')],
       [(ter,terminals['eps'],'eps')],
       [(nonter,nonterminals['primitiveDatatype'],'primitiveDatatype')],
       [(nonter,nonterminals['constructedDatatype'],'constructedDatatype')],
       [(ter,terminals['TK_RECORD'],'TK_RECORD'),(ter,terminals['TK_RECORDID'],'TK_RECORDID')], 
       [(ter,terminals['TK_COMMA'],'TK_COMMA'),(nonter,nonterminals['parameter_list'],'parameter_list')],
       [(ter,terminals['eps'],'eps')],
       [(ter,terminals['TK_MAIN'],'TK_MAIN'),(nonter,nonterminals['stmt_s'],'stmt_s'),(ter,terminals['TK_ENDMAIN'],'TK_ENDMAIN')],
       [(nonter,nonterminals['declaration_s'],'declaration_s'),(nonter,nonterminals['otherStmts'],'otherStmts')],
       [(nonter,nonterminals['all_declaration'],'all_declaration'),(nonter,nonterminals['declaration_s'],'declaration_s')],
       [(ter,terminals['eps'],'eps')],
       [(nonter,nonterminals['declaration'],'declaration')],
       [(nonter,nonterminals['array_declaration'],'array_declaration')],
       [(nonter,nonterminals['map_declaration'],'map_declaration')],
       [(ter,terminals['TK_VAR'],'TK_VAR'),(nonter,nonterminals['dataType'],'dataType'),(ter,terminals['TK_ID'],'TK_ID'),(nonter,nonterminals['more_IDs'],'more_IDs'),(ter,terminals['TK_SEM'],'TK_SEM')],
       [(ter,terminals['TK_ARRAY'],'TK_ARRAY'),(nonter,nonterminals['primitiveDatatype'],'primitiveDatatype'),(ter,terminals['TK_ARRAYID'],'TK_ARRAYID'),(ter,terminals['TK_SQL'],'TK_SQL'),(ter,terminals['TK_NUM'],'TK_NUM'),(ter,terminals['TK_SQR'],'TK_SQR'),(nonter,nonterminals['more_array_IDs'],'more_array_IDs'),(ter,terminals['TK_SEM'],'TK_SEM')],
       [(ter,terminals['TK_MAP'],'TK_MAP'),(nonter,nonterminals['primitiveDatatype'],'primitiveDatatype'),(ter,terminals['TK_MAPID'],'TK_MAPID'),(nonter,nonterminals['moreMapID'],'moreMapID'),(ter,terminals['TK_SEM'],'TK_SEM')],
       [(ter,terminals['TK_COMMA'],'TK_COMMA'),(ter,terminals['TK_MAPID'],'TK_MAPID'),(nonter,nonterminals['moreMapID'],'moreMapID')],
       [(ter,terminals['eps'],'eps')],
       [(ter,terminals['TK_COMMA'],'TK_COMMA'),(ter,terminals['TK_ARRAYID'],'TK_ARRAYID'),(ter,terminals['TK_SQL'],'TK_SQL'),(ter,terminals['TK_NUM'],'TK_NUM'),(ter,terminals['TK_SQR'],'TKSQR')],
       [(ter,terminals['eps'],'eps')],
       [(ter,terminals['TK_COMMA'],'TK_COMMA'),(ter,terminals['TK_ID'],'TK_ID'),(nonter,nonterminals['more_IDs'],'more_IDs')],
       [(ter,terminals['eps'],'eps')],
       [(nonter,nonterminals['stmt'],'stmt'),(nonter,nonterminals['otherStmts'],'otherStmts')],
       [(ter,terminals['eps'],'eps')],
       [(nonter,nonterminals['assignmentStmt'],'assignStmt')],
       [(nonter,nonterminals['iterativeStmt'],'iterativeStmt')],
       [(nonter,nonterminals['conditionalStmt'],'conditionalStmt')],
       [(nonter,nonterminals['ioStmt'],'ioStmt')],
       [(nonter,nonterminals['funCallStmt'],'funCallStmt')],
       [(nonter,nonterminals['mapStmt'],'mapStmt')],
       [(ter,terminals['TK_ASSIGN'],'TK_ASSIGN'),(nonter,nonterminals['SingleOrRecOrArrayId'],'SingleOrRecOrArrayId'),(ter,terminals['TK_ASSIGNOP'],'TK_ASSIGNOP'),(nonter,nonterminals['arithmeticExpression'],'arithmeticExpression'),(ter,terminals['TK_SEM'],'TK_SEM')],
       [(ter,terminals['TK_ID'],'TK_ID')],
       [(ter,terminals['TK_RECORDID'],'TK_RECORDID'),(ter,terminals['TK_DOT'],'TK_DOT'),(ter,terminals['TK_ID'],'TK_ID')],
       [(ter,terminals['TK_ARRAYID'],'TK_ARRAYID'),(ter,terminals['TK_SQL'],'TK_SQL'),(nonter,nonterminals['numorid'],'numorid'),(ter,terminals['TK_SQR'],'TK_SQR')],
       [(ter,terminals['TK_OP'],'TK_OP'), (nonter,nonterminals['arithmeticExpression'],'arithmeticExpression') ,(ter,terminals['TK_CL'],'TK_CL'), (nonter,nonterminals['more_variables'],'more_variables')] , [(nonter,nonterminals['variable'],'variable'), (nonter,nonterminals['more_variables'],'more_variables')], [(ter,terminals['eps'],'eps')],

       [(nonter,nonterminals['arithmeticExpression'],'arithmeticExpression')], [(nonter,nonterminals['operator'],'operator'), (nonter,nonterminals['arithmeticExpression'],'arithmeticExpression')],

       [(ter,terminals['TK_PLUS'],'TK_PLUS')], [(ter,terminals['TK_MUL'],'TK_MUL')], [(ter,terminals['TK_MINUS'],'TK_MINUS')], [(ter,terminals['TK_DIV'],'TK_DIV')], [(ter,terminals['TK_MOD'],'TK_MOD')],

       [(ter,terminals['TK_CALL'],'TK_CALL'), (ter,terminals['TK_FUNID'],'TK_FUNID'), (ter,terminals['TK_SQL'],'TK_SQL'),(nonter,nonterminals['idList'],'idList'), (ter,terminals['TK_SQR'],'TK_SQR'), (ter,terminals['TK_SQL'],'TK_SQL'),(nonter,nonterminals['idList'],'idList'), (ter,terminals['TK_SQR'],'TK_SQR'), (ter,terminals['TK_SEM'],'TK_SEM')],

       [(ter,terminals['TK_ID'],'TK_ID'), (nonter,nonterminals['more_ids'],'more_ids')], [(ter,terminals['eps'],'eps')],

       [(ter,terminals['TK_COMMA'],'TK_COMMA'), (nonter,nonterminals['idList'],'idList')], [(ter,terminals['eps'],'eps')],

       [(ter,terminals['TK_WHILE'],'TK_WHILE'),  (nonter,nonterminals['booleanExpression'],'booleanExpression'), (nonter,nonterminals['stmt'],'stmt'), (nonter,nonterminals['otherStmts'],'otherStmts'), (ter,terminals['TK_ENDWHILE'],'TK_ENDWHILE')],

       [(ter,terminals['TK_IF'],'TK_IF'), (nonter,nonterminals['booleanExpression'],'booleanExpression'), (nonter,nonterminals['stmt'],'stmt'), (nonter,nonterminals['otherStmts'],'otherStmts'), (nonter,nonterminals['mod1'],'mod1'),  (ter,terminals['TK_ENDIF'],'TK_ENDIF')],

       [(nonter,nonterminals['mod2'],'mod2'), (nonter,nonterminals['mod4'],'mod4')],

       [(nonter,nonterminals['mod3'],'mod3'), (nonter,nonterminals['mod2'],'mod2')], [(ter,terminals['eps'],'eps')],

       [(ter,terminals['TK_ELSEIF'],'TK_ELSEIF'), (nonter,nonterminals['booleanExpression'],'booleanExpression'), (nonter,nonterminals['stmt'],'stmt'), (nonter,nonterminals['otherStmts'],'otherStmts')],

       [(ter,terminals['TK_ELSE'],'TK_ELSE'), (nonter,nonterminals['stmt'],'stmt'), (nonter,nonterminals['otherStmts'],'otherStmts')], [(ter,terminals['eps'],'eps')],

       [(ter,terminals['TK_GET'],'TK_GET'), (nonter,nonterminals['allVar'],'allVar'), (ter,terminals['TK_SEM'],'TK_SEM')], [(ter,terminals['TK_PUT'],'TK_PUT'), (nonter,nonterminals['allVar'],'allVar'), (ter,terminals['TK_SEM'],'TK_SEM')], [(ter,terminals['TK_PUTS'],'TK_PUTS'), (ter,terminals['TK_STRING'],'TK_STRING'), (ter,terminals['TK_SEM'],'TK_SEM')],

       [(ter,terminals['TK_ID'],'TK_ID')], [(ter,terminals['TK_RECORDID'],'TK_RECORDID'), (ter,terminals['TK_DOT'],'TK_DOT'), (ter,terminals['TK_ID'],'TK_ID')], [(ter,terminals['TK_ARRAYID'],'TK_ARRAYID'), (ter,terminals['TK_SQL'],'TK_SQL'), (nonter,nonterminals['numorid'],'numorid'), (ter,terminals['TK_SQR'],'TK_SQR')],

       [(ter,terminals['TK_NUM'],'TK_NUM')], [(ter,terminals['TK_ID'],'TK_ID')],

       [(ter,terminals['TK_OP'],'TK_OP'), (nonter,nonterminals['booleanExpression'],'booleanExpression'), (nonter,nonterminals['bExp'],'bExp')], [(nonter,nonterminals['variable'],'variable')], [(ter,terminals['TK_NOT'],'TK_NOT'), (nonter,nonterminals['booleanExpression'],'booleanExpression')],

       [(ter,terminals['TK_CL'],'TK_CL')], [(nonter,nonterminals['Op'],'Op'), (nonter,nonterminals['booleanExpression'],'booleanExpression'), (ter,terminals['TK_CL'],'TK_CL')],

       [(nonter,nonterminals['logicalOp'],'logicalOp')], [(nonter,nonterminals['relationalOp'],'relationalOp')],

       [(ter,terminals['TK_ID'],'TK_ID')], [(ter,terminals['TK_NUM'],'TK_NUM')], [(ter,terminals['TK_RNUM'],'TK_RNUM')], [(ter,terminals['TK_CHR'],'TK_CHR')], [(ter,terminals['TK_ARRAYID'],'TK_ARRAYID'), (ter,terminals['TK_SQL'],'TK_SQL'), (nonter,nonterminals['numorid'],'numorid'), (ter,terminals['TK_SQR'],'TK_SQR')], [(ter,terminals['TK_RECORDID'],'TK_RECORDID'), (ter,terminals['TK_DOT'],'TK_DOT'), (ter,terminals['TK_ID'],'TK_ID')], [ (ter,terminals['TK_MAPID'],'TK_MAPID'), (ter,terminals['TK_SQL'],'TK_SQL'), (ter,terminals['TK_MAPFIELD'],'TK_MAPFIELD'), (ter,terminals['TK_SQR'],'TK_SQR')],

       [(ter,terminals['TK_AND'],'TK_AND')], [(ter,terminals['TK_OR'],'TK_OR')],

       [(ter,terminals['TK_LT'],'TK_LT')], [(ter,terminals['TK_LE'],'TK_LE')], [(ter,terminals['TK_EQ'],'TK_EQ')], [(ter,terminals['TK_GT'],'TK_GT')], [(ter,terminals['TK_GE'],'TK_GE')], [(ter,terminals['TK_NE'],'TK_NE')],

       [(nonter,nonterminals['mapAdd'],'mapAdd')],[(nonter,nonterminals['mapDelete'],'mapDelete')],

       [(ter,terminals['TK_MAPINSERT'],'TK_MAPINSERT'), (ter,terminals['TK_MAPID'],'TK_MAPID'), (ter,terminals['TK_OP'],'TK_OP'), (ter,terminals['TK_MAPFIELD'],'TK_MAPFIELD'), (ter,terminals['TK_COMMA'],'TK_COMMA'), (nonter,nonterminals['variable'],'variable'), (ter,terminals['TK_CL'],'TK_CL'),(ter,terminals['TK_SEM'],'TK_SEM')],

       [(ter,terminals['TK_MAPREMOVE'],'TK_MAPREMOVE'), (ter,terminals['TK_MAPID'],'TK_MAPID'), (ter,terminals['TK_OP'],'TK_OP'), (ter,terminals['TK_MAPFIELD'],'TK_MAPFIELD'), (ter,terminals['TK_CL'],'TK_CL'), (ter,terminals['TK_SEM'],'TK_SEM')]]

stack=[(ter,terminals['end'],'end'),(nonter,nonterminals['program'],'program')]

###################################

# Lexer 

def lexeme(characters):
    pos=0
    pos_prev_line = 0
    error_line=1; #line no where error occured
    tokens=[]
    no_of_tokens_in_line=[]
    no_of_tok=0
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern) #Compile a regular expression pattern into a regular expression object, which can be used for matching using its match() and search() methods
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
        if not match:
            error_pos=pos-pos_prev_line+1
            sys.stderr.write('Illegal character: {} at line {} and position{}\n'.format(characters[pos],error_line,error_pos))
            pos+=1
    return tokens,no_of_tokens_in_line

###################################

# Parser

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
    print(parse_tree.data)
    i=0
    while i<parse_tree.no_of_children:
        print_tree(parse_tree.children[i])
        i+=1
        
###################################

#Symbol Table
    
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

###############################################################3

# Abstract Syntax Tree

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
            make_otherStmt_ast(a_big_otherStmt,new_ast)
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
                    new_ast1=tree(sub_tree.children[1].children[1].text,0,new_ast)
                elif sub_tree.children[1].children[0].data=='TK_ARRAYID':
                    new_ast1=tree(sub_tree.children[1].children[2].text,0,new_ast)
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
    if temp_tree.children[0].data!='eps':
        temp_tree=temp_tree.children[1]
        if temp_tree.children[0].data!='eps':
            new_ast=tree('global',0,curr_ast)
            curr_ast.children.append(new_ast)
            curr_ast.no_of_children+=1
            curr_index+=1
            curr_ast=new_ast
            new_ast=tree('assign',0,curr_ast)
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

def print_symbol_table(symbol_table):
    for k in symbol_table:
        print('name '+symbol_table[k].name+' type '+symbol_table[k].type+' scope '+symbol_table[k].scope+' array_size '+symbol_table[k].array_size)
        for j in symbol_table[k].fields:
            print('name '+j.name+' type '+j.type+' scope '+j.scope+' array_size '+j.array_size)
        for j in symbol_table[k].input:
            print('name '+j.name+' type '+j.type+' scope '+j.scope+' array_size '+j.array_size)
        for j in symbol_table[k].output:
            print('name '+j.name+' type '+j.type+' scope '+j.scope+' array_size '+j.array_size)
            

##############################

# Semantic Analysis and Type Checking

def find_arithmetic_type(ast,symbol_table,scope):
	type1=''
	val=ast.children[0].data
	if val!='TK_PLUS' and val!='TK_MINUS' and val!='TK_MUL' and val!='TK_DIV':
		for token_expr in token_exprs:
			pattern, tag = token_expr
			regex = re.compile(pattern)
			match = regex.match(val,0)
			if match:
				if tag=='TK_RNUM':
					type1='real'
				elif tag=='TK_NUM':
					type1='int'
				elif tag=='TK_CHR':
					type1='char'
				elif tag=='TK_ID':
					flag=0
					for symbol in symbol_table:
						if symbol_table[symbol].name==val and symbol_table[symbol].scope==scope:
							flag=1
							type1=symbol_table[symbol].type
					if flag==0:
						sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
				elif tag=='TK_RECORDID':
					flag=0
					val2=''
					k=0
					for v in val:
						if k!=0 and k!=1:
							val2+=v
						k+=1
					for symbol in symbol_table:
						if symbol_table[symbol].name==val2:
							flag=1
							flag2=0
							rec=symbol_table[symbol].type
							k=0
							rec2=''
							for r in rec:
								if k>=7:
									rec2+=r
								k+=1
							for field in symbol_table[(rec2,'global')].fields:
								if field.name==ast.children[0].text:
									flag2=1
									type1=field.type
									break
							if flag2==0:
								sys.stderr.write('Error : attempt to access invalid field '+ast.children[1].text+' of record '+tag+' in '+scope+'\n') 
					if flag==0:
						sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
				elif tag=='TK_ARRAYID':
					flag=0
					for symbol in symbol_table:
						if symbol_table[symbol].name==val and symbol_table[symbol].scope==scope:
							flag=1
							type1=symbol_table[symbol].type
							k=0
							typey=''
							for x in type1:
								if k>5:
									typey+=x
								k+=1
							type1=typey
							if flag==0:
								sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
				break
	else:
		type1=find_arithmetic_type(ast.children[0])
	type2=''
	val=ast.children[1].data
	if val!='TK_PLUS' and val!='TK_MINUS' and val!='TK_MUL' and val!='TK_DIV':
		for token_expr in token_exprs:
			pattern, tag = token_expr
			regex = re.compile(pattern)
			match = regex.match(val,0)
			if match:
				if tag=='TK_RNUM':
					type2='real'
				elif tag=='TK_NUM':
					type2='int'
				elif tag=='TK_CHR':
					type2='char'
				elif tag=='TK_ID':
					flag=0
					for symbol in symbol_table:
						if symbol_table[symbol].name==val and symbol_table[symbol].scope==scope:
							flag=1
							type2=symbol_table[symbol].type
					if flag==0:
						sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
				elif tag=='TK_RECORDID':
					flag=0
					val2=''
					k=0
					for v in val:
						if k!=0 and k!=1:
							val2+=v
						k+=1
					for symbol in symbol_table:
						if symbol_table[symbol].name==val2:
							flag=1
							flag2=0
							rec=symbol_table[symbol].type
							k=0
							rec2=''
							for r in rec:
								if k>=7:
									rec2+=r
								k+=1
							for field in symbol_table[(rec2,'global')].fields:
								if field.name==ast.children[1].text:
									flag2=1
									type2=field.type
									break
							if flag2==0:
								sys.stderr.write('Error : attempt to access invalid field '+ast.children[1].text+' of record '+tag+' in '+scope+'\n') 
					if flag==0:
						sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
				elif tag=='TK_ARRAYID':
					flag=0
					for symbol in symbol_table:
						if symbol_table[symbol].name==val and symbol_table[symbol].scope==scope:
							flag=1
							type2=symbol_table[symbol].type
							k=0
							typey=''
							for x in type2:
								if k>5:
									typey+=x
								k+=1
							type2=typey
							if flag==0:
								sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
				break
	else:
		type2=find_arithmetic_type(ast.children[1])
	if type2!=type1:
		if (type2!='int' and type2!='real') or (type1!='int' and type1!='real'):
			sys.stderr.write('Error : type mismatch : variable '+ast.children[0].data+' is of type '+type1+' and being operated with variable '+ast.children[1].data+' of type '+type2+' in '+scope+'\n')
	return type1


def semantic_analysis(ast,symbol_table):
	#global_stmt
	temp_ast=ast.children[0]
	if temp_ast.data!='eps':
		temp_ast=temp_ast.children[0]
		flag=0
		for symbol in symbol_table:
			if symbol_table[symbol].name==temp_ast.children[0].data and symbol_table[symbol].scope=='global':
				flag=1
				type1=symbol_table[symbol].type
		if flag==0:
			sys.stderr.write('Error : attempt to access '+temp_ast.children[0].data+' without declaration in global\n')
		else:
			val=temp_ast.children[1].data
			for token_expr in token_exprs:
				pattern, tag = token_expr
				regex = re.compile(pattern)
				match = regex.match(val,0)
				if match:
					type2=''
					if tag=='TK_RNUM':
						type2='real'
					elif tag=='TK_NUM':
						type2='int'
					elif tag=='TK_CHR':
						type2='char'
					if type2!=type1:
						if type2!='int' or type1!='real':
							sys.stderr.write('Error : type mismatch : variable '+temp_ast.children[0].data+' is of type '+type1+' and being assigned value of type '+type2+' in global\n')
					break
	
	#functions and main
	for temp_ast in ast.children:			
		scope=temp_ast.data
		if scope!='MAIN'and scope!='global':
			scope='function '+scope
		else:
			scope='main'
		for curr_ast in temp_ast.children:
	
			#for assignment statements
			if curr_ast.data=='TK_ASSIGN'and scope!='global':
				flag=0
				var=''
				for symbol in symbol_table:
					if symbol_table[symbol].name==curr_ast.children[0].data and symbol_table[symbol].scope==scope:
						flag=1
						type1=symbol_table[symbol].type
						k=0
						typex=''
						typey=''
						for x in type1:
							if k<=4:
								typex+=x
							if k>5:
								typey+=x
							k+=1
						if typex=='array':
							type1=typey
							var=curr_ast.children[0].data+'['+curr_ast.children[0].text+']'
						else:
							var=curr_ast.children[0].data
					name2='R_'
					for n in symbol_table[symbol].name:
						name2+=n
					if name2==curr_ast.children[0].data and symbol_table[symbol].scope==scope:
						flag=1
						flag2=0
						rec=symbol_table[symbol].type
						k=0
						rec2=''
						for r in rec:
							if k>=7:
								rec2+=r
							k+=1
						for field in symbol_table[(rec2,'global')].fields:
							if field.name==curr_ast.children[0].text:
								flag2=1
								type1=field.type
								var=curr_ast.children[0].data+'.'+field.name
								break
						if flag2==0:
							sys.stderr.write('Error : attempt to access invalid field '+curr_ast.children[0].text+' of record '+name2+' in '+scope+'\n')
				if flag==0:
					sys.stderr.write('Error : attempt to access '+curr_ast.children[0].data+' without declaration in '+scope+'\n')
				else:
					type2=''
					val=curr_ast.children[1].data
					if val!='TK_PLUS' and val!='TK_MINUS' and val!='TK_MUL' and val!='TK_DIV':
						for token_expr in token_exprs:
							pattern, tag = token_expr
							regex = re.compile(pattern)
							match = regex.match(val,0)
							if match:
								if tag=='TK_RNUM':
									type2='real'
								elif tag=='TK_NUM':
									type2='int'
								elif tag=='TK_CHR':
									type2='char'
								elif tag=='TK_ID':
									flag=0
									for symbol in symbol_table:
										if symbol_table[symbol].name==val and symbol_table[symbol].scope==scope:
											flag=1
											type2=symbol_table[symbol].type
									if flag==0:
										sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
								elif tag=='TK_RECORDID':
									flag=0
									val2=''
									k=0
									for v in val:
										if k!=0 and k!=1:
											val2+=v
										k+=1
									for symbol in symbol_table:
										if symbol_table[symbol].name==val2:
											flag=1
											flag2=0
											rec=symbol_table[symbol].type
											k=0
											rec2=''
											for r in rec:
												if k>=7:
													rec2+=r
												k+=1
											for field in symbol_table[(rec2,'global')].fields:
												if field.name==curr_ast.children[1].text:
													flag2=1
													type2=field.type
													break
											if flag2==0:
												sys.stderr.write('Error : attempt to access invalid field '+curr_ast.children[1].text+' of record '+tag+' in '+scope+'\n') 
									if flag==0:
										sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
								elif tag=='TK_ARRAYID':
									flag=0
									for symbol in symbol_table:
										if symbol_table[symbol].name==val and symbol_table[symbol].scope==scope:
											flag=1
											type2=symbol_table[symbol].type
											k=0
											typey=''
											for x in type2:
												if k>5:
													typey+=x
												k+=1
											type2=typey
									if flag==0:
										sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
								break
					else:
						type2=find_arithmetic_type(curr_ast.children[1],symbol_table,scope)
					if type2!=type1:
						if type2!='int' or type1!='real':
							sys.stderr.write('Error : type mismatch : variable '+var+' is of type '+type1+' and being assigned value of type '+type2+' in '+scope+'\n')
		
			#for function call statements
			if curr_ast.data=='funCall':
				nam=curr_ast.text
				flagz=0
				for sym in symbol_table:
					if symbol_table[sym].name==nam:
						flagz=1
						sub_ast=curr_ast.children[0]
						if len(sub_ast.children)>len(symbol_table[sym].input):
							sys.stderr.write('Error : too many input arguments while calling function '+nam+' in '+scope+'\n')
						elif len(sub_ast.children)<len(symbol_table[sym].input):
							sys.stderr.write('Error : too few input arguments while calling function '+nam+' in '+scope+'\n')
						else:
							t=0
							for inp in sub_ast.children:
								type2=''
								val=inp.data
								for token_expr in token_exprs:
									pattern, tag = token_expr
									regex = re.compile(pattern)
									match = regex.match(val,0)
									if match:
										if tag=='TK_RNUM':
											type2='real'
										elif tag=='TK_NUM':
											type2='int'
										elif tag=='TK_CHR':
											type2='char'
										elif tag=='TK_ID':
											flag=0
											for symbol in symbol_table:
												if symbol_table[symbol].name==val and symbol_table[symbol].scope==scope:
													flag=1
													type2=symbol_table[symbol].type
											if flag==0:
												sys.stderr.write('Error : attempt to access '+val+' without declaration in '+scope+'\n')
			
										break			
								if type2!=symbol_table[sym].input[t].type:
									sys.stderr.write('Error : type mismatch in '+' input argument of function '+nam+' in '+scope+'\n')
				if flagz==0:
					sys.stderr.write('Error : attempt to use function '+nam+' without declaration in '+scope+'\n')
					
###################################

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

###################################

# MAIN

def main():
#    filename = sys.argv[1]
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens,no_of_tokens_in_line = lexeme(characters)
    token=('end','end')
    tokens.append(token)
#    for token in tokens:
#        print(token)
    parse_tree=parser(tokens,no_of_tokens_in_line)
    print('Parse Tree:\n')
    print_tree(parse_tree)
    print('\n')
    symbol_table=make_symbol_table(parse_tree)
    print('Symbol Table:\n')
    print_symbol_table(symbol_table)
    print('\n')
    ast=make_ast(parse_tree)
    print('Abstract Syntax Tree:\n')
    print_tree(ast)
    print('\n')
    semantic_analysis(ast,symbol_table)
    f=open("output.txt",'w')
    codegen(ast,f)

if __name__ == '__main__': main()
