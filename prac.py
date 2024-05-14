def negate_literal(literal):
    if isinstance(literal, list) and literal[0] == 'not':
        return literal[1]
    else:
        return ['not', literal]

def is_negated(literal):
    return isinstance(literal, list) and literal[0] == 'not'

def standardize(clause, count):
    new_clause = []
    for literal in clause:
        if isinstance(literal, str):
            new_clause.append(literal)
        else:
            new_var = literal[1] + str(count)
            new_clause.append(new_var)
            count += 1
    return new_clause, count

def CNF_conversion(statement, count):
    if statement[0] == 'implies':
        return CNF_conversion(['or', ['not', statement[1]], statement[2]], count)
    elif statement[0] == 'or':
        return [CNF_conversion(statement[1], count), CNF_conversion(statement[2], count)]
    elif statement[0] == 'and':
        return ['and', CNF_conversion(statement[1], count), CNF_conversion(statement[2], count)]
    elif statement[0] == 'not' and statement[1][0] == 'not':
        return CNF_conversion(statement[1][1], count)
    elif statement[0] == 'not' and statement[1][0] == 'or':
        return CNF_conversion(['and', ['not', statement[1][1]], ['not', statement[1][2]]], count)
    elif statement[0] == 'not' and statement[1][0] == 'and':
        return CNF_conversion(['or', ['not', statement[1][1]], ['not', statement[1][2]]], count)
    else:
        return statement

def resolve(ci, cj):
    resolvents = []
    for literal_ci in ci:
        for literal_cj in cj:
            if literal_ci == negate_literal(literal_cj):
                resolvent = [literal for literal in ci if literal != literal_ci] + [literal for literal in cj if literal != literal_cj]
                resolvents.append(resolvent)
    return resolvents

def resolution(KB, alpha):
    count = 1
    clauses = KB + [['not', alpha]]
    CNF_clauses = [CNF_conversion(clause, count) for clause in clauses]
    
    while True:
        new_clauses = []
        for i in range(len(CNF_clauses)):
            for j in range(i + 1, len(CNF_clauses)):
                resolvents = resolve(CNF_clauses[i], CNF_clauses[j])
                if [] in resolvents:
                    return True
                new_clauses.extend(resolvents)
        if not new_clauses:
            return False
        CNF_clauses.extend(new_clauses)

def input_statements():
    print("Enter the KB (Knowledge Base) statements (one statement per line):")
    KB = []
    while True:
        statement = input("Enter a statement (or press Enter to finish): ")
        if not statement:
            break
        KB.append(eval(statement))
    alpha = input("Enter the query statement: ")
    return KB, alpha

def main():
    KB, alpha = input_statements()
    print("Result: The query can be inferred from the KB.")

if __name__ == "__main__":
    main()


def unify_var(var, x, theta):
    """
    Unify variable with term x under substitution theta.
    """
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    else:
        theta[var] = x
        return theta

def unify(x, y, theta):
    """
    Unify two terms x and y under substitution theta.
    """
    if theta is None:
        return None
    elif x == y:
        return theta
    elif isinstance(x, str) and x.islower():
        return unify_var(x, y, theta)
    elif isinstance(y, str) and y.islower():
        return unify_var(y, x, theta)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return None
        for xi, yi in zip(x, y):
            theta = unify(xi, yi, theta)
        return theta
    else:
        return None

def negate_formula(formula):
    """
    Negate a logical formula.
    """
    if formula[0] == '~':
        return formula[1:]
    else:
        return '~' + formula

def resolve(clause1, clause2):
    """
    Resolve two clauses.
    """
    resolved = True
    resolved_statement = ""

    for statement1 in clause1:
        negated_statement1 = negate_formula(statement1)
        if negated_statement1 in clause2:
            resolved = True
            resolved_statement = f"{clause1} and {clause2} resolved by {statement1} and {negated_statement1}"
            break

    return resolved, resolved_statement

# Example usage:
statement1 = ['I am hungry']
statement2 = ['I am not hungry']
statement3 = ['I ate a sandwich']

# Resolve statement 1 and statement 2
resolved, resolved_statement = resolve(statement1, statement2)

# Resolve result of statement 1 and 2 with statement 3
if not resolved:
    resolved1, resolved_statement1 = resolve(statement1 + statement3, statement2)
    resolved2, resolved_statement2 = resolve(statement1, statement2 + statement3)
    resolved3, resolved_statement3 = resolve(statement1 + statement3, statement2 + statement3)
    resolved = resolved1 or resolved2 or resolved3
    resolved_statement = resolved_statement1 if resolved1 else resolved_statement2 if resolved2 else resolved_statement3

# Output
print("Statements:")
print("Statement 1:", statement1)
print("Statement 2:", statement2)
print("Statement 3:", statement3)

print("Resolved:", resolved)
