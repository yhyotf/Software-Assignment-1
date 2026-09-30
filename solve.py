##
# 2WF90 Algebra for Security -- Software Assignment 1 
# Integer and Modular Arithmetic
# solve.py
#
#
# Group number:
# 49
#
# Author names and student IDs:
# Yahya Outifa (2247127) 
# Aly Elakkad (2272121)
# Spyros Katsileros (2113325)
# author_name_4 (author_student_ID_4)
##

# Import built-in json library for handling input/output 
import json
DIGITS = "0123456789ABCDEF"
KARATSUBA_THRESHOLD = 5 

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
    m, n = len(x), len(y)
    z = [0] * (m + n)                              # 1.1  z_i <- 0 (m + n words, see above)
    for i in range(m):                             # 2.1
        c = 0                                      # 2.2
        for j in range(n):                         # 2.3
            t = z[i + j] + x[i] * y[j] + c         # 2.4  at most (b-1) + (b-1)^2 + (b-1) = b^2 - 1
            c = t // b                             # 2.5  the carry is the top digit of t
            z[i + j] = t - c * b                   # 2.6  keep the bottom digit
        z[i + n] = c                               # 2.7
    if z[m + n - 1] == 0:                          # 3.1
        k = m + n - 1
    else:
        k = m + n
    return z[:k]                                   # 3.2

def mul_school(x, y, b):
    """Signed multiplication with the primary school method. x, y are nums, returns a num.
    Multiply the magnitudes with mul_mag_school and adjust the sign (product of the signs)."""
    if x[1] == [0] or y[1] == [0]:                 # a zero factor is trivial (and gives no -0)
        return (1, [0])
    return (x[0] * y[0], mul_mag_school(x[1], y[1], b))   # "you simply have to adjust the sign"

# ---- Algorithm 1.5 (Karatsuba) ----------------------------------
def karatsuba_mag(x, y, n, b):
    """Algorithm 1.5, steps 1.1 - 3.2. x and y are mags of at most n digits (leading zero digits allowed).
    Returns the mag x * y (leading zeros allowed).
    - Base case (the notes leave it out): if n <= KARATSUBA_THRESHOLD, return mul_mag_school(x, y, b).
    - If n is odd, n <- n + 1; pad x and y with zeros to exactly n digits; split at n/2.
    - The call for (x_hi + x_lo)(y_hi + y_lo) gets wordlength n/2 + 1, because the sums can carry."""
    if n <= KARATSUBA_THRESHOLD:                   # NOTE: the notes leave the base case out; small inputs
        return mul_mag_school(x, y, b)             #       are multiplied with Algorithm 1.4
    if n % 2 == 1:                                 # 1.1
        n = n + 1
    h = n // 2                                     # n/2
    x = x + [0] * (n - len(x))                     # leading zero words, so x and y have exactly n words
    y = y + [0] * (n - len(y))
    x_lo, x_hi = x[:h], x[h:]                      # 1.2  x = x_hi b^(n/2) + x_lo
    y_lo, y_hi = y[:h], y[h:]                      #      y = y_hi b^(n/2) + y_lo
    z2 = karatsuba_mag(x_hi, y_hi, h, b)           # 2.1
    z0 = karatsuba_mag(x_lo, y_lo, h, b)           # 2.2
    z1 = karatsuba_mag(add_mag(x_hi, x_lo, b),     # 2.3  NOTE: the sums can have n/2 + 1 words (carry),
                       add_mag(y_hi, y_lo, b), h + 1, b)          # so this call gets wordlength n/2 + 1
    z1 = sub_mag(z1, z0, b)                        # 2.3  ... - z0
    z1 = sub_mag(z1, z2, b)                        # 2.3  ... - z2
    z = add_mag([0] * n + z2, [0] * h + z1, b)     # 3.1  z2 b^n + z1 b^(n/2)   (shifting = prepending zeros)
    z = add_mag(z, z0, b)                          # 3.1  ... + z0
    return z                                       # 3.2

def mul_karatsuba(x, y, b):
    """Signed multiplication with Karatsuba. x, y are nums, returns a num.
    Calls karatsuba_mag with n = the larger of the two lengths, then adjusts the sign (use make_num)."""
    if x[1] == [0] or y[1] == [0]:                 # a zero factor is trivial (and gives no -0)
        return (1, [0])
    z = karatsuba_mag(x[1], y[1], max(len(x[1]), len(y[1])), b)
    while len(z) > 1 and z[-1] == 0:               # Algorithm 1.5 allows leading zero words: remove them
        z.pop()
    return (x[0] * y[0], z)

