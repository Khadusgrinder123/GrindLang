import TokenLibrary as TL
import os
from pathlib import Path

TokenType = TL.TokenType()
Keywords = TokenType.Keyword()
NonLetters = TokenType.NonLetter()
SingleOP = TokenType.SOP()
DoubleOP = TokenType.DOP()

current_char = ''
prev_chars = ''
token = []
cursor = 0

def input_code():
    print('Drag and Drop your file here (or type the content path).')
    path = input().strip().strip("'\"")
    
    if not path.endswith('.grind'):  # ✓ Correct - single dot
        print('wrong file extension')
        return input_code()
    
    try:
        grind_path = Path(path).expanduser().resolve()
        with open(grind_path, 'r', encoding='utf-8') as f:
            code = f.read()
        print(f"Loaded from {grind_path}")
        return code, grind_path
    except FileNotFoundError:
        print(f"File not found: {path}")
        return input_code()

text, grind_path = input_code()
print(text)

TL.sws()

while cursor < len(text):
    current_char = text[cursor]
    # eos
    if current_char == '\n':
        token.append('END_OF_STATEMENT')
        prev_chars = ''
        cursor += 1
        continue

    # eos
    if current_char == ';':
        token.append('END_OF_STATEMENT')
        prev_chars = ''
        cursor += 1
        continue

    # skip space
    if current_char == ' ':
        prev_chars = ''
        cursor += 1
        continue

    # digit
    if current_char.isdigit():
        number_start = cursor
        dot_count = 0
        while cursor < len(text) and (text[cursor].isdigit() or text[cursor] == "."):
            if text[cursor] == ".":
                dot_count += 1
            cursor += 1
        number = text[number_start:cursor]

        if dot_count > 1:
            raise ValueError('more than 1 dots')

        if dot_count == 1:
            if not number[-1].isdigit(): # checks what is after "."
                raise ValueError('invalid dot placement')

        token_type = "FLOAT" if dot_count == 1 else "INTEGER"
        token.append(token_type + ":" + number)
        continue

    # keywords
    if prev_chars in Keywords:
        token.append(Keywords[prev_chars])
        cursor += 1

    # variable
    if current_char.isalpha() or current_char == "_":
        identifier_start = cursor
        cursor += 1
        while cursor < len(text) and (text[cursor].isalnum() or text[cursor] == "_"):
            cursor += 1
        identifier = text[identifier_start:cursor]
        token.append(Keywords.get(identifier, "IDENTIFIER:" + identifier))
        continue

    # operator
    if current_char in SingleOP:
        # +
        # +=
        si_store = text[cursor]
        do_c = text[cursor]
        do_c += text[cursor + 1]
        if do_c in DoubleOP:
            if do_c == '//':
                while current_char != '\n':
                    current_char = text[cursor]
                    cursor += 1
                cursor -= 1
            if do_c != '//':
                token.append(DoubleOP[do_c])
                cursor += 1
        if not do_c in DoubleOP:
            if si_store in SingleOP:
                token.append(SingleOP[si_store])
                cursor += 1


    # non letters
    if current_char in NonLetters:
        token.append(NonLetters[current_char])


    # string start
    if text[cursor] == '"':
        in_string = ''
        cursor += 1
        while cursor < len(text) and text[cursor] != '"':
            in_string += text[cursor]
            cursor += 1
        token.append("STRING:" + in_string)
        if cursor >= len(text):
            raise SyntaxError ('string lateral with no end point')


    prev_chars += current_char
    cursor += 1

token.append('EOF')

print("<---LEXER--->")
print(token, "\n")


def ScannedText():
    return token