# coding=utf-8
import re

import jieba.posseg as pseg
from id_validator import validator

IDCARD_PATTERN = re.compile(r"[\dXx*]{18}")
PHONE_PATTERN = re.compile(r"1[\d*]{10}")
SKILLCERT_PATTERN = re.compile(r"[\d*]+")
BANDCARD_PATTERN = re.compile(r"[\d*]{16,19}")


def is_human_name(word_string):
    """
    判断是否人名
    :param word_string:
    :return:
    """
    pair_word_list = pseg.lcut(word_string)
    for eve_word, cixing in pair_word_list:
        if cixing == "nr":
            return True
    return False


def is_bank_card(card):
    if not BANDCARD_PATTERN.match(card):
        return False
    if '*' in card:
        return True
    try:
        digits = [int(x) for x in reversed(card)]
        check_sum = sum(digits[::2]) + sum((dig // 10 + dig % 10) for dig in [2 * el for el in digits[1::2]])
        return check_sum % 10 == 0
    except:
        return False


def is_id_card(card):
    if not IDCARD_PATTERN.match(card):
        return False
    if '*' in card:
        return True
    return validator.is_valid(card)


def is_phone(number):
    if not PHONE_PATTERN.match(number):
        return False
    else:
        return True


def is_skill_cert(number):
    if not SKILLCERT_PATTERN.match(number):
        return False
    else:
        return True


def is_pii(info, itype='name'):
    if itype == 'name':
        return is_human_name(info)
    elif itype == 'mobile':
        return is_phone(info)
    elif itype == 'idcard':
        return is_id_card(info)
    elif itype == 'bank_card':
        return is_bank_card(info)
    elif itype == 'skill_cert':
        return is_skill_cert(info)
    else:
        return None
