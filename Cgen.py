import Parser
ast = Parser.RawAST()
new_ast = """"""
a = 0
while a < len(ast):
    new_ast += (ast[a])
    a += 1
    new_ast += ("\n")

print("<---polished_ast--->", new_ast)
print('\n')

current_token = ''
cursor = 0

main = ''''''
indent_level = 0
loop_counter = 0

def emit_line(line):
    global main
    # make line for main
    main += ('    ' * indent_level) + line + '\n'

def read_list(token, cursor=0):
    # this is for if and loop
    values = []
    if cursor >= len(token) or token[cursor] != '[':
        raise SyntaxError('Expected a serialized list in parser output.')
    cursor += 1

    while cursor < len(token):
        while cursor < len(token) and token[cursor] == ' ':
            cursor += 1
        if cursor < len(token) and token[cursor] == ']':
            return values, cursor + 1
        if cursor >= len(token) or token[cursor] not in ("'", '"'):
            raise SyntaxError('Expected a quoted item in parser list output.')

        quote = token[cursor]
        cursor += 1
        value = ''
        while cursor < len(token) and token[cursor] != quote:
            if token[cursor] == '\\' and cursor + 1 < len(token):
                cursor += 1
                escaped = token[cursor]
                if escaped == 'n': value += '\n'
                elif escaped == 't': value += '\t'
                elif escaped == 'r': value += '\r'
                else: value += escaped
            else:
                value += token[cursor]
            cursor += 1
        if cursor >= len(token):
            raise SyntaxError('Unterminated quoted item in parser list output.')
        cursor += 1
        values.append(value)

        while cursor < len(token) and token[cursor] == ' ':
            cursor += 1
        if cursor < len(token) and token[cursor] == ',':
            cursor += 1
        elif cursor < len(token) and token[cursor] != ']':
            raise SyntaxError('Expected a comma or closing bracket in parser list output.')

    raise SyntaxError('Unterminated list in parser output.')

def condition_to_c(tokens):
    condition = ''
    operators = {
        'EQUAL_TO': '==',
        'LESS_THAN': '<',
        'GREATER_THAN': '>',
        'TRUE': '1',
        'FALSE': '0'
    }
    for part in tokens:
        if part in ('LPAREN', 'RPAREN'):
            continue
        if part in operators:
            condition += operators[part]
        elif part.startswith('INTEGER:'):
            condition += part.removeprefix('INTEGER:')
        elif part.startswith('FLOAT:'):
            condition += part.removeprefix('FLOAT:')
        else:
            condition += part
    return condition

def gen_statements(statements):
    for statement in statements:
        if statement in ('LCURLY', 'RCURLY'):
            continue
        if statement.startswith('PRINT:'):
            gen_print(statement)
        elif statement.startswith('VARIABLE_DECLARATION:IDENTIFIER:'):
            gen_let(statement)
        elif statement.startswith('IF:'):
            gen_if(statement)
        elif statement.startswith('LOOP:'):
            gen_loop(statement)
        elif statement == 'STOP':
            emit_line('break;')
        else:
            raise SyntaxError(f'Unsupported statement in if/loop: {statement}')

def gen_print(token):
    if token.startswith('PRINT:STRING:'):
        token = token.removeprefix('PRINT:STRING:')
        emit_line(f'printf("{token}\\n");')

    if token.startswith('PRINT:INTEGER:'):
        token = token.removeprefix('PRINT:INTEGER:')
        emit_line(f'printf("%d\\n", {token});')

    if token.startswith('PRINT:FLOAT:'):
        token = token.removeprefix('PRINT:FLOAT:')
        emit_line(f'printf("%f\\n", {token});')

def gen_if(token):
    global indent_level
    # remove 'if'
    token = token.removeprefix('IF:')

    condition, cursor = read_list(token)
    # same as expression
    if cursor >= len(token) or token[cursor] != ':':
        raise SyntaxError('Expected condition/body separator in IF parser output.')
    statements, cursor = read_list(token, cursor + 1)
    branches = [(condition_to_c(condition), statements)]

    # check for more branches
    while cursor < len(token):
        if token.startswith(':ELIF:', cursor):
            condition, cursor = read_list(token, cursor + len(':ELIF:'))
            if cursor >= len(token) or token[cursor] != ':':
                raise SyntaxError('Expected ELIF condition/body separator.')
            statements, cursor = read_list(token, cursor + 1)
            branches.append((condition_to_c(condition), statements))
        elif token.startswith(':ELSE:', cursor):
            statements, cursor = read_list(token, cursor + len(':ELSE:'))
            branches.append((None, statements))
        else:
            raise SyntaxError('Unexpected trailing data in IF parser output.')

    # now it will reflect the code
    for index, (condition, statements) in enumerate(branches):
        if index == 0:
            emit_line(f'if ({condition}) {{')
        elif condition is None:
            emit_line('} else {')
        else:
            emit_line(f'}} else if ({condition}) {{')
        indent_level += 1
        gen_statements(statements)
        indent_level -= 1
    emit_line('}')

