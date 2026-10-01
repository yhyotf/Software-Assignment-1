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
# Oskar Rabenda (2332159)
##

# Import built-in json library for handling input/output 
import json
DIGITS = "0123456789ABCDEF"
KARATSUBA_THRESHOLD = 5 

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

def mul_mag_school(x, y, b):
    """Multiply two mags with the primary school method (Algorithm 1.4, steps 1.1 - 3.2).

    Args:
        x, y: mags of the two factors (digit lists, least significant digit first). Leading zeros are allowed.
        b: the radix, 2 <= b <= 16.

    Returns:
        The mag x * y. Leading zeros remain if the inputs had them or a factor is 0 ([0] * [3, 2] gives
        [0, 0]); callers that compare by length must remove them.

    Raises:
        Nothing; the inputs are not checked (they must be non-empty lists of digits 0 .. b-1).
    """
    m, n = len(x), len(y)
    z = [0] * (m + n)
    for i in range(m):
        c = 0
        for j in range(n):
            t = z[i + j] + x[i] * y[j] + c
            c = t // b
            z[i + j] = t - c * b
        z[i + n] = c
    if z[m + n - 1] == 0:
        k = m + n - 1
    else:
        k = m + n
    return z[:k]

def mul_school(x, y, b):
    """Signed multiplication with the primary school method. x, y are nums, returns a num.
    Multiply the magnitudes with mul_mag_school and adjust the sign (product of the signs)."""
    if x[1] == [0] or y[1] == [0]:                 # a zero factor is trivial (and gives no -0)
        return (1, [0])
    return (x[0] * y[0], mul_mag_school(x[1], y[1], b))   # "you simply have to adjust the sign"

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

def divmod_mag(x, y, b):
    """Divide two mags with remainder (Algorithm 1.6, steps 1.1 - 3.2).

    Args:
        x: mag of the dividend. Leading zeros are allowed (mul_mag_school can leave them).
        y: mag of the divisor. Must not be [0] and must not have leading zeros.
        b: the radix, 2 <= b <= 16.

    Returns:
        (q, r): mags without leading zeros with x = q*y + r and 0 <= r < y. If x < y, this is ([0], x).

    Raises:
        Nothing; the inputs are not checked. y = [0] makes the loop run forever, and a y with leading zeros
        gives wrong results, because the comparisons look at the length first.

    Note:
        Each quotient digit q_i is found by subtracting y*b^i from r while it fits, at most b - 1 times.
        x itself is not changed; r starts as a copy.
    """
    r = x[:]
    while len(r) > 1 and r[-1] == 0:
        r.pop()
    if (len(r), r[::-1]) < (len(y), y[::-1]):
        return [0], r
    k = len(r) - len(y) + 1
    q = [0] * k
    for i in range(k - 1, -1, -1):
        # q_i is how often y*b^i fits in r. y*b^i is y shifted i places
        top = r[i:]
        while len(top) > 1 and top[-1] == 0:
            top.pop()
        while (len(top), top[::-1]) >= (len(y), y[::-1]):
            top = sub_mag(top, y, b)
            q[i] = q[i] + 1
        r = r[:i] + top
    while len(q) > 1 and q[-1] == 0: # remove leading zeros from q
        q.pop()
    return q, r

def ext_euclid(x, y, b):
    """Compute the gcd(x,y) and provide Bezout coefficients (u and v) (Algorithm 2.2, steps 1.1 - 3.4).
    Args:
        x: num (sign, mag) of any sign. Mag without leading zeros
        y: num (sign, mag) of any sign. Mag without leading zeros
            x and y are not both zero.
        b: the radix, 2 <= b <= 16.
    
    Returns:
        (d, u, v): three nums without leading zeros, with d = gcd(x, y) >= 0
        and u*x + v*y = d.
    
    Raises:
        Nothing. The inputs are not checked. If x and y are both zero (excluded by spec), the loop is skipped and (0,1,0) is returned.

    Note:
        The loop runs on |x| and |y|. At the end, the sign of u is flipped if x was negative, and the sign of v if y was negative (zero is never flipped,
        so -0 cannot occur).
    """
    x_sign,x_mag = x 
    y_sign,y_mag = y

    # To not affect the real magnitudes
    a = x_mag[:]
    c = y_mag[:]

    u1,u2 = (1,[1]),(1,[0])
    v1,v2 = (1,[0]),(1,[1])

    while c != [0]: 
        q,r = divmod_mag(a,c,b)
        a,c = c,r

        qu2 = mul_mag_school(q,u2[1],b)
        while len(qu2)>1 and qu2[-1]==0: 
            qu2.pop() # Removing extra zeros from the ends
        
        qv2 = mul_mag_school(q,v2[1],b)
        while len(qv2)>1 and qv2[-1]==0:
            qv2.pop() # Removing extra zeros from the ends
        
        if qu2 ==[0]:
            qu2 = (1,qu2) 
        else:
            qu2 = (u2[0], qu2) # Here is a check to ensure if the magnitude is 0, it can not be -0
        
        if qv2 ==[0]:
            qv2 = (1,qv2) 
        else:
            qv2 = (v2[0], qv2) # Here is a check to ensure if the magnitude is 0, it can not be -0

        u3 = sub(u1,qu2,b)
        v3 = sub(v1,qv2,b)

        u1,u2 = u2,u3
        v1,v2 = v2,v3

    d = (1,a) # The gcd must be positive

    if x_sign < 0 and u1[1] != [0]:
        u = (-u1[0], u1[1])
    else:
        u = u1
    
    if y_sign < 0 and v1[1] != [0]:
        v = (-v1[0], v1[1])
    else:
        v = v1

    return d,u,v


