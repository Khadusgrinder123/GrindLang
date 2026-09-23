import Lexer
tokenized_text = Lexer.ScannedText()

p_cursor = 0

def advance():
    global p_cursor
    p_cursor += 1

def advance_by(skip):
    global p_cursor
    p_cursor += skip

def current():
    return tokenized_text[p_cursor]

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
    value = current()
    advance()
    expect("END_OF_STATEMENT")

    return {
        "type": "PRINT",
        "value": value
    }

def parse_let():
    expect("LET")
    #let int x = 10;
    print("expected DATATYPE ----", current())

    if current() in ("INTEGER", "FLOAT", "BOOLEAN", "STRING"):
        advance()
        print("expected IDENTIFIER",current())

        variable = current() # identifier
        advance()

        print("expected EQUAL_TO", current())
        expect("EQUAL_TO")

        
        print("expected VALUE", current())
        var_value = []

        if current().startswith(("INTEGER:", "FLOAT:")):
            if tokenized_text[p_cursor + 1] in Lexer.SingleOP:
                var_value.append(parse_expression())
            else:
                if tokenized_text[p_cursor - 1] == "EQUAL_TO":
                    if tokenized_text[p_cursor - 3] in ("INTEGER", "FLOAT", "BOOLEAN", "STRING"):
                        if tokenized_text[p_cursor - 4] == "LET":
                            var_value.append(current())
                else: raise SyntaxError(
                    "undefined number without a parent"
                )
                advance()


        expect("END_OF_STATEMENT")

        return {
            "type": "VARIABLE_DECLARATION",
            "Variable": variable,
            "VariableValue": var_value
        }
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

        if current() == "PRINT":
            loop_work.append(parse_show())
            continue

        if current() == "LET":
            loop_work.append(parse_let())
            continue

        if current() == "LOOP":
            loop_work.append(parse_loop())
            continue

        raise SyntaxError(f"Unexpected token inside loop: {current()}")

    expect("RCURLY")

    return {
        "type": "LOOP",
        "work": loop_work,
        "reps": reps
    }

def parse_expression():    
    expression = []

    while current() not in ("END_OF_STATEMENT", "EOF"):
        expression.append(current())
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
    
        for i in range(len(expression)):
            # 3-2-3

            if expression[op_pos[pos] + initial_dna] == "EOE": break

            parsed_exp.append(f"STARTING: {expression[op_pos[0] - 1]};")

            # for minus
            if expression[op_pos[pos]] == "-":
                parsed_exp.append(f"OP: {expression[op_pos[pos]]};")
                if len(op_pos) == 1:
                    parsed_exp.append(f"RHS: {rhs(0)}")
                if len(op_pos) == 0: raise SyntaxError("no operator found. Expected atleast 1")
                if len(op_pos) > 1:
                    # for higher or equal power
                    if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "sec_op":
                        parsed_exp.append(f"ST- LHS: {lhs(initial_dna)}; OP:{expression[op_pos[pos] + initial_dna]}; RHS: {rhs(initial_dna)}")
                    # for lower power
                    if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "first_op":
                        parsed_exp.append(f"RHS: {lhs(initial_dna)}; OP: {expression[op_pos[pos] + initial_dna]}; LHS: {rhs(initial_dna)}")

            # for addition
            if expression[op_pos[pos]] == "+":
                parsed_exp.append(f"OP: {expression[op_pos[pos]]};")
                if len(op_pos) == 1:
                    parsed_exp.append(f"RHS: {rhs(0)}")
                if len(op_pos) == 0: raise SyntaxError("no operator found. Expected atleast 1")
                if len(op_pos) > 1:
                    if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "sec_op":
                        parsed_exp.append(f"ST- LHS: {lhs(initial_dna)}; OP:{expression[op_pos[pos] + initial_dna]}; RHS: {rhs(initial_dna)}")
                    elif check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "first_op":
                        parsed_exp.append(f"C- RHS: {lhs(initial_dna)}; OP: {expression[op_pos[pos] + initial_dna]}; LHS: {rhs(initial_dna)}")

            # for multiplication
            if expression[op_pos[pos]] == "*":
                parsed_exp.append(f"OP: {expression[op_pos[pos]]};")
                if len(op_pos) == 1:
                    parsed_exp.append(f"RHS: {rhs(0)}")
                if len(op_pos) == 0: raise SyntaxError("no operator found. Expected atleast 1")
                if len(op_pos) > 1:
                    if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "sec_op":
                        parsed_exp.append(f"ST- LHS: {lhs(initial_dna)}; OP:{expression[op_pos[pos] + initial_dna]}; RHS: {rhs(initial_dna)}")
                    if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "first_op":
                        parsed_exp.append(f"C- RHS: {lhs(initial_dna)}; OP: {expression[op_pos[pos] + initial_dna]}; LHS: {rhs(initial_dna)}")

            # for division
            if expression[op_pos[pos]] == "/":
                parsed_exp.append(f"OP: {expression[op_pos[pos]]};")
                if len(op_pos) == 1:
                    parsed_exp.append(f"RHS: {rhs(0)}")
                if len(op_pos) == 0: raise SyntaxError("no operator found. Expected atleast 1")
                if len(op_pos) > 1:
                    if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "sec_op":
                        parsed_exp.append(f"ST- LHS: {lhs(initial_dna)}; OP:{expression[op_pos[pos] + initial_dna]}; RHS: {rhs(initial_dna)}")
                    if check_power(expression[op_pos[pos]], expression[op_pos[pos] + initial_dna]) == "first_op":
                        parsed_exp.append(f"C- RHS: {lhs(initial_dna)}; OP: {expression[op_pos[pos] + initial_dna]}; LHS: {rhs(initial_dna)}")

            initial_dna += 2

    check_LR()

    return {
        "type": "EXPRESSION",
        "value": parsed_exp
    }