def gen_loop(token):
    global indent_level, loop_counter
    # remove 'loop'
    token = token.removeprefix('LOOP:')
    statements, cursor = read_list(token)
    # checks for number after rep
    if cursor >= len(token) or token[cursor] != ':':
        raise SyntaxError('Expected body/repetition separator in LOOP parser output.')
    reps = token[cursor + 1:]

    # if keep
    if reps == 'KEEP':
        emit_line('while (1) {')
    else:
        reps = reps.removeprefix('INTEGER:')
        counter_name = f'_grind_loop_{loop_counter}'
        loop_counter += 1
        emit_line(f'for (int {counter_name} = 0; {counter_name} < {reps}; {counter_name}++) {{')

    indent_level += 1
    gen_statements(statements)
    indent_level -= 1
    emit_line('}')

def gen_let(token):
    global main

    token = token.removeprefix('VARIABLE_DECLARATION:IDENTIFIER:')
    token = token.replace("[\'", "")
    token = token.replace("\']", "")
    

    a = 0
    name = ''
    while token[a] != ':':
        name += token[a]
        a += 1
    a += 1

    

    tt = ''
    while token[a] != ':':
        tt += token[a]
        a += 1
    tt = tt.replace('"', '')
    tt = tt.replace('[','')
    a += 1
    if tt == 'INTEGER': tt = 'int'
    elif tt == 'FLOAT': tt = 'float'
    elif tt == 'STRING': tt = 'char'
    elif tt == 'EXPRESSION': tt = 'expression'
    elif tt == 'BOOLEAN': raise SyntaxError('boolean unsupported sorry.')
    else: raise SyntaxError('how does this error survive till this stage?!')

    value = ''
    int_value = 0
    flt_value = 0.0
    str_value = ''
    if tt == 'int':
        while a < len(token) and token[a] != '\n':
            value += token[a]
            a += 1
        int_value = int(value)
        emit_line(f'{tt} {name} = {int_value};')

    elif tt == 'float':
        while a < len(token) and token[a] != '\n':
            value += token[a]
            a += 1
        flt_value = float(value)
        emit_line(f'{tt} {name} = {flt_value};')

    elif tt == 'char':
        while a < len(token) and token[a] != '\n':
            value += token[a]
            a += 1
        str_value = value.replace('"', '\\"')
        emit_line(f'char {name}[] = "{str_value}";')


    expression = ''
    if tt == 'expression':
        a += 1
        value = token[a:]
        
        
        value = value.replace('INTEGER:', '')
        value = value.replace('FLOAT:', '')
        
        
        expression = value
        emit_line(f'float {name} = {expression};')
            


while cursor < len(new_ast):
    # make proper token
    while new_ast[cursor] != '\n':
        current_token += new_ast[cursor]
        cursor += 1

    # check
    if current_token.startswith('PRINT:'):
        gen_print(current_token)

    if current_token.startswith('VARIABLE_DECLARATION:IDENTIFIER:'):
        gen_let(current_token)

    if current_token.startswith('IF:'):
        gen_if(current_token)

    if current_token.startswith('LOOP:'):
        gen_loop(current_token)

    current_token = ''
    cursor += 1


c_code = f'''
#include <stdio.h>

int main() {{
    {main}
    return 0;
}}
'''

print("<---c code--->", c_code)

def Output():
    return c_code

time = Parser.Lexer.TL.sw_stop()
print(f"second: {time[0]}\nms: {time[1]}\nns: {time[2]}")

def score():
    global time
    if time[0] == 0 and time[1] == 0:
        return "excellent speed!"

    if time[0] == 0 and time[1] > 0:
        return "i mean meh but still not that slow"

    if time[0] > 0:
        return "bruh why is this so slow?"

print(score())