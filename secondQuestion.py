''' 
Question 2: Expression Evaluator
'''
from pathlib import Path


def format_number(value):
 # whole number should be displayed without decimal points. 
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def tokenize(expression):
#the inpuut expression converts into tokens. 
    tokens = []
    i = 0

    while i < len(expression):
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            start = i
            dot_count = 0

            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                if expression[i] == ".":
                    dot_count += 1
                i += 1

            number_text = expression[start:i]

            if number_text == "." or dot_count > 1:
                raise ValueError("Invalid number")

            tokens.append(("NUM", number_text))
            continue

        if ch in "+-*/":
            tokens.append(("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
            continue

        if ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1
            continue

        raise ValueError(f"Invalid character: {ch}")

    tokens.append(("END", ""))
    return tokens


def tokens_to_string(tokens):
    #Converts token list into the required output format.
    parts = []
    for token_type, token_value in tokens:
        if token_type == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{token_type}:{token_value}]")
    return " ".join(parts)


def current_token(tokens, index):
    #Returns the current token.
    return tokens[index]


def make_number_node(value):
    #Creates a number node.
    return ("num", float(value))


def make_binary_node(op, left, right):
    #Creates a binary operator node.
    return ("bin", op, left, right)


def make_neg_node(child):
    #Creates a unary negative node.
    return ("neg", child)


def tree_to_string(node):
    #Converts the parse tree into the required prefix string format.

    kind = node[0]

    if kind == "num":
        return format_number(node[1])

    if kind == "neg":
        return f"(neg {tree_to_string(node[1])})"

    if kind == "bin":
        op = node[1]
        left = tree_to_string(node[2])
        right = tree_to_string(node[3])
        return f"({op} {left} {right})"


def evaluate_tree(node):
    #Evaluates the parse tree and returns the numerical result. Handles errors like division by zero.
    kind = node[0]

    if kind == "num":
        return node[1]

    if kind == "neg":
        return -evaluate_tree(node[1])

    if kind == "bin":
        op = node[1]
        left_value = evaluate_tree(node[2])
        right_value = evaluate_tree(node[3])

        if op == "+":
            return left_value + right_value
        if op == "-":
            return left_value - right_value
        if op == "*":
            return left_value * right_value
        if op == "/":
            if right_value == 0:
                raise ZeroDivisionError("Division by zero")
            return left_value / right_value


def parse_expression(tokens, index):
    #Handles + and - operations.
    left_node, index = parse_term(tokens, index)

    while True:
        token_type, token_value = current_token(tokens, index)

        if token_type == "OP" and token_value in "+-":
            op = token_value
            right_node, index = parse_term(tokens, index + 1)
            left_node = make_binary_node(op, left_node, right_node)
        else:
            break

    return left_node, index


def parse_term(tokens, index):
    '''Handles *, /, and implicit multiplication. 
    Implicit multiplication has higher precedence than + and - but the same precedence as explicit * and /.'''
    left_node, index = parse_factor(tokens, index)

    while True:
        token_type, token_value = current_token(tokens, index)

        # Explicit multiplication or division
        if token_type == "OP" and token_value in "*/":
            op = token_value
            right_node, index = parse_factor(tokens, index + 1)
            left_node = make_binary_node(op, left_node, right_node)

        # Implicit multiplication
        elif token_type in ("NUM", "LPAREN"):
            right_node, index = parse_factor(tokens, index)
            left_node = make_binary_node("*", left_node, right_node)

        else:
            break

    return left_node, index


def parse_factor(tokens, index):
  #Handles unary minus. Unary plus is not supported and will raise an error.
    token_type, token_value = current_token(tokens, index)

    if token_type == "OP" and token_value == "-":
        child_node, index = parse_factor(tokens, index + 1)
        return make_neg_node(child_node), index

    if token_type == "OP" and token_value == "+":
        raise ValueError("Unary plus is not supported")

    return parse_primary(tokens, index)


def parse_primary(tokens, index):
   #Handles numbers and parenthesized expressions.
    token_type, token_value = current_token(tokens, index)

    if token_type == "NUM":
        return make_number_node(token_value), index + 1

    if token_type == "LPAREN":
        node, index = parse_expression(tokens, index + 1)

        if current_token(tokens, index)[0] != "RPAREN":
            raise ValueError("Missing closing parenthesis")

        return node, index + 1

    raise ValueError("Expected number or '('")


def evaluate_expression(expression):
    #Evaluates a single expression string and returns a dictionary with input, tree, tokens, and result.
    original_input = expression.rstrip("\n")

    
    try:
        tokens = tokenize(original_input)
        token_string = tokens_to_string(tokens)
    except Exception:
        return {
            "input": original_input,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }

    try:
        tree, index = parse_expression(tokens, 0)

        if current_token(tokens, index)[0] != "END":
            raise ValueError("Unexpected trailing tokens")

        tree_string = tree_to_string(tree)
    except Exception:
        return {
            "input": original_input,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }
    try:
        result = evaluate_tree(tree)
    except Exception:
        result = "ERROR"

    return {
        "input": original_input,
        "tree": tree_string,
        "tokens": token_string,
        "result": result
    }


def result_to_output_string(result):
    #Converts result value into required output format.
    if result == "ERROR":
        return "ERROR"
    return format_number(result)


def write_output_file(results, output_path):
    #Writes the results to output.txt in the specified format.
    lines = []

    for item in results:
        lines.append(f"Input: {item['input']}")
        lines.append(f"Tree: {item['tree']}")
        lines.append(f"Tokens: {item['tokens']}")
        lines.append(f"Result: {result_to_output_string(item['result'])}")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def evaluate_file(input_path: str) -> list[dict]:
    #Reads expressions from the input file, evaluates them, and writes the results to output.txt. Returns a list of result dictionaries.
    input_file = Path(input_path)

    with open(input_file, "r", encoding="utf-8") as file:
        expressions = file.readlines()

    results = [evaluate_expression(expr) for expr in expressions]

    output_file = input_file.parent / "output.txt"
    write_output_file(results, output_file)

    return results


if __name__ == "__main__":
    input_name = input("Enter input file name: ").strip()
    results = evaluate_file(input_name)
    print(f"Processed {len(results)} expression(s).")
    print("Output written to output.txt")