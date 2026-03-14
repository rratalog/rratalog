from math import floor, log10


def round_(x, n):
    """Round a float, x, to n significant figures."""
    n = int(n)
    x = float(x)

    if x == 0:
        return 0

    e = floor(log10(abs(x)) - n + 1)
    shifted_dp = x / (10**e)
    return round(shifted_dp) * (10**e)


def string(x, n):
    """Convert a float, x, to a string with n significant figures."""
    n = int(n)
    x = float(x)

    if n < 1:
        raise ValueError("1+ significant digits required.")

    s, e = "".join(("{:.", str(n - 1), "e}")).format(x).split("e")
    e = int(e)

    if e == 0:
        return s

    s = s.replace(".", "")
    if e < 0:
        return "".join(("0.", "0" * (abs(e) - 1), s))
    else:
        s += "0" * (e - n + 1)
        i = e + 1
        sep = ""
        if i < n:
            sep = "."
        if s[0] == "-":
            i += 1
        return sep.join((s[:i], s[i:]))
