from time import perf_counter_ns
start_time = 0

def sws():
    global start_time
    start_time = perf_counter_ns()

def sw_stop():
    elapsed = perf_counter_ns() - start_time

    seconds = elapsed // 1_000_000_000
    ms = (elapsed % 1_000_000_000) // 1_000_000
    ns = elapsed % 1_000_000
    return [seconds,ms,ns]

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
            "keep": "KEEP", # used after rep. Creates infinite loop
            "stop":"STOP", # stop an infinite loop on something being true
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
            "<=": "LESS_EQUAL"
        }
        return self.DoubleOP