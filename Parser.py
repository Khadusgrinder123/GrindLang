import NewLexer as Lexer
tokenized_text = Lexer.ScannedText()
p_cursor = 0
variables = {}


def advance():
    global p_cursor
    p_cursor += 1

def advance_by(skip):
    global p_cursor
    p_cursor += skip

def current():
    return tokenized_text[p_cursor]

def ensure_variable_defined(name):
    if name not in variables:
        raise SyntaxError(f"Undefined variable: {name}")

def resolve_variable(token):
    if token.startswith("IDENTIFIER:"):
        name = token.removeprefix("IDENTIFIER:")
        ensure_variable_defined(name)
        return variables[name]
    return token

def expect(token):
    if current() != token:
        if current() != "EOF":
            raise SyntaxError(
                f"Expected {token}. Instead got {current()}"
            )
        if current() == "EOF":
            print(f'\n FOUND EOF INSTEAD OF EXPECTED "{token}" \n')
    # if the expected syntax is found then advance
    advance()

def parse_show():
    expect("PRINT")

    # show "hellow";
    value = resolve_variable(current())
    advance()
    expect("END_OF_STATEMENT")

    return f"""PRINT:{value}"""

def parse_let():
    expect("LET")
    #let int x = 10;
    if current() in ("INTEGER", "FLOAT", "BOOLEAN", "STRING"):
        advance()

        variable = current() # identifier
        advance()

        expect("EQUAL_TO")


        value = resolve_variable(current())
        if value.startswith(("INTEGER:", "FLOAT:")) and tokenized_text[p_cursor + 1] in Lexer.SingleOP:
            value = parse_expression_c()
        else:
            advance()

        var_value = [value]
        expect("END_OF_STATEMENT")

        variable_name = variable.removeprefix("IDENTIFIER:")
        variables[variable_name] = value

        return f"""VARIABLE_DECLARATION:{variable}:{var_value}"""
    else: raise SyntaxError (f"Expected int,float,bool,str but got {current()}")

def parse_loop():
    expect("LOOP")
    expect("LCURLY")
    if current() == "END_OF_STATEMENT": advance()
    expect("REPS")
    expect("COLON")
    reps = current() # expected number or keep
    advance()
    expect("END_OF_STATEMENT")

    if current() == "END_OF_STATEMENT" or current() == "COMMENT":
        advance()


    loop_work = []

    while current() != "RCURLY":
        if current() == "END_OF_STATEMENT" or current() == "COMMENT":
            advance()
            continue

        if current() == "EOF":
            break

        parsed = parse_all()
        if parsed is not None:
            loop_work.append(parsed)
            continue

        raise SyntaxError(f"Unexpected token inside loop: {current()}")

    expect("RCURLY")

    if reps == 'KEEP':
        if 'STOP' in loop_work:
            pass
        if 'STOP' not in loop_work:
            print("Sensitive loop. Uncontrolled Infinite loop")

    if reps != 'KEEP':
    # loop_work, rep
        return f"""LOOP:{loop_work}:{reps.removeprefix('INTEGER:')}"""
    if reps == 'KEEP': 
        return f"""LOOP:{loop_work}:{reps}"""


