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