def mod_reduce(x, m, b):
    """Reduce x modulo m (Algorithm 2.5, steps 1.1 - 3.2).

    Args:
        x: num (sign, mag) of any sign. The mag may have leading zeros.
        m: mag of the modulus. Must not be [0].
        b: the radix, 2 <= b <= 16.

    Returns:
        The num (1, r) with 0 <= r < m and r = x (mod m), without leading zeros. For a negative x with
        |x| mod m = x' != 0 the result is m - x' (step 3.1). For m = [1] the result is always (1, [0]).

    Raises:
        Nothing; the inputs are not checked. m = [0] makes it loop forever, which is why solve_exercise
        answers null for a zero modulus before calling any modular function.

    Note:
        Steps 2.1 - 2.2 (subtract m*b^i while it fits) are the loop of Algorithm 1.6 without the quotient,
        so divmod_mag does them.
    """
    sx, mx = x
    _, r = divmod_mag(mx, m, b)
    if sx < 0 and r != [0]:
        r = sub_mag(m, r, b)
    return (1, r)

def mod_add(x, y, m, b):
    """Algorithm 2.7. x and y are nums (any sign), m is a mag != [0]. Returns the num (x + y) mod m in [0, m).
    Reduce x and y first, then z' = x + y, and subtract m once if z' >= m."""
    xr = mod_reduce(x, m, b)                       #      reduce first: 0 <= x', y' < m
    yr = mod_reduce(y, m, b)
    z = add_mag(xr[1], yr[1], b)                   # 1.1  z' <- x' + y'  (lies in [0, 2m - 1))
    if (len(z), z[::-1]) >= (len(m), m[::-1]):     # 2.1  z' >= m: subtract m once
        z = sub_mag(z, m, b)
    return (1, z)                                  # 2.2

def mod_sub(x, y, m, b):
    """Compute (x - y) mod m (Algorithm 2.8).

    Args:
        x, y: nums (sign, mag) of any sign.
        m: mag of the modulus. Must not be [0].
        b: the radix, 2 <= b <= 16.

    Returns:
        The num (1, z) with 0 <= z < m and z = x - y (mod m).

    Raises:
        Nothing; the inputs are not checked. m = [0] makes it loop forever (solve_exercise answers null instead).

    Note:
        Algorithm 2.8 assumes 0 <= x, y < m, but the assignment allows any integer, so x and y are reduced
        first. Then z' = x' - y' lies in (-m, m), and adding m once when z' < 0 is enough.
    """
    xr = mod_reduce(x, m, b)
    yr = mod_reduce(y, m, b)
    z = sub(xr, yr, b)
    if z[0] < 0:
        z = add(z, (1, m), b)
    return z

def mod_mul(x, y, m, b):
    """Compute (x * y) mod m (Algorithm 2.9).

    Args:
        x, y: nums (sign, mag) of any sign.
        m: mag of the modulus. Must not be [0].
        b: the radix, 2 <= b <= 16.

    Returns:
        The num (1, z) with 0 <= z < m and z = x * y (mod m).

    Raises:
        Nothing; the inputs are not checked. m = [0] makes it loop forever (solve_exercise answers null instead).

    Note:
        x and y are reduced first, so the product has at most twice as many digits as m. The assignment
        allows any multiplication method; this uses the primary school method (mul_mag_school).
    """
    xr = mod_reduce(x, m, b)
    yr = mod_reduce(y, m, b)
    z = mul_mag_school(xr[1], yr[1], b)
    return mod_reduce((1, z), m, b)

def mod_inverse(x, m, b):
    """Compute the inverse of x modulo m (Algorithm 2.11, the extended Euclidean algorithm for one coefficient).

    Args:
        x: num (sign, mag) of any sign.
        m: mag of the modulus. Must not be [0].
        b: the radix, 2 <= b <= 16.

    Returns:
        The num (1, z) with 0 <= z < m and x*z = 1 (mod m), or None if gcd(x, m) != 1 (no inverse exists;
        solve_exercise writes it as null). For m >= 2, x = 0 or a multiple of m gives None.
        For m = [1] the result is (1, [0]), since every integer is 0 mod 1.

    Raises:
        Nothing; the inputs are not checked. m = [0] makes it loop forever (solve_exercise answers null instead).

    Note:
        x is reduced first, because Algorithm 2.11 expects 0 <= a < m. As printed, the algorithm can end with a
        negative coefficient (3 mod 7 gives -2, the answer is 5), so the result is reduced once more.
    """
    a = mod_reduce(x, m, b)[1]
    mm = m
    x1, x2 = (1, [1]), (1, [0])
    while mm != [0]:
        q, r = divmod_mag(a, mm, b)
        a, mm = mm, r
        qx2 = mul_mag_school(q, x2[1], b)
        x3 = sub(x1, (x2[0], qx2), b)
        x1, x2 = x2, x3
    if a == [1]:
        return mod_reduce(x1, m, b)
    return None


def solve_exercise(exercise_location: str, answer_location: str):
    with open(exercise_location, "r") as exercise_file:
        exercise = json.load(exercise_file)

    b = exercise["radix"]
    op = exercise["operation"]

    # Strings -> nums. The digits already are radix b digits, so we only map them to numbers and
    # reverse them (least significant first). Done once for every operand the exercise has
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
            d, u, v = ext_euclid(x, y, b)
            results = {"answer-a": u, "answer-b": v, "answer-gcd": d}
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
    solve_exercise('Simple/Exercises/exercise0.json', 'Simple/MyAnswers/answer0.json')