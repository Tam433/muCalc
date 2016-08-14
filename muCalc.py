"""
  This is a Scientific Calculator implemented in pure python!
  Current Supported Features :

    1) Standard Trigonometric Functions (Sine,Cosine,Tangent...)
    2) Standard Hyperbolic Trig Functions (Sinh,Cosh,Tanh.....)
    3) Math functions (Signum,Floor,Ceiling,Abs,Factorial.....)
    4) Variable declaration
    5) Standard math constants
    6) Relational operators
       a) > , >= , < , <= , != , == 
    7) Logical operators

    N.W.A (Nerds With Attitude) 2016
"""

import math_lib  # Imports the math_lib.py file for standard functions and variables
from tokdefs import *
env = {} # Environment to evaluate an expression ; it's where usr declared variables are stored.
env.update(vars(math_lib)) # Kinda' populating the environment with variables and functions.
env['False'] = False
env['True'] = True
iscallable = callable

###########################################
# This Class Encapsulates a Token         #
###########################################
class Token:
   def __init__(self, value, type):
          self.value = value # Token value
          self.type = type  # Token type

   def __str__(self):    # Python specific function , no actual use in calc
        return 'Token({value}, {type})'.format(
            value=repr(self.value),
            type=self.type)

   def __repr__(self): # Same as above one
        return self.__str__()

######################################################################################################
# This class is the main workhorse of the calculator.                                                #
# It generates tokens from math expressions.                                                         #
# Ex, : 2*pi*rad --> Token(2,NUM), Token('*',MUL), Token('pi',ID), Token('*',MUL), Token('rad',ID)   #
######################################################################################################
class Tokenizer:
   def __init__(self,exp):
      self.exp = exp # Math expression
      self.pos = 0   # Position of the character pointer
      self.current_char = self.exp[self.pos]  # The character pointer

   def advance(self):  # Advance the character pointer by 1
      self.pos += 1
      if self.pos > (len(self.exp) - 1):
         self.current_char = None
      else:
         self.current_char = self.exp[self.pos]

   def skip_ws(self):  # Skip whitespaces!
          while self.current_char.isspace():
               self.advance()
   def peek(self):   # This function kinda' peeks to see what the hell the next character is!
     pos = self.pos
     if pos > (len(self.exp) - 1):
        return None
     else:
        return self.exp[pos+1]

   def num(self):  # Function to Lex a number
        result = ''
        while ((self.current_char is not None) and (self.current_char.isdigit() or '.' in self.current_char )):
         result += self.current_char
         self.advance()
        return result

   def _id(self): # Function to Lex a name
        result = ''
        while ((self.current_char is not None) and (self.current_char.isalnum())):
         result += self.current_char
         self.advance()
        return str(result)

   def error(self):
      raise SyntaxError("W.T.F! is this ? "+self.current_char+" in input "+self.exp)

   def next_token(self):  # It gets the next token from the expression, Uses all functions defined above!
        while self.current_char != None:
           if self.current_char.isdigit():
              return Token(self.num(),NUM)

           elif self.current_char.isspace():
               self.skip_ws()
               continue

           elif self.current_char.isalpha():
              return Token(self._id(),ID)

           elif self.current_char == '+':
              self.advance()
              return Token('+',PLUS)

           elif self.current_char == '-':
              self.advance()
              return Token('-',MINUS)

           elif self.current_char == '/':
              self.advance()
              return Token('/',DIV)

           elif self.current_char == '*':
              self.advance()
              return Token('*',MUL)

           elif self.current_char == '%':
              self.advance()
              return Token('%',MOD)

           elif self.current_char == '^':
              self.advance()
              return Token('^',POW)

           elif self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token('==',EQ)
                else:   
                   self.advance()
                   return Token('=',ASSIGN)

           elif self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token('!=',NE)
                else:   
                    self.error()

           elif self.current_char == '>':
              if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token('>=',GE)
              else:
                self.advance()
                return Token('>',GT)
            
           elif self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token('<=',LE)
                else:
                  self.advance()
                  return Token('<',LT)

           elif self.current_char == '(':
              self.advance()
              return Token('(',LPAREN)

           elif self.current_char == ')':
              self.advance()
              return Token(')',RPAREN)

           else:
              self.error() 
        return Token('EOF',EOF)

   def peek_token(self): # This function kinda' peeks the next token
        pos = self.pos
        current_char = self.current_char
        peek_token = self.next_token()
        self.pos = pos
        self.current_char = current_char
        return peek_token