# ---- Algorithm 1.6 (Division with remainder) --------------------
def divmod_mag(x, y, b):
    """Algorithm 1.6, steps 1.1 - 3.2. x and y are mags, y != [0]. Returns (q, r), both mags without leading
    zeros, with x = q*y + r and 0 <= r < y. Find each q_i by subtracting y*b^i from r while it fits.
    Also correct for x < y (q = [0], r = x). Needed by the extended Euclidean algorithm."""
    r = x[:]                                       # 1.1  r <- x (a copy without leading zeros, so the
    while len(r) > 1 and r[-1] == 0:               #      comparisons below can look at the length first)
        r.pop()
    if (len(r), r[::-1]) < (len(y), y[::-1]):      #      x < y: q = 0 and r = x
        return [0], r
    k = len(r) - len(y) + 1                        # 1.2
    q = [0] * k
    for i in range(k - 1, -1, -1):                 # 2.1
        # 2.2 - 2.3: q_i is how often y*b^i fits in r; subtract it that often. y*b^i is y shifted i
        # places, so only the digits of r from position i upwards (r div b^i) take part.
        top = r[i:]
        while len(top) > 1 and top[-1] == 0:
            top.pop()
        while (len(top), top[::-1]) >= (len(y), y[::-1]):   # fits at most b - 1 times
            top = sub_mag(top, y, b)
            q[i] = q[i] + 1
        r = r[:i] + top                            #      r <- r - q_i*b^i*y
    while len(q) > 1 and q[-1] == 0:               # 3.1  remove leading zeros from q
        q.pop()
    return q, r                                    # 3.2

# ---- Algorithm 2.2 (Extended Euclidean Algorithm) ---------------
def ext_euclid(x, y, b):
    """Algorithm 2.2, steps 1.1 - 3.4. x and y are nums, not both zero.
    Returns (d, u, v): three nums with d = gcd(x, y) >= 0 and u*x + v*y = d.
    Follow the notes exactly (Bezout coefficients are not unique, the grader expects those of Algorithm 2.2):
    work on |x| and |y|, get q and r from divmod_mag, update the coefficients with the signed mul and sub,
    and fix the signs of u and v at the end (steps 3.2, 3.3).
    Check: ext_euclid(96, 40) -> d = 8, u = -2, v = 5."""
    x_sign,x_mag = x 
    y_sign,y_mag = y # We separate the signs and magnitudes of x and y into separate variables

    a = x_mag[:]
    c = y_mag[:] # We now make clones of the magnitudes as to not affect the real magnitudes

    u1,u2 = (1,[1]),(1,[0])
    v1,v2 = (1,[0]),(1,[1]) # We set the values of u1,u2,v1,v2.

    while c != [0]: 
        q,r = divmod_mag(a,c,b) #Obtain quotient and remainder through division
        a,c = c,r # Replace (a, c) with (c, r): the gcd stays the same

        qu2 = mul_mag_school(q,u2[1],b) # Multiply q and magnitude of u2
        while len(qu2)>1 and qu2[-1]==0: 
            qu2.pop() # Removing extra 0's from the ends
        
        qv2 = mul_mag_school(q,v2[1],b)
        while len(qv2)>1 and qv2[-1]==0:
            qv2.pop() # Removing extra 0's from the ends
        
        if qu2 ==[0]:
            qu2 = (1,qu2) 
        else:
            qu2 = (u2[0], qu2) # Here is a check to ensure if the magnitude is 0, it can not be -0. Otherwise the value will have its original sign
        
        if qv2 ==[0]:
            qv2 = (1,qv2) 
        else:
            qv2 = (v2[0], qv2) # Here is a check to ensure if the magnitude is 0, it can not be -0. Otherwise the value will have its original sign

        u3 = sub(u1,qu2,b) # Here we do the part u3 = u1 - qu2
        v3 = sub(v1,qv2,b) # Here we do the part v3 = v1 - qv2

        u1,u2 = u2,u3
        v1,v2 = v2,v3

    d = (1,a) # The gcd must be positive

    if x_sign < 0 and u1[1] != [0]:
        u = (-u1[0], u1[1])
    else:
        u = u1 # The loop worked on |x|, so if x was negative, we flip the sign of its coefficient
    
    if y_sign < 0 and v1[1] != [0]:
        v = (-v1[0], v1[1])
    else:
        v = v1 # The loop worked on |y|, so if y was negative, we flip the sign of its coefficient

    return d,u,v
    
        
    


# ===============================================================
# MODULAR ARITHMETIC   (m is a MAG with m != [0]; uses the integer arithmetic above)
# ===============================================================

# ---- Algorithm 2.5 (Modular reduction with radix b) --------------
def mod_reduce(x, m, b):
    """Algorithm 2.5, steps 1.1 - 3.2. x is a num (any sign), m is a mag != [0].
    Returns a num y with 0 <= y < m and y = x (mod m). Work on |x|: for i = k-n down to 0 subtract m*b^i
    while it fits; for a negative x with a non-zero remainder x', the result is m - x' (step 3.1).
    Also correct for m = [1] (result 0)."""
    sx, mx = x
    # 1.1 - 2.2  Work on |x|: for i = k-n down to 0, subtract m*b^i while it fits. That is exactly the
    #            loop of Algorithm 1.6 without keeping the quotient, so divmod_mag does it for us.
    _, r = divmod_mag(mx, m, b)
    if sx < 0 and r != [0]:                        # 3.1  -x' = m - x' (mod m)
        r = sub_mag(m, r, b)
    return (1, r)                                  # 3.2

