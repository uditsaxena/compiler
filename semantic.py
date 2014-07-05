#semantic analysis

from token_exp import token_exprs
import re
import sys

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
				print(nam)
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
									print(type2,symbol_table[sym].input[t].type)
									sys.stderr.write('Error : type mismatch in '+' input argument of function '+nam+' in '+scope+'\n')
				if flagz==0:
					sys.stderr.write('Error : attempt to use function '+nam+' without declaration in '+scope+'\n')
					
