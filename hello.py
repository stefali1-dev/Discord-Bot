
def stringToHex(s):
    new_s = ""
    for ch in s:
        hex_char = hex(ord(ch))[2:]
        new_s += "%" + hex_char.upper()

    return new_s