# ---- Algorithm 2.7 (Modular addition) ----------------------------
def mod_add(x, y, m, b):
    """Algorithm 2.7. x and y are nums (any sign), m is a mag != [0]. Returns the num (x + y) mod m in [0, m).
    Reduce x and y first, then z' = x + y, and subtract m once if z' >= m."""
    xr = mod_reduce(x, m, b)                       #      reduce first: 0 <= x', y' < m
    yr = mod_reduce(y, m, b)
    z = add_mag(xr[1], yr[1], b)                   # 1.1  z' <- x' + y'  (lies in [0, 2m - 1))
    if (len(z), z[::-1]) >= (len(m), m[::-1]):     # 2.1  z' >= m: subtract m once
        z = sub_mag(z, m, b)
    return (1, z)                                  # 2.2

# ---- Algorithm 2.8 (Modular subtraction) -------------------------
def mod_sub(x, y, m, b):
    """Algorithm 2.8. x and y are nums (any sign), m is a mag != [0]. Returns the num (x - y) mod m in [0, m).
    Reduce x and y first, then z' = x - y, and add m once if z' < 0."""
    xr = mod_reduce(x, m, b)                       #      reduce first: 0 <= x', y' < m
    yr = mod_reduce(y, m, b)
    z = sub(xr, yr, b)                             # 1.1  z' <- x' - y'  (lies in (-m, m))
    if z[0] < 0:                                   # 2.1  z' < 0: add m once
        z = add(z, (1, m), b)
    return z                                       # 2.2

# ---- Algorithm 2.9 (Modular multiplication, naive) ----------------
def mod_mul(x, y, m, b):
    """Algorithm 2.9. x and y are nums (any sign), m is a mag != [0]. Returns the num (x * y) mod m in [0, m).
    Reduce x and y first, multiply with any multiplication method, then reduce the product."""
    xr = mod_reduce(x, m, b)                       #      reduce first: the product then has at most
    yr = mod_reduce(y, m, b)                       #      twice as many digits as m
    z = mul_mag_school(xr[1], yr[1], b)            # 1.1  z' <- x' * y'  (primary school, Algorithm 1.4)
    return mod_reduce((1, z), m, b)                # 2.1  z <- z' mod m  (Algorithm 2.5)

# ---- Algorithm 2.11 (Modular inversion) ---------------------------
def mod_inverse(x, m, b):
    """Algorithm 2.11, based on the extended Euclidean algorithm. x is a num (any sign), m is a mag != [0].
    Returns the num x^-1 mod m in [0, m), or None if x has no inverse (gcd(x, m) != 1).
    Watch out: as printed, the algorithm can return a NEGATIVE coefficient (the inverse of 3 mod 7 comes out
    as -2, the answer is 5), so add m when needed. Decide and test the edge cases: x = 0, x a multiple of m,
    and m = [1] (every x is invertible, the answer is 0)."""
    a = mod_reduce(x, m, b)[1]                     #      the notes assume 0 <= a < m, so reduce x first
    mm = m                                         # 1.1  a' <- a, m' <- m  (a and mm below)
    x1, x2 = (1, [1]), (1, [0])                    # 1.2
    # Invariant: a' = x1*a (mod m) and m' = x2*a (mod m). The loop ends with a' = gcd(a, m).
    while mm != [0]:                               # 2.1
        q, r = divmod_mag(a, mm, b)                # 2.2  q = a' div m', r = a' - q*m'
        a, mm = mm, r                              # 2.3
        qx2 = mul_mag_school(q, x2[1], b)          # 2.4  x3 <- x1 - q*x2 (q >= 0, so q*x2 has the sign of x2)
        x3 = sub(x1, (x2[0], qx2), b)
        x1, x2 = x2, x3                            # 2.5
    if a == [1]:                                   # 3.1  gcd = 1: the inverse is x1, but x1 can be negative
        return mod_reduce(x1, m, b)                #      (3 mod 7 gives -2), so bring it into [0, m)
    return None                                    # 3.2  gcd != 1: no inverse (written as null)


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
        elif op == "extended_euclidean_algorithm":
            results = {"answer": ext_euclid(x, y, b)}
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
        elif op == "inversion":  # inversion
            results = {"answer": mod_inverse(x, m, b)}   # None (no inverse) is written as null

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
    solve_exercise('Simple/Exercises/exercise7.json', 'Simple/MyAnswers/answer0.json')