
# main function, responsible for computing the values of variables
def find_variables(clauses, variables):

    number_of_clauses = len(clauses)
    number_of_variables = len(variables)

    # we've found the values of the variables that satisfy all the clauses
    if number_of_clauses == 0:
        return clauses, variables, True

    # otherwise we check all the current clauses for any singletons
    for cl in range(number_of_clauses):

        clause = clauses[cl]
        # checks what variables are in the clause
        check = [ch for ch in range(len(clause)) if clause[ch] != 0]
        print("clause and check:")
        print(clause)
        # if there is only one variable in the clause
        if len(check) == 1:

            # we get the corresponding index
            index = int(check[0])
            # we get the expected value, either 1 or -1
            value = clause[index]
            print(index)
            print(value)
            # if this variable is already set to the opposite value,
            # then we have a contradiction and this combination of
            # variable values is incorrect
            if variables[index] == -1 * value:
                return clauses, variables, False

            # otherwise, this might be a viable solution, so we add
            # our found value into the variable values
            variables[index] = value

            # then we delete the currect clause because we've already
            # satisfied it
            clauses = clauses[:cl] + clauses[cl+1:]

            number_of_clauses -= 1

            # now we have to check the other clauses and remove all
            # the ones we've already satisfied with this last addition
            delete = []

            # we go over all the remaining clauses
            for a in range(number_of_clauses):

                acl = clauses[a]

                # if the clause is satisfied, we add to the delete list
                if acl[index] == value:
                    delete.append(a)
                # otherwise, if the opposite value appears in the clause
                # we delete that variable from the clause but don't add
                # it to the delete list
                elif acl[index] == -1 * value:
                    clauses[a][index] = 0
                    # if this deletion makes it so that the clause is empty,
                    # then the clause is automatically false and this
                    # variable value combination is incorrect
                    if all(val == 0 for val in clauses[a]):
                        return clauses, variables, False

            # we only leave the clauses that aren't "deleted"
            clauses = [clauses[clause_no] for clause_no in range(number_of_clauses)
                       if clause_no not in delete]

            # now we have to continue the search with this combination,
            # if we get a mistake somewhere down the line and it returns
            # false, then we've already made a mistake here, so we just
            # return false at this point
            return find_variables(clauses, variables)

    # if there aren't any singletons, then we have to just try and add a
    # variable value
    for clause_no in range(number_of_clauses):
        for var_no in range(number_of_variables):

            # we get the current variable value in the current clause
            var_val = clauses[clause_no][var_no]

            # if it has no value, we ignore it
            if var_val == 0:
                continue

            temp_clauses = clauses.copy()
            temp_variables = variables.copy()

            # we add the variable value to the variable value combination
            # and delete the current clause
            temp_variables[var_no] = var_val
            temp_clauses = temp_clauses[:clause_no] + temp_clauses[clause_no+1:]

            no_temp_clauses = number_of_clauses - 1

            incorrect = False
            delete = []

            for a in range(no_temp_clauses):

                acl = temp_clauses[a]

                if acl[var_no] == var_val:
                    delete.append(a)
                elif acl[var_no] == -1 * var_val:
                    temp_clauses[a][var_no] = 0
                    if all(val == 0 for val in temp_clauses[a]):
                        incorrect = True
                        break

            if incorrect:
                continue

            temp_clauses = [temp_clauses[x] for x in range(len(temp_clauses)) if x not in delete]

            tcl, tvar, found = find_variables(temp_clauses, temp_variables)

            if found:
                return tcl, tvar, found

    return clauses, variables, False


name = "test"
task_name = name + ".txt"
solution_name = name + "_solution.txt"

with open(task_name) as data:
    lines = data.read().splitlines()

info_row = lines[2].split(" ")
no_columns = int(info_row[2])
no_rows = int(info_row[3])

starting_clauses = []

for i in range(3, len(lines)):

    one_clause = lines[i].split(" ")[:-2]
    clause_with_values = [0 for k in range(no_columns + 1)]
    for j in range(len(one_clause)):
        number = int(one_clause[j])
        if number > 0:
            clause_with_values[number] = 1
        else:
            clause_with_values[-1 * number] = -1

    starting_clauses.append(clause_with_values)


starting_variables = [0 for var in range(no_columns + 1)]
print(starting_clauses)
final_clauses, final_variables, found_solution = find_variables(starting_clauses, starting_variables)

if found_solution:
    variables_index_values = [str(index * final_variables[index]) for index in
                              range(len(final_variables)) if final_variables[index] != 0]
    variables_string = " ".join(variables_index_values)
    print(variables_string)
else:
    print(False)

