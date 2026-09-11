class TokenType:
    # if,else,elif,loop,return,int,float,char,class,void,break,continue
    # boolean,function, let, sizeof, const
    
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
            "until": "KEEP_UNTIL", # put a boolean here to create a infinite loop
            # loop will run until some value is true
            "func": "FUNCTION",
            "class": "CLASS",
            "length": "LENGTH_OF_STRING",
            "allocate": "ALLOCATE",
            "nil": "NILL",
            "delete": "DELETE",
            "import": "IMPORT",
            "try": "TRY",
            "catch": "CATCH",
            "throw": "THROW",
            "switch": "SWITCH",
            "case": "CASE",
            "default": "DEFAULT",
            "force": "FORCE", # variable wont be deleted until manually removed
            "nickname": "NICKNAME", # typedef or alias
            "assume": "ASSUME", # assert expects something throw error if false
            "return": "RETURN",
            "break": "BREAK",
            "continue": "CONTINUE",
            "nothing": "NOTHING",
            "and": "AND",
            "or": "OR",
            "not": "NOT",
            "true": "TRUE",
            "false": "FALSE",
            "let": "LET",
            "const": "CONST",
            "sizeof": "SIZEOF",
            "show": "PRINT",

            # data types
            "tiny_int": "INT8",
            "small_int": "INT16",
            "mid_int": "INT32",
            "large_int": "INT64",
            "tiny_flt": "FLOAT16",
            "small_flt": "FLOAT32",
            "mid_flt": "FLOAT64",
            "large_flt": "FLOAT128",
            "bool": "BOOLEAN",
            "char": "CHARACTER",
            "str": "STRING"   
        }
        return self.Keywords

    def NonLetter(self):
        self.NonLetters = {
            "(": "LPAREN",
            ")": "RPAREN",
            "{": "LCURLY",
            "}": "RCURLY",
            "[": "LSQUARE",
            "]": "RSQUARE",
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
            "&": "ADRESSOF",
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