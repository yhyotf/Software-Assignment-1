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
# Yahya Outifa (2247127) 
# Aly Elakkad (2272121)
# author_name_3 (author_student_ID_3)
# author_name_4 (author_student_ID_4)
##

# Import built-in json library for handling input/output 
import json
DIGITS = "0123456789ABCDEF"


def addition(x, y, b): 
    m, n = len(x), len(y)
    z, c =  [], 0
    x = x + [0] * (max(m, n) - m)                  # step 1.2: x_i ← 0 for m ≤ i < max{m,n}
    y = y + [0] * (max(m, n) - n)                 # step 1.2: y_i ← 0 for n ≤ i < max{m,n}
    for i in range(max(m, n)):                     
        zi = x[i] + y[i] + c                            
        if zi >= b:
            zi -= b
            c = 1
        else:
            c = 0
        z.append(zi)
        if c == 1:
            z.append(1)                            
        return z


# ---- Algorithm 1.2 (Addition) ----------------------------------
# ---- Algorithm 1.2 (Addition), for x, y in N -------------------
def add_mag(x, y, b):
    """Algorithm 1.2, steps 1.1 - 3.2. x and y are mags (x, y in N), any lengths.
    Returns the mag x + y. Pad the shorter one with zeros (steps 1.2, 1.3); the carry is 0 or 1;
    a leftover carry becomes a new top digit (step 3.1)."""
    m, n = len(x), len(y)
    c = 0                                          # 1.1
    x = x + [0] * (max(m, n) - m)                  # 1.2  x_i <- 0 for m <= i < max{m,n}
    y = y + [0] * (max(m, n) - n)                  # 1.3  y_i <- 0 for n <= i < max{m,n}
    z = [0] * max(m, n)
    for i in range(max(m, n)):                     # 2.1
        z[i] = x[i] + y[i] + c                     # 2.2
        if z[i] >= b:                              # 2.3
            z[i] = z[i] - b
            c = 1
        else:
            c = 0
    if c == 1:                                     # 3.1
        k = max(m, n) + 1
        z.append(1)                                #      z_{k-1} = 1
    else:
        k = max(m, n)
    return z[:k]                                   # 3.2

# ---- Algorithm 1.3 (Subtraction), for x > y in N ---------------
def sub_mag(x, y, b):
    """Algorithm 1.3, steps 1.1 - 3.3. x and y are mags with x >= y.
    Returns the mag x - y WITHOUT leading zeros (step 3.2 removes them; the result of 100 - 99 is [1])."""
    m, n = len(x), len(y)
    c = 0                                          # 1.1
    y = y + [0] * (m - n)                          # 1.2  y_i <- 0 for n <= i < m
    z = [0] * m
    for i in range(m):                             # 2.1
        z[i] = x[i] - y[i] - c                     # 2.2
        if z[i] < 0:                               # 2.3
            z[i] = z[i] + b
            c = 1
        else:
            c = 0
    k = m                                          # 3.1
    while k >= 2 and z[k - 1] == 0:                # 3.2
        k = k - 1
    return z[:k]                                   # 3.3

# ---- Signed addition and subtraction (the text around 1.2 / 1.3) ----
def add(x, y, b):
    """Signed addition of two nums. Returns a num.
    Follow the text of the notes: addition of 0 is trivial; two positives or two negatives -> add_mag and
    keep the sign; a positive and a negative -> subtraction of the two magnitudes (larger minus smaller)
    with the sign of the larger. Equal magnitudes with different signs -> (1, [0])."""
    sx, mx = x
    sy, my = y
    if mx == [0]:                                  # "Addition of 0 is trivial."
        return y
    if my == [0]:
        return x
    if sx == sy:                                   # two positives: Alg. 1.2
        return (sx, add_mag(mx, my, b))            # two negatives: Alg. 1.2, "adjusting the sign of the output"
    # a positive and a negative number: "equivalent to subtraction of two positive numbers"
    if mx == my:
        return (1, [0])
    if (len(mx), mx[::-1]) > (len(my), my[::-1]):  # |x| > |y|
        return (sx, sub_mag(mx, my, b))            # Alg. 1.3, sign of the larger
    return (sy, sub_mag(my, mx, b))                # "swapping the two numbers and adjusting the sign"

