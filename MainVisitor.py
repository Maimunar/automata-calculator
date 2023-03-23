from antlr4.tree.Tree import ParseTree
from CalculatorVisitor import CalculatorVisitor
from CalculatorParser import CalculatorParser
import sys
from antlr4 import *
from CalculatorLexer import CalculatorLexer
import copy

class ReturnValueException(Exception):
    def __init__(self, value):
        self.value = value
    def val(self):
        return self.value

class ExprVisitor(CalculatorVisitor):
    def __init__ (self, *args, **kwargs):
        super(CalculatorVisitor, self).__init__(*args, **kwargs)
        self.vars = {}
        self.funcVars = []
        self.funcs = {}

    # Single Variables / Content

    def visitNumber(self, ctx: CalculatorParser.NumberContext):
        return int(ctx.NUMBER().getText())

    def visitID(self, ctx: CalculatorParser.IDContext):
        allVars = copy.deepcopy(self.vars)
        allVars.update({} if not self.funcVars else self.funcVars[-1])
        id = ctx.ID().getText()
        if id in allVars.keys():
            return allVars[id]
        else:
            raise Exception(f'Variable {id} is not defined')
    
    def visitBoolean(self, ctx: CalculatorParser.BooleanContext):
        return ctx.BOOL().getText() == 'true'
    
    def visitBoolNum(self, ctx: CalculatorParser.BoolNumContext):
        return float(ctx.NUMBER().getText())

    def visitBoolID(self, ctx: CalculatorParser.BoolIDContext):   
        return self.visitID(ctx)

    # Calculation Operations

    def visitMultiplication(self, ctx:CalculatorParser.MultiplicationContext):
        return self.visit(ctx.left) * self.visit(ctx.right)

    def visitDivision(self, ctx: CalculatorParser.DivisionContext):
        return self.visit(ctx.left) / self.visit(ctx.right) 
    
    def visitPlus(self, ctx: CalculatorParser.PlusContext):
        return self.visit(ctx.left) + self.visit(ctx.right) 
   
    def visitMinus(self, ctx: CalculatorParser.MinusContext):
        return self.visit(ctx.left) - self.visit(ctx.right) 
    
    def visitParenthesis(self, ctx: CalculatorParser.ParenthesisContext):
        return self.visit(ctx.inner)
    
    # Logic Operations

    def visitNegation(self, ctx: CalculatorParser.NegationContext):
        return not self.visit(ctx.inner)
    
    def visitMore(self, ctx: CalculatorParser.MoreContext):
        return self.visit(ctx.left) > self.visit(ctx.right) 
    
    def visitLess(self, ctx: CalculatorParser.LessContext):
        return self.visit(ctx.left) < self.visit(ctx.right) 
    
    def visitEqual(self, ctx: CalculatorParser.EqualContext):
        return self.visit(ctx.left) == self.visit(ctx.right) 
    
    def visitMoreEqual(self, ctx: CalculatorParser.MoreEqualContext):
        return self.visit(ctx.left) >= self.visit(ctx.right) 
    
    def visitLessEqual(self, ctx: CalculatorParser.LessEqualContext):
        return self.visit(ctx.left) <= self.visit(ctx.right) 
    
    def visitNotEqual(self, ctx: CalculatorParser.NotEqualContext):
        return self.visit(ctx.left) != self.visit(ctx.right) 
    
    def visitBoolParenthesis(self, ctx: CalculatorParser.BoolParenthesisContext):
        return self.visit(ctx.inner)

    def visitLogicAnd(self, ctx: CalculatorParser.LogicAndContext):
        return self.visit(ctx.left) and self.visit(ctx.right) 

    def visitLogicOr(self, ctx: CalculatorParser.LogicOrContext):
        return self.visit(ctx.left) or self.visit(ctx.right) 

    # Expressions

    def visitPrint(self, ctx: CalculatorParser.PrintContext):
        print(f'<Print>     {ctx.expr().getText()} ==> {self.visit(ctx.expr())}')

    def visitAssign(self, ctx: CalculatorParser.AssignContext):
        num = self.visit(ctx.expr())
        id = ctx.ID().getText()
        print(f'<Assign>    {id} = {num}')
        self.vars[id] = num
        print(self.vars)

    def visitStatementBlock(self, ctx: CalculatorParser.StatementBlockContext):
        return self.visit(ctx.inner)

    def visitIf(self, ctx: CalculatorParser.IfContext):
        childCount = ctx.getChildCount()
        print(f'<If>    {childCount} children')
        for i in range(childCount):
            if ctx.getChild(i).getText() == 'if':
                conditionRes = self.visit(ctx.getChild(i+1))
                if conditionRes == True:
                    return self.visit(ctx.getChild(i+2))
        # Else Logic
        if ctx.getChild(childCount - 2).getText() == 'else':
            return self.visit(ctx.getChild(childCount - 1))
    
    def visitWhile(self, ctx: CalculatorParser.WhileContext):
        print (f'<While>    {ctx.getChild(1).getText()}')
        while self.visit(ctx.getChild(1)):
            self.visit(ctx.getChild(2))

    # Functions 
    
    def visitFunctionCall(self, ctx: CalculatorParser.FunctionCallContext):
        functionName = ctx.ID().getText()
        params = ctx.expr()
        vars = [self.visit(p) for p in params]
        print('<FUNCTION CALL>   ',functionName,vars)

        if functionName in self.funcs.keys():
            arguments = self.funcs[functionName]['parameters'].copy()
            if len(vars) != len(arguments):
                raise Exception(f"Expected {len(arguments)} arguments. Received {len(vars)}")
            functionParams = {}
            for index,argument in enumerate(arguments):
                functionParams[argument] = vars[index]
            functionBody = self.funcs[functionName]['block']
            self.funcVars.append(functionParams)
            result = self.visit(functionBody)
            print('<FUNCTION RESULT>    ', f'{functionName} ==> {result}')
            self.funcVars.pop()
            return result
        else:
            raise Exception(f'Function "{functionName}" not defined! ')
    
    def visitFunctionBody(self, ctx: CalculatorParser.FunctionBodyContext):
        try:
            return self.visit(ctx.inner)
        except ReturnValueException as err:
            return err.val()

    def visitFuncDefine(self, ctx: CalculatorParser.FuncDefineContext):
        ids = ctx.ID()
        fName = ids[0].getText()
        params = [p.getText() for p in ids[1:]]
        block = ctx.funcBlock()

        self.funcs[fName] = {
            'parameters': params,
            'block': block
        }

    def visitFuncPrint(self, ctx: CalculatorParser.FuncPrintContext):
        return self.visitPrint(ctx)
    
    def visitFuncIf(self, ctx: CalculatorParser.FuncIfContext):
        return self.visitIf(ctx)

    def visitFuncWhile(self, ctx: CalculatorParser.FuncWhileContext):
        return self.visitWhile(ctx)

    def visitFuncAssign(self, ctx: CalculatorParser.FuncAssignContext):
        return self.visitAssign(ctx)
    
    def visitFuncFuncDefine(self, ctx: CalculatorParser.FuncFuncDefineContext):
        return self.visitFuncDefine(ctx)
    
    def visitReturnStatement(self, ctx: CalculatorParser.ReturnStatementContext):
        raise ReturnValueException(self.visit(ctx.expr()))
    

def main(argv):
    if len(argv) > 1:
        input_stream = FileStream(argv[1])
    else:
        input_stream = StdinStream()
    
    lexer = CalculatorLexer(input_stream)
    
    stream = CommonTokenStream(lexer)
    parser = CalculatorParser(stream)
    tree = parser.main()

    visitor = ExprVisitor()

    visitor.visit(tree)
 
if __name__ == '__main__':
    main(sys.argv)