
# # 토큰 타입을 상수로 정의
# INTEGER, STRING, EOF = 0, 1, None
from printer import Printer

IDENT = "IDENT"
CONST = "CONST"
ASSIGNMENT_OP = "ASSIGNMENT_OP"
SEMI_COLON = "SEMI_COLON"
ADD_OP = "ADD_OP"
MIN_OP = "MIN_OP"
MULT_OP = "MULT_OP"
DIV_OP = "DIV_OP"
LEFT_PAREN = "LEFT_PAREN"
RIGHT_PAREN = "RIGHT_PAREN"
EOF = "EOF"


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
class Lexer:
    def __init__(self, text, print_type, symbolTable):
        self.text = text
        self.current_char = self.text[0]
        self.pos = 0
        next_token = None
        token_string = ''
        self.sentence=''
        self.id = 0
        self.const = 0
        self.op = 0
        self.state = "(OK)"
        self.print_type = print_type
        self.printer = Printer(print_type, symbolTable)
        self.symbol_table = symbolTable
        
    # def setState(self, newState):
    #     self.state = newState
        
    def split_statements(self,content):
        return content.split(';')
        
    def error(self):
        raise Exception('Invalid character')
    
    def advance(self):
        # if self.text[self.pos] != "\n":
        #     self.sentence += self.text[self.pos]
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def word(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_':
            result += self.current_char
            self.advance()
        return result
    
    ###
    def lexical(self):
        while self.current_char is not None:
            # 공백
            if self.current_char.isspace() or ord(self.current_char) <= 32:
                self.skip_whitespace()
                if self.sentence:
                    self.sentence += ' '
                continue
            # 식별자
            if self.current_char.isalpha():
                self.token_string = self.word()
                self.next_token = IDENT
                self.sentence += self.token_string
                # self.symbol_table.set(self.token_string, 0)
                self.id += 1
                self.printer.print_type_b(self.token_string)
                return
            # 숫자
            if self.current_char.isdigit():
                self.token_string = str(self.integer())
                self.next_token = CONST
                self.sentence += self.token_string
                self.const += 1
                self.printer.print_type_b(self.token_string)
                return
            
            # ;
            if self.current_char == ";":
                self.advance()
                self.token_string = ";"
                self.next_token = SEMI_COLON
                if self.sentence[-1] == ' ':
                    self.sentence = self.sentence[:-1] + self.token_string
                else:
                    self.sentence += self.token_string
                if self.print_type == 'a':
                    print(self.sentence)
                # print(self.state)
                self.printer.print_type_a(self.id, self.const, self.op, self.state)
                self.sentence = ''
                self.id = 0
                self.const = 0
                self.op = 0
                self.state = "(OK)"
                self.printer.print_type_b(self.token_string)
                return
            
            # :=    
            if self.current_char == ":":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    self.token_string = ":="
                    self.next_token = ASSIGNMENT_OP
                    self.sentence += self.token_string
                    self.printer.print_type_b(self.token_string)
                    return
            # +
            if self.current_char == "+":
                self.advance()
                self.token_string = "+"
                self.next_token = ADD_OP
                self.sentence += self.token_string
                self.op += 1
                self.printer.print_type_b(self.token_string)
                return
            # -
            if self.current_char == "-":
                self.advance()
                self.token_string = "-"
                self.next_token = MIN_OP
                self.sentence += self.token_string
                self.op += 1
                self.printer.print_type_b(self.token_string)
                return
            # *
            if self.current_char == "*":
                self.advance()
                self.token_string = "*"
                self.next_token = MULT_OP
                self.sentence += self.token_string
                self.op += 1
                self.printer.print_type_b(self.token_string)
                return
            # /
            if self.current_char == "/":
                self.advance()
                self.token_string = "/"
                self.next_token = DIV_OP
                self.sentence += self.token_string
                self.op += 1
                self.printer.print_type_b(self.token_string)
                return
            # (
            if self.current_char == "(":
                self.advance()
                self.token_string = "("
                self.next_token = LEFT_PAREN
                self.sentence += self.token_string
                self.printer.print_type_b(self.token_string)
                return
            # /
            if self.current_char == ")":
                self.advance()
                self.token_string = ")"
                self.next_token = RIGHT_PAREN
                self.sentence += self.token_string
                self.printer.print_type_b(self.token_string)
                return
            
        
            self.error()
            
        if self.sentence:
            if self.print_type == 'a':
                print(self.sentence)
            self.printer.print_type_a(self.id, self.const, self.op, self.state)
            self.sentence = None
        
        self.token_string = ''
        self.next_token = EOF