def parse_if():
    expect("IF")
    if_condition = []
    if_statement = []
    expect("LPAREN")
    if_condition.append("LPAREN")

    while current() != "LCURLY":
        if current() == "EOF": break
        if_condition.append(current())
        if current() == "LPAREN":
            if_condition.append(current()) #
            advance()
            while current() != "RPAREN":
                if current() == "EOF": break
                if_condition.append(current())
                advance()
        advance()

    print(current())
    print(if_condition)

    # language rule
    # if (condition) {statement}
    # a "{" is immediate after condition's ")"

    expect("LCURLY")
    if_statement.append("LCURLY")
    while current() != "RCURLY":

        if current() == "IF":
            if_statement.append(parse_if())
            continue

        if current() == "LET":
            if_statement.append(parse_let())
            continue

        if current() == "PRINT":
            if_statement.append(parse_show())
            continue

        if current() == "LOOP":
            if_statement.append(parse_loop())
            continue

        if current() == "END_OF_STATEMENT":
            advance()
            continue

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
            elif_condition.append(current())
            if current() == "LPAREN":
                elif_condition.append(current())
                advance()
                while current() != "RPAREN":
                    if current() == "EOF": break
                    elif_condition.append(current())
                    advance()
            advance()

        expect("LCURLY")
        elif_statement.append("LCURLY")

        while current() != "RCURLY":

            if current() == "IF":
                elif_statement.append(parse_if())
                continue

            if current() == "LET":
                elif_statement.append(parse_let())
                continue

            if current() == "PRINT":
                elif_statement.append(parse_show())
                continue

            if current() == "LOOP":
                elif_statement.append(parse_loop())
                continue

            if current() == "END_OF_STATEMENT":
                advance()
                continue

        expect("RCURLY")
        elif_statement.append("RCURLY")

    print("elif condition", elif_condition)
    print("elif statement", elif_statement)

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
                if current() == "IF":
                    else_statement.append(parse_if())
                    continue

                if current() == "LET":
                    else_statement.append(parse_let())
                    continue

                if current() == "PRINT":
                    else_statement.append(parse_show())
                    continue

                if current() == "LOOP":
                    else_statement.append(parse_loop())
                    continue

                if current() == "END_OF_STATEMENT":
                    advance()
                    continue

            expect("RCURLY")
            else_statement.append("RCURLY")

    print("else statement:",else_statement)


    pivot = (1 if elif_availabe else 0) | (2 if else_available else 0)

    # 0 = Neither
    # 1 = Elif only
    # 2 = Else only
    # 3 = Both

    if pivot == 0: # neither
            return {
            "type": "IF",
            "condition": if_condition,
            "statement": if_statement
        }
    if pivot == 1: # elif only
            return {
            "type": "IF",
            "condition": if_condition,
            "statement": if_statement,
            "elif condition": elif_condition,
            "elif statement": elif_statement
        }
    if pivot == 2: # else only
            return {
            "type": "IF",
            "condition": if_condition,
            "statement": if_statement,
            "else statement": else_statement
        }
    if pivot == 3: # both
            return {
            "type": "IF",
            "condition": if_condition,
            "statement": if_statement,
            "elif condition": elif_condition,
            "elif statement": elif_statement,
            "else statement": else_statement
        }



AST = []

# main loop
while p_cursor < len(tokenized_text):

    if tokenized_text[p_cursor] == "PRINT":
        AST.append(parse_show())

    elif tokenized_text[p_cursor] == "LET":
        AST.append(parse_let())

    elif tokenized_text[p_cursor] == "LOOP":
        AST.append(parse_loop())

    elif tokenized_text[p_cursor] == "END_OF_STATEMENT" or tokenized_text[p_cursor] == "COMMENT":
        advance()

    elif tokenized_text[p_cursor] == "EOF":
        print("Parser successfully ending.")
        break

    elif tokenized_text[p_cursor].startswith(("INTEGER:", "FLOAT:")):
        if tokenized_text[p_cursor + 1] in Lexer.SingleOP:
            AST.append(parse_expression())
        else:
            if tokenized_text[p_cursor - 1] == "EQUAL_TO":
                if tokenized_text[p_cursor - 3] in ("INTEGER", "FLOAT", "BOOLEAN", "STRING"):
                    if tokenized_text[p_cursor - 4] == "LET":
                        pass
            else: raise SyntaxError(
                "undefined number without a parent"
            )
            advance()

    elif tokenized_text[p_cursor] == "IF":
        AST.append(parse_if())

    else:
        raise SyntaxError(
            f"Unexpected Token:\n{current()}"
        )


print("---PARSER---", AST)
print("\n\n\n")