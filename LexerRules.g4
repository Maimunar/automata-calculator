lexer grammar LexerRules;

// Algorithmic operators
PLUS: '+';
MINUS: '-';
MULTIPLY: '*';
DIVIDE: '/';

// Logic operators
MOREOP: '>';
LESSOP: '<';
EQUALOP: '==';
MORE_EQUALOP: '>=';
LESS_EQUALOP: '<=';
NOT_EQUALOP: '!=';
BOOL: 'true' | 'false';
AND_OP: '&&';
OR_OP: '||';
NEGATION: '!';

// If Operators
IF: 'if';
ELSE: 'else';
OBRACE: '{';
CBRACE: '}';
WHILE: 'while';

// Function Operators
FUNC: 'function';
RETURN: 'return';

// Content
NUMBER: [0-9]+;
WS: [ \t]+ -> skip;
NEWLINE: '\r\n';
ID: [a-zA-Z][a-zA-Z0-9]*;