######################################################################################
# This Class is the Evaluator which uses the 'Lexer' Class defined above.            #
# It gets a token determines it's type and evaluates it using standard algebra rules #
# The process is called 'RECURSIVE DESCENT PARSEING' Got that??                      #
######################################################################################
class Parser:
    def __init__(self,lexer):
     self.lexer = lexer
     self.current_token = lexer.next_token()

    def eat(self,token_type): # Checks the token_type of current_token and kinda' EATS it and assigns the next token to current_token
      if token_type == self.current_token.type:
         self.current_token = self.lexer.next_token()
      else:
         raise SyntaxError("Expected:"+token_type+" Got: "+self.current_token.type)

    def atom(self):  # Lowest Level of an expression really 'atomic'
     token =  self.current_token
     if self.current_token.type == NUM: # Handle a number
         self.eat(NUM)
         if '.' in token.value:  # if decimal place is present in number, convert it into float
            return float(token.value)
         else:  # else the number is good old integer
            return int(token.value)

     if self.current_token.type == ID: # This handles if current_token is an ID
         self.eat(ID)
         if iscallable(env[token.value]):  # Check if the ID is a function
            self.eat(LPAREN)
            result = (env[token.value](self.expr0())) # If it is, then call it for a favour from the Environment
            self.eat(RPAREN)
            return result   # returns the computed result
         else:
            return env[token.value]  # Else the ID is a variable, gets it's value

     elif self.current_token.type == PLUS:  # Handles unary operator +a
         self.eat(PLUS)
         return +self.atom()

     elif self.current_token.type == MINUS: # Handles unary operator -a
         self.eat(MINUS)
         return -self.atom()

     elif self.current_token.type == LPAREN: # Handles (
         self.eat(LPAREN)
         node = self.expr0()
         self.eat(RPAREN)
         return node

    def expr3(self): # Second Lowest level, Handles exponentation! (^)
      left = self.atom()
      while self.current_token.type in (POW):
         token = self.current_token
         self.eat(POW)
         left = left ** self.atom()
      return  left

    def expr2(self): # First Lowest level, Handles Multiplication, Division, Modulo (*,/,%)
      left = self.expr3()
      while self.current_token.type in (MUL,DIV,MOD):
         token = self.current_token
         if self.current_token.type == MUL:
            self.eat(MUL)
            left = left * self.expr3()
         elif self.current_token.type == DIV:
            self.eat(DIV)
            left = left / self.expr3()
         elif self.current_token.type == MOD:
            self.eat(MOD)
            left = left % self.expr3()
      return left

    def expr1(self): # Zero'th Level, simple Addition and Substraction (+,-)
      left = self.expr2()
      while self.current_token.type in (PLUS, MINUS):
          token = self.current_token
          if token.type == PLUS:
            self.eat(PLUS)
            left = left + self.expr2()
          elif token.type == MINUS:
            self.eat(MINUS)
            left = left - self.expr2()
      return left

    def expr0(self):
        left = self.expr1()
        while self.current_token.type in (GE,GT,LE,LT,EQ,NE):
            token = self.current_token
            if token.type == GE:
                self.eat(GE)
                left = left >= self.expr1()
            elif token.type == LT:
                self.eat(LT)
                left = left < self.expr1()
            elif token.type == LE:
                self.eat(LE)
                left = left <= self.expr1()
            elif token.type == GT:
                self.eat(GT)
                left = left > self.expr1()
            elif token.type == EQ:
                self.eat(EQ)
                left = left == self.expr1()
            elif token.type == NE:
                self.eat(NE)
                left = left != self.expr1()
        return left

    def assign(self): # Handles variable assignment (ex: my_Var = expression)
      if self.current_token.type == ID and (self.lexer.peek_token()).type == ASSIGN:
        var_name = self.current_token.value
        self.eat(ID)
        self.eat(ASSIGN)
        right = self.expr0()
        env[var_name] = right
        return right
      else:
        return self.expr0()

    def parse(self): # It all starts with a call to this function, Don't try to call it's name , even loudly, it won't work ;-)
        node = self.assign()
        if self.current_token.type != EOF:
            raise Exception
        return node

def main():
    print 3*"\t"+"SciCalc v2.0 , a scientific calculator "
    print 3*"\t"+"N.W.A 2016 ;-)"
    while True:
        try:
            try:
                text = raw_input('--> ')
            except NameError:  # Python3
                text = input('--> ')
        except EOFError:
            break
        if not text:
            continue
        try:
          lexer = Tokenizer(text)
          parser = Parser(lexer)
          print(parser.parse())
        except Exception as e:
           print type(e).__name__ , e.args

if __name__ == "__main__":
   main()
