##
# 2WF90 Algebra for Security -- Software Assignment 1 
# Integer and Modular Arithmetic
# solve.py
#
#
# Group number:
# group_number 
#
# Author names and student IDs:
# author_name_1 (author_student_ID_1) 
# author_name_2 (author_student_ID_2)
# author_name_3 (author_student_ID_3)
# author_name_4 (author_student_ID_4)
##

# Import built-in json library for handling input/output 
import json



def solve_exercise(exercise_location: str, answer_location: str):
    with open(exercise_location, "r") as exercise_file:
        exercise = json.load(exercise_file)

    r = exercise["radix"]
    x = parse(exercise["x"])
    op = exercise["operation"]

    if exercise["type"] == "integer_arithmetic":
        y = parse(exercise["y"])
        if op == "addition":
            answer = {"answer": to_string(add(x, y, r))}
        elif op == "subtraction":
            answer = {"answer": to_string(sub(x, y, r))}
        elif op == "multiplication_primary":
            answer = {"answer": to_string(mul_school(x, y, r))}
        elif op == "multiplication_karatsuba":
            answer = {"answer": to_string(mul_karatsuba(x, y, r))}
        else:  # extended_euclidean_algorithm
            raise NotImplementedError("EEA still to do")
    else:  # modular_arithmetic
        m = parse(exercise["modulus"])[1]         # modulus is never negative
        if m == [0]:
            answer = {"answer": None}             # modulus 0: undefined
        elif op == "reduction":
            answer = {"answer": to_string(mod_reduce(x, m, r))}
        elif op == "addition":
            y = parse(exercise["y"])
            answer = {"answer": to_string(mod_add(x, y, m, r))}
        elif op == "subtraction":
            y = parse(exercise["y"])
            answer = {"answer": to_string(mod_sub(x, y, m, r))}
        elif op == "multiplication":
            y = parse(exercise["y"])
            answer = {"answer": to_string(mod_mul(x, y, m, r))}
        else:  # inversion
            raise NotImplementedError("inversion needs the EEA, still to do")

    with open(answer_location, "w") as answer_file:
        json.dump(answer, answer_file, indent=4)

# You can call your function from here
# Please do not *run* code outside this block
# You can however define other functions or constants
if __name__ == '__main__':
    solve_exercise('Simple/Exercises/exercise0.json', 'Simple/Answers/answer0.json')