import Lexer

tokenized_text = Lexer.ScannedText()
cursor = Lexer.Cursor()

print(cursor)

# rhs is evaluated first in a node

current_if = 0
r = 1
e = 0 + r
rule = []
execution = []
AST = []


# if rule
if "IF" in tokenized_text:
    if_pos = tokenized_text.index('IF')
    current_if += 1
    if "LPAREN" in tokenized_text[if_pos + 1]:
        while "RPAREN" not in tokenized_text[if_pos + r]:
            r += 1
            rule.append(tokenized_text[if_pos + r])
            if "LCURLY" in rule and "RPAREN" not in rule:
                print("SYNTAX ERROR")
                break
                # "{" in rule but ")" not than a syntax error
        if "RPAREN" in rule: 
            rule.append(f"if_block: {current_if}")

print(rule)


# if execute