def sub(x, y, b):
    """Signed subtraction x - y of two nums. Returns a num.
    Follow the text of the notes: subtraction of 0 or from 0 is trivial; different signs -> add the
    magnitudes; equal signs -> subtract the magnitudes, swapping them and adjusting the sign when
    |x| < |y|. Do not just call add(x, neg(y))."""
    sx, mx = x
    sy, my = y
    if my == [0]:                                  # "Subtraction of 0 or from 0 is trivial."
        return x
    if mx == [0]:
        return (-sy, my)
    if sx != sy:                                   # positive and negative: "addition of two positive numbers,
        return (sx, add_mag(mx, my, b))            #  and adjusting the sign of the output"
    # two positives, or two negatives: "subtraction of two positive numbers and adjusting the sign"
    if mx == my:
        return (1, [0])
    if (len(mx), mx[::-1]) > (len(my), my[::-1]):  # |x| > |y|
        return (sx, sub_mag(mx, my, b))            # Alg. 1.3
    return (-sx, sub_mag(my, mx, b))               # swap the two numbers, adjust the sign

# ---- Algorithm 1.4 (Naive multiplication) -----------------------
def mul_mag_school(x, y, b):
    """Algorithm 1.4, steps 1.1 - 3.2. Primary school multiplication of two mags.
    Returns the mag x * y. Two deviations from the printed notes (they drop the top word):
    allocate m + n words in 1.1, and in 3.1 the output length k is m + n - 1 if the top word is 0, else m + n.
    (A zero factor may give leading zeros; make_num in mul_school cleans them up.)"""
    ...

def mul_school(x, y, b):
    """Signed multiplication with the primary school method. x, y are nums, returns a num.
    Multiply the magnitudes with mul_mag_school and adjust the sign (product of the signs)."""
    ...

# ---- Algorithm 1.5 (Karatsuba) ----------------------------------
def karatsuba_mag(x, y, n, b):
    """Algorithm 1.5, steps 1.1 - 3.2. x and y are mags of at most n digits (leading zero digits allowed).
    Returns the mag x * y (leading zeros allowed).
    - Base case (the notes leave it out): if n <= KARATSUBA_THRESHOLD, return mul_mag_school(x, y, b).
    - If n is odd, n <- n + 1; pad x and y with zeros to exactly n digits; split at n/2.
    - The call for (x_hi + x_lo)(y_hi + y_lo) gets wordlength n/2 + 1, because the sums can carry."""
    ...

def mul_karatsuba(x, y, b):
    """Signed multiplication with Karatsuba. x, y are nums, returns a num.
    Calls karatsuba_mag with n = the larger of the two lengths, then adjusts the sign (use make_num)."""
    ...

# ---- Algorithm 1.6 (Division with remainder) --------------------
def divmod_mag(x, y, b):
    """Algorithm 1.6, steps 1.1 - 3.2. x and y are mags, y != [0]. Returns (q, r), both mags without leading
    zeros, with x = q*y + r and 0 <= r < y. Find each q_i by subtracting y*b^i from r while it fits.
    Also correct for x < y (q = [0], r = x). Needed by the extended Euclidean algorithm."""
    ...

# ---- Algorithm 2.2 (Extended Euclidean Algorithm) ---------------
def ext_euclid(x, y, b):
    """Algorithm 2.2, steps 1.1 - 3.4. x and y are nums, not both zero.
    Returns (d, u, v): three nums with d = gcd(x, y) >= 0 and u*x + v*y = d.
    Follow the notes exactly (Bezout coefficients are not unique, the grader expects those of Algorithm 2.2):
    work on |x| and |y|, get q and r from divmod_mag, update the coefficients with the signed mul and sub,
    and fix the signs of u and v at the end (steps 3.2, 3.3).
    Check: ext_euclid(96, 40) -> d = 8, u = -2, v = 5."""
    ...


# ===============================================================
# MODULAR ARITHMETIC   (m is a MAG with m != [0]; uses the integer arithmetic above)
# ===============================================================

# ---- Algorithm 2.5 (Modular reduction with radix b) --------------
def mod_reduce(x, m, b):
    """Algorithm 2.5, steps 1.1 - 3.2. x is a num (any sign), m is a mag != [0].
    Returns a num y with 0 <= y < m and y = x (mod m). Work on |x|: for i = k-n down to 0 subtract m*b^i
    while it fits; for a negative x with a non-zero remainder x', the result is m - x' (step 3.1).
    Also correct for m = [1] (result 0)."""
    ...

# The course assumes reduced inputs for Algorithms 2.7 - 2.9; the assignment allows any integer,
# so each of them first reduces x and y with mod_reduce.