# oh my god man this is useless expression parsing is useless
# my initial plan was conversion to x86-64 assembly
# i changed my plan later to c and now this is useless
# more like its gonna increase my work!
def parse_expression():    
    expression = []

    while current() not in ("END_OF_STATEMENT", "EOF"):
        expression.append(resolve_variable(current()))
        advance()

    number_pos = []
    op_pos = []

    for i in range(len(expression)):
        if expression[i].startswith(("INTEGER:", "FLOAT:")):
            number_pos.append(i)
        elif expression[i] in Lexer.SingleOP:
            op_pos.append(i)
        else: raise SyntaxError("expected to be a number or operator!")

    parsed_exp = []

    def check_LR():
        # 3+2*3
        # pos = which operator do you wanna check
        # op_pos = [1, 3]
        # number_pos = [0, 2, 4]
        # expression = ["INTEGER:3, "+", "INTEGER: 2", "*", "INTEGER: 3:"]

        def check_power(first_op, sec_op):
            if first_op == "+": first_op = 2
            elif first_op == "-": first_op = 1
            elif first_op == "*": first_op = 3
            elif first_op == "/": first_op = 4
            else: raise SyntaxError("put a valid operator")
    
            if sec_op == "+": sec_op = 2
            elif sec_op == "-": sec_op = 1
            elif sec_op == "*": sec_op = 3
            elif sec_op == "/": sec_op = 4
            else: raise SyntaxError("put a valid operator")
    
            if first_op > sec_op:
                return "first_op"
    
            if sec_op > first_op:
                return "sec_op"

            if first_op == sec_op:
                return "first_op"

        pos = 0
        initial_dna = 2
        expression.append("EOE") # end of expression

        def lhs(dna):
            return expression[op_pos[0] + dna - 1]
        def rhs(dna):
            return expression[op_pos[0] + dna + 1]

        if len(op_pos) == 1:
                    parsed_exp.append(f"LHS:{expression[op_pos[pos] - 1]};OP:{expression[op_pos[pos]]};RHS:{expression[op_pos[pos] + 1]}")
        
        if len(op_pos) > 1:
            for i in range(len(expression)):
            # 3-2-3
                if expression[op_pos[pos] + initial_dna] == "EOE": break
                parsed_exp.append(f"STARTING:{expression[op_pos[0] - 1]};")
                # for minus
                if expression[op_pos[pos]] == "-":
                    parsed_exp.append(f"OP:{expression[op_pos[pos]]};")
                    if len(op_pos) == 1:
                        parsed_exp.append(f"RHS:{rhs(0)}")
                    if len(op_pos) == 0: raise SyntaxError("no operator found. Expected atleast 1")
                    if len(op_pos) > 1:
                        # for higher or equal power
                        if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "sec_op":
                            # st = sum of this term
                            parsed_exp.append(f"ST-LHS:{lhs(initial_dna)};OP:{expression[op_pos[pos] + initial_dna]};RHS:{rhs(initial_dna)}")
                        # for lower power
                        if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "first_op":
                            parsed_exp.append(f"RHS:{lhs(initial_dna)};OP:{expression[op_pos[pos] + initial_dna]};LHS:{rhs(initial_dna)}")
                # for addition
                if expression[op_pos[pos]] == "+":
                    parsed_exp.append(f"OP:{expression[op_pos[pos]]};")
                    if len(op_pos) == 1:
                        parsed_exp.append(f"RHS:{rhs(0)}")
                    if len(op_pos) == 0: raise SyntaxError("no operator found. Expected atleast 1")
                    if len(op_pos) > 1:
                        # st - sum of this term. Due to higher priority
                        if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "sec_op":
                            parsed_exp.append(f"ST-LHS:{lhs(initial_dna)};OP:{expression[op_pos[pos] + initial_dna]};RHS:{rhs(initial_dna)}")
                            # c- means continuation. This is for lower priority operator
                        elif check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "first_op":
                            parsed_exp.append(f"C-RHS:{lhs(initial_dna)};OP:{expression[op_pos[pos] + initial_dna]};LHS:{rhs(initial_dna)}")
                            
                            # in any case 'st-' will have more priority then 'c
                            # c rhs = st rhs. so you can skip c rhs 
                            # only important are
                            # starting once, c lhs, st rhs
                            # or in any case if rhs is before lhs then thats a duplicate
                            # of before rhs
                            # most trustable thing is lhs
                            # lhs is almost new unless user typed same number more than 1 time
                            # dang i have to test my own system to identify what it does
                            # this thing is super complex ngl
                            
                # for multiplication
                if expression[op_pos[pos]] == "*":
                    parsed_exp.append(f"OP:{expression[op_pos[pos]]};")
                    if len(op_pos) == 1:
                        parsed_exp.append(f"RHS:{rhs(0)}")
                    if len(op_pos) == 0: raise SyntaxError("no operator found. Expected atleast 1")
                    if len(op_pos) > 1:
                        if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "sec_op":
                            parsed_exp.append(f"ST-LHS:{lhs(initial_dna)};OP:{expression[op_pos[pos] + initial_dna]};RHS:{rhs(initial_dna)}")
                        if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "first_op":
                            parsed_exp.append(f"C-RHS:{lhs(initial_dna)};OP:{expression[op_pos[pos] + initial_dna]};LHS:{rhs(initial_dna)}")
                # for division
                if expression[op_pos[pos]] == "/":
                    parsed_exp.append(f"OP:{expression[op_pos[pos]]};")
                    if len(op_pos) == 1:
                        parsed_exp.append(f"RHS:{rhs(0)}")
                    if len(op_pos) == 0: raise SyntaxError("no operator found. Expected atleast 1")
                    if len(op_pos) > 1:
                        if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "sec_op":
                            parsed_exp.append(f"ST-LHS:{lhs(initial_dna)};OP:{expression[op_pos[pos] + initial_dna]};RHS:{rhs(initial_dna)}")
                        if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "first_op":
                            parsed_exp.append(f"C-RHS:{lhs(initial_dna)};OP:{expression[op_pos[pos] + initial_dna]};LHS:{rhs(initial_dna)}")
                initial_dna += 2
                # oh my god only god knows how and what i made
                # i am foreing to my own code
                # ts more verbose than c++

    check_LR()

    return f"""EXPRESSION:{parsed_exp}"""
# sorry i am removing this
# this wont be used anymore but will still stay in the code
# its a proof (i dont know what)


def parse_expression_c():
    expression = ''
    while current() != 'END_OF_STATEMENT':
        expression += current()
        advance()
        if current() == 'EOF':
            break
    return f'EXPRESSION: {expression}'



