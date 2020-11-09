def zero():
    return "zero"


def one():
    return "one"


def two():
    return "two"


switcher = {
    0: zero,
    1: one,
    2: two
}
aaaa = 'one"'
func = switcher.get(aaaa, "nothing")
print(func)