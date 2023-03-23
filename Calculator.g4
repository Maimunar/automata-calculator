grammar Calculator;
import LexerRules;

expr: funcExpr | calcExpr | boolExpr;

calcExpr:
	NUMBER													# Number
	| ID													# ID
	| funcExpr												# FunctionExpression
	| left = calcExpr operator = MULTIPLY right = calcExpr	# Multiplication
	| left = calcExpr operator = DIVIDE right = calcExpr	# Division
	| left = calcExpr operator = PLUS right = calcExpr		# Plus
	| left = calcExpr operator = MINUS right = calcExpr		# Minus
	| '(' inner = calcExpr ')'								# Parenthesis;

boolExpr:
	BOOL														# Boolean
	| ID														# BoolID
	| NUMBER													# BoolNum
	| funcExpr													# BoolFunctionExpression
	| operator = NEGATION inner = boolExpr						# Negation
	| left = boolExpr operator = MOREOP right = boolExpr		# More
	| left = boolExpr operator = LESSOP right = boolExpr		# Less
	| left = boolExpr operator = EQUALOP right = boolExpr		# Equal
	| left = boolExpr operator = MORE_EQUALOP right = boolExpr	# MoreEqual
	| left = boolExpr operator = LESS_EQUALOP right = boolExpr	# LessEqual
	| left = boolExpr operator = NOT_EQUALOP right = boolExpr	# NotEqual
	| left = boolExpr operator = AND_OP right = boolExpr		# LogicAnd
	| left = boolExpr operator = OR_OP right = boolExpr			# LogicOr
	| '(' inner = boolExpr ')'									# BoolParenthesis;

funcExpr: funcName = ID '(' params = expr* ')' # FunctionCall;

statBlock:
	OBRACE NEWLINE inner = body CBRACE NEWLINE # StatementBlock;

stat:
	IF boolExpr statBlock (ELSE IF boolExpr statBlock)* (ELSE statBlock)?	# If
	| WHILE boolExpr statBlock										# While
	| expr NEWLINE													# Print
	| ID '=' expr NEWLINE											# Assign
	| FUNC funcName = ID '(' params = ID* ')' funcBlock				# FuncDefine;

funcBlock:
	OBRACE NEWLINE inner = funcBody CBRACE NEWLINE # FunctionBody;

funcStat:
	IF boolExpr funcBlock (ELSE IF boolExpr funcBlock)* (
		ELSE funcBlock
	)?													# FuncIf
	| WHILE boolExpr funcBlock							# FuncWhile
	| expr NEWLINE										# FuncPrint
	| ID '=' expr NEWLINE								# FuncAssign
	| FUNC funcName = ID '(' params = ID* ')' funcBlock	# FuncFuncDefine
	| RETURN expr NEWLINE								# ReturnStatement;

funcBody: funcStat+;

body: stat+;

main: body;