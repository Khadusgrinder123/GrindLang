import TokenLibrary as TL

TokenType = TL.TokenType()
Keywords = TokenType.Keyword()
NonLetters = TokenType.NonLetter()
SingleOP = TokenType.SOP()
DoubleOP = TokenType.DOP()


text = '''
let tiny_int RED = 33
let tiny_flt B = 3.4
show B;
show RED;
show "hello world";
if (2 > 1) {
    show "right";
}
'''
line = 1
scanned_text = []
cursor = 0

while cursor < len(text):
    char = text[cursor]

    if char.isspace():
        if char == "\n":
            scanned_text.append(NonLetters[char])
            line += 1
        cursor += 1
        continue

    if char == '"':
        cursor += 1
        string_start = cursor
        while cursor < len(text) and text[cursor] != '"':
            cursor += 1
        if cursor >= len(text):
            raise ValueError(f"string has not closing. Line {line}.")
        scanned_text.append("STRING:" + text[string_start:cursor])
        if cursor < len(text):
            cursor += 1
        continue

    if char.isdigit():
        number_start = cursor
        dot_count = 0
        while cursor < len(text) and (text[cursor].isdigit() or text[cursor] == "."):
            if text[cursor] == ".":
                dot_count += 1
            cursor += 1
        number = text[number_start:cursor]

        if dot_count > 1:
            raise ValueError(f"Invalid Number {number}. Line {line}.")

        if dot_count == 1:
            if not number[-1].isdigit(): # checks what is after "."
                raise ValueError(f"Invalid number {number}. Line {line}.")


        token_type = "FLOAT" if dot_count == 1 else "INTEGER"
        scanned_text.append(token_type + ":" + number)
        continue

    if char.isalpha() or char == "_":
        identifier_start = cursor
        cursor += 1
        while cursor < len(text) and (text[cursor].isalnum() or text[cursor] == "_"):
            cursor += 1
        identifier = text[identifier_start:cursor]
        scanned_text.append(Keywords.get(identifier, "IDENTIFIER:" + identifier))
        continue

    operator = text[cursor:cursor + 2]
    if operator in DoubleOP:
        scanned_text.append(DoubleOP[operator])
        cursor += 2
        continue

    if char in SingleOP:
        scanned_text.append(SingleOP[char])
        cursor += 1
        continue

    if char in NonLetters:
        scanned_text.append(NonLetters[char])
        cursor += 1
        continue

    raise ValueError(f"Unknown char {char}. Line {line}.")

print(scanned_text)

def ScannedText():
    return scanned_text