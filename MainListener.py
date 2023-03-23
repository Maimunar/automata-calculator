from CalculatorParser import CalculatorParser
import sys
from antlr4 import *
from CalculatorLexer import CalculatorLexer
from CalculatorListener import CalculatorListener

class ExprListener(CalculatorListener):
    def __init__ (self, *args, **kwargs):
        super(ExprListener, self).__init__(*args, **kwargs)
        self.nums = []
        self.ids = []
        self.vars = {}
    
    def exitNumber(self, ctx: CalculatorParser.NumberContext):
        num = int(ctx.NUMBER().getText())
        self.nums.append(num)

    def exitID(self, ctx: CalculatorParser.IDContext):
        id = ctx.ID().getText()
        if id in self.vars.keys():
            self.nums.append(self.vars[id])
        else:
            raise Exception(f'Variable {id} is not defined')

    def exitMultiplication(self, ctx: CalculatorParser.MultiplicationContext):
        right = self.nums.pop()
        left = self.nums.pop()
        self.nums.append(left*right)
    
    def exitDivision(self, ctx: CalculatorParser.DivisionContext):
        right = self.nums.pop()
        left = self.nums.pop()
        self.nums.append(left/right)

    def exitPlus(self, ctx: CalculatorParser.PlusContext):
        right = self.nums.pop()
        left = self.nums.pop()
        self.nums.append(left+right)
    
    def exitMinus(self, ctx: CalculatorParser.MinusContext):
        right = self.nums.pop()
        left = self.nums.pop()
        self.nums.append(left-right)

    def exitPrint(self, ctx: CalculatorParser.PrintContext):
        print(f'{ctx.expr().getText()} = {self.getResult()}')
    
    def exitAssign(self, ctx: CalculatorParser.AssignContext):
        num = self.nums.pop()
        id = ctx.ID().getText()
        print(f'Assigning {num} to {id}')
        self.vars[id] = num
        print(self.vars)

    def getResult(self):
        return self.nums.pop()        

def main(argv):
    if len(argv) > 1:
        input_stream = FileStream(argv[1])
    else:
        input_stream = StdinStream()
    
    lexer = CalculatorLexer(input_stream)
    
    stream = CommonTokenStream(lexer)
    parser = CalculatorParser(stream)
    tree = parser.main()

    listener = ExprListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
 
if __name__ == '__main__':
    main(sys.argv)