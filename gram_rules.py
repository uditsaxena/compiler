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
rules=[
      [(nonter,nonterminals['typeDefinition_s'],'typeDefinition_s'),(nonter,nonterminals['globalStatements'],'globalStatements'),(nonter,nonterminals['otherFunctions'],'otherFunctions'),(nonter,nonterminals['mainFunction'],'mainFunction')],
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
       [(ter,terminals['TK_COMMA'],'TK_COMMA'),(ter,terminals['TK_ID'],'TK_ID'),(ter,terminals['TK_SQL'],'TK_SQL'),(ter,terminals['TK_NUM'],'TK_NUM'),(ter,terminals['TK_SQR'],'TKSQR')],
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
       [(ter,terminals['TK_MAPREMOVE'],'TK_MAPREMOVE'), (ter,terminals['TK_MAPID'],'TK_MAPID'), (ter,terminals['TK_OP'],'TK_OP'), (ter,terminals['TK_MAPFIELD'],'TK_MAPFIELD'), (ter,terminals['TK_CL'],'TK_CL'), (ter,terminals['TK_SEM'],'TK_SEM')]
       ]
stack=[(ter,terminals['end'],'end'),(nonter,nonterminals['program'],'program')]