def parse_if():
    expect("IF")
    if_condition = []
    if_statement = []
    expect("LPAREN")
    if_condition.append("LPAREN")

    while current() != "LCURLY":
        if current() == "EOF": break
        if_condition.append(resolve_variable(current()))
        if current() == "LPAREN":
            if_condition.append(current()) #
            advance()
            while current() != "RPAREN":
                if current() == "EOF": break
                if_condition.append(resolve_variable(current()))
                advance()
        advance()


    # language rule
    # if (condition) {statement}
    # a "{" is immediate after condition's ")"

    expect("LCURLY")
    if_statement.append("LCURLY")
    while current() != "RCURLY":
        if current() == "END_OF_STATEMENT":
            advance()
            continue

        if current() == "EOF":
            break

        parsed = parse_all()
        if parsed is not None:
            if_statement.append(parsed)
            continue

        raise SyntaxError(f"Unexpected token inside if statement: {current()}")

    expect("RCURLY")
    if_statement.append("RCURLY")

    elif_availabe = False
    if current() == "ELSE_IF": # we want elif right after "}"
        elif_condition = []
        elif_statement = []
        elif_availabe = True
        advance()

    if elif_availabe:
        expect("LPAREN")
        elif_condition.append("LPAREN")

        while current() != "LCURLY":
            if current() == "EOF": break
            elif_condition.append(resolve_variable(current()))
            if current() == "LPAREN":
                elif_condition.append(current())
                advance()
                while current() != "RPAREN":
                    if current() == "EOF": break
                    elif_condition.append(resolve_variable(current()))
                    advance()
            advance()

        expect("LCURLY")
        elif_statement.append("LCURLY")

        while current() != "RCURLY":
            if current() == "END_OF_STATEMENT":
                advance()
                continue

            if current() == "EOF":
                break

            parsed = parse_all()
            if parsed is not None:
                elif_statement.append(parsed)
                continue

            raise SyntaxError(f"Unexpected token inside elif statement: {current()}")

        expect("RCURLY")
        elif_statement.append("RCURLY")


    else_available = False
    if current() == "ELSE":
        else_available = True
        else_statement = []
        advance()

    if else_available:
        if current() == "LCURLY":
            else_statement.append(current())
            advance()
            while current() != "RCURLY":
                if current() == "END_OF_STATEMENT":
                    advance()
                    continue

                if current() == "EOF":
                    break

                parsed = parse_all()
                if parsed is not None:
                    else_statement.append(parsed)
                    continue

                raise SyntaxError(f"Unexpected token inside else statement: {current()}")

            expect("RCURLY")
            else_statement.append("RCURLY")


    pivot = (1 if elif_availabe else 0) | (2 if else_available else 0)

    # 0 = Neither
    # 1 = Elif only
    # 2 = Else only
    # 3 = Both

    if pivot == 0: # neither
            #f""""""
            # ifcon,state
            return f"""IF:{if_condition}:{if_statement}"""
    if pivot == 1: # elif only
            #if,elif,con,state
            return f"""IF:{if_condition}:{if_statement}:ELIF:{elif_condition}:{elif_statement}"""
    if pivot == 2: # else only
            #if,else,con,state,state
            return f"""IF:{if_condition}:{if_statement}:ELSE:{else_statement}"""
    if pivot == 3: # both
            #if,elif,cond,state,elsestate
            return f"""IF:{if_condition}:{if_statement}:ELIF:{elif_condition}:{elif_statement}:ELSE:{else_statement}"""

def parse_stop():
    expect('STOP')
    return 'STOP'

def parse_assignment():
    variable = current().removeprefix('IDENTIFIER:')
    ensure_variable_defined(variable)
    advance()

    if current() not in ('EQUAL_TO', 'PLUS_EQUAL', 'MINUS_EQUAL', 'MUL_EQUAL', 'DIV_EQUAL'):
        raise SyntaxError(f"Expected assignment operator after variable, got {current()}")

    op = current()
    advance()

    value = resolve_variable(current())
    advance()
    expect('END_OF_STATEMENT')

    if op == 'EQUAL_TO' and (
        value.startswith(("INTEGER:", "FLOAT:", "STRING:")) or value in ("TRUE", "FALSE")
    ):
        variables[variable] = value

    return f"ASSIGNMENT:{variable}:{op}:{value}"

def parse_true():
    expect('TRUE')
    return 'TRUE'

def parse_false():
    expect('FALSE')
    return 'FALSE'

def parse_all():
    token = current()

    if token == "PRINT":
        return parse_show()

    if token == "LET":
        return parse_let()

    if token == "LOOP":
        return parse_loop()

    if token == "IF":
        return parse_if()

    if token == "END_OF_STATEMENT" or token == "COMMENT":
        advance()
        return None

    if token == "EOF":
        return None

    if token == 'STOP':
        return parse_stop()

    if token.startswith('IDENTIFIER:'):
        return parse_assignment()

    if token == 'TRUE':
        return parse_true()

    if token == 'FALSE':
        return parse_false()

    raise SyntaxError(f"Unexpected Token:\n{token}")

AST = []

# main loop
while p_cursor < len(tokenized_text):
    if current() == "EOF":
        print("Parser successfully ending.")
        break

    parsed = parse_all()
    if parsed is not None:
        AST.append(parsed)

print(f'<---PARSER---> raw ast: {AST}')
print("\n")

def RawAST():
    return AST