# ---- Algorithm 2.7 (Modular addition) ----------------------------
def mod_add(x, y, m, b):
    """Algorithm 2.7. x and y are nums (any sign), m is a mag != [0]. Returns the num (x + y) mod m in [0, m).
    Reduce x and y first, then z' = x + y, and subtract m once if z' >= m."""
    ...

# ---- Algorithm 2.8 (Modular subtraction) -------------------------
def mod_sub(x, y, m, b):
    """Algorithm 2.8. x and y are nums (any sign), m is a mag != [0]. Returns the num (x - y) mod m in [0, m).
    Reduce x and y first, then z' = x - y, and add m once if z' < 0."""
    ...

# ---- Algorithm 2.9 (Modular multiplication, naive) ----------------
def mod_mul(x, y, m, b):
    """Algorithm 2.9. x and y are nums (any sign), m is a mag != [0]. Returns the num (x * y) mod m in [0, m).
    Reduce x and y first, multiply with any multiplication method, then reduce the product."""
    ...

# ---- Algorithm 2.11 (Modular inversion) ---------------------------
def mod_inverse(x, m, b):
    """Algorithm 2.11, based on the extended Euclidean algorithm. x is a num (any sign), m is a mag != [0].
    Returns the num x^-1 mod m in [0, m), or None if x has no inverse (gcd(x, m) != 1).
    Watch out: as printed, the algorithm can return a NEGATIVE coefficient (the inverse of 3 mod 7 comes out
    as -2, the answer is 5), so add m when needed. Decide and test the edge cases: x = 0, x a multiple of m,
    and m = [1] (every x is invertible, the answer is 0)."""
    ...


# ===============================================================
# SOLVING AN EXERCISE
# ===============================================================
def solve_exercise(exercise_location: str, answer_location: str):
    with open(exercise_location, "r") as exercise_file:
        exercise = json.load(exercise_file)

    b = exercise["radix"]
    op = exercise["operation"]

    # Strings -> nums. The digits already are radix b digits, so we only map them to numbers and
    # reverse them (least significant first). Done once for every operand the exercise has.
    operands = {}
    for key in ("x", "y", "modulus"):
        if key in exercise:
            s = exercise[key]
            sign = 1
            if s[0] == "-":
                sign, s = -1, s[1:]
            mag = [DIGITS.index(ch) for ch in reversed(s)]
            while len(mag) > 1 and mag[-1] == 0:   # remove leading zeros
                mag.pop()
            if mag == [0]:
                sign = 1                           # never -0
            operands[key] = (sign, mag)
    x = operands["x"]

    # results: answer key -> num (None = undefined, written as null)
    if exercise["type"] == "integer_arithmetic":
        y = operands["y"]
        if op == "addition":
            results = {"answer": add(x, y, b)}
        elif op == "subtraction":
            results = {"answer": sub(x, y, b)}
        elif op == "multiplication_primary":
            results = {"answer": mul_school(x, y, b)}
        elif op == "multiplication_karatsuba":
            results = {"answer": mul_karatsuba(x, y, b)}
        else:  # extended_euclidean_algorithm
            raise NotImplementedError("extended_euclidean_algorithm still to do")
    else:  # modular_arithmetic
        m = operands["modulus"][1]                 # the modulus is never negative
        if m == [0]:
            results = {"answer": None}             # modulus 0: undefined (also for inversion)
        elif op == "reduction":
            results = {"answer": mod_reduce(x, m, b)}
        elif op == "addition":
            results = {"answer": mod_add(x, operands["y"], m, b)}
        elif op == "subtraction":
            results = {"answer": mod_sub(x, operands["y"], m, b)}
        elif op == "multiplication":
            results = {"answer": mod_mul(x, operands["y"], m, b)}
        else:  # inversion
            raise NotImplementedError("inversion still to do")

    # nums -> strings: reverse the digits back, map them to characters, put the sign in front.
    answer = {}
    for key, num in results.items():
        if num is None:
            answer[key] = None
        else:
            sign, mag = num
            s = "".join(DIGITS[d] for d in reversed(mag))
            answer[key] = "-" + s if sign < 0 else s

    with open(answer_location, "w") as answer_file:
        json.dump(answer, answer_file, indent=4)


if __name__ == '__main__':
    solve_exercise('Simple/Exercises/exercise0.json', 'Simple/MyAnswers/answer0.json')