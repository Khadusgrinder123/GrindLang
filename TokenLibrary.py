class TokenType:
    # if,else,elif,loop,return,int,float,char,class,void,break,continue
    # boolean, let, sizeof, const
    
    def __init__(self):
        self.Keyword()
        self.DOP()
        self.SOP()
        self.NonLetter()

    def Keyword(self):
        self.Keywords = {
            "if": "IF",
            "else": "ELSE",
            "elif": "ELSE_IF",
            "loop": "LOOP",
            "reps": "REPS", # expects a number after this
            "keep": "KEEP", # this is only used after reps
            # creates infinite loop
            "nil": "NILL",
            "delete": "DELETE",
            "and": "AND",
            "or": "OR",
            "not": "NOT",
            "true": "TRUE",
            "false": "FALSE",
            "let": "LET",
            "show": "PRINT",

            # data types
            "int": "INTEGER",
            "float":"FLOAT",
            "bool": "BOOLEAN",
            "str": "STRING"   
        }
        return self.Keywords

    
    def NonLetter(self):
        self.NonLetters = {
            "(": "LPAREN",
            ")": "RPAREN",
            "{": "LCURLY",
            "}": "RCURLY",
            ":": "COLON",
            ";": "END_OF_STATEMENT",
            "\n": "END_OF_STATEMENT",
            ",": "COMMA",
            ".": "DOT"
        }
        return self.NonLetters

    def SOP(self):
        self.SingleOP = {
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/",
            "=": "EQUAL_TO",
            "!": "NOT",
            "<": "LESS_THAN",
            ">": "GREATER_THAN"
        }
        return self.SingleOP

    def DOP(self):
        self.DoubleOP = {
            "+=": "PLUS_EQUAL",
            "-=": "MINUS_EQUAL",
            "*=": "MUL_EQUAL",
            "/=": "DIV_EQUAL",
            "//": "COMMENT",
            "==": "IF_EQUAL",
            ">=": "GREATER_EQUAL",
            "<=": "LESS_EQUAL",
            "!=": "NOT_EQUAL"
        }
        return self.DoubleOP