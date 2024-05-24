# -*- coding:utf8 -*-
import re


def translate(pattern):
    i, n = 0, len(pattern)
    res = ''
    while i < n:
        c = pattern[i]
        i = i + 1
        if c == '*':
            res = res + '.*'
        elif c == '?':
            res = res + '.'
        elif c == '[':
            j = i
            if j < n and pattern[j] == '!':
                j = j + 1
            if j < n and pattern[j] == ']':
                j = j + 1
            while j < n and pattern[j] != ']':
                j = j + 1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pattern[i:j].replace('\\', '\\\\')
                i = j + 1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)
        else:
            res = res + re.escape(c)
    return res + '\Z(?ms)'


def pattern_match(pattern, name):
    split_list = pattern.split(",")
    pattern_list = []
    for item in split_list:
        item = item.strip()
        if item:
            pattern_list.append("*{}*".format(item))

    if not name:
        pattern_list.append("*")

    name = re.sub(r"^pid_[\d]{4}_[\d]{4}", "", name)
    return _pattern_match(pattern_list, name)


def _pattern_match(patterns, name):
    for pattern in patterns:
        res = translate(pattern)
        re_pat = re.compile(res, re.IGNORECASE)
        if re_pat.match(name) is not None:
            return True
    return False
