import re
from dice_classes import NamedDiceCollection, DiceExpressionTerm, DiceBag, Dice

TOKEN_TAKE_HIGHEST = 'h'
TOKEN_TAKE_LOWEST = 'l'

def check_string_format(a_string):
    '''
    ok: 1d4
    ok: 2d6+4-3d8h2
    ok: 3d9l1
    !ok: 3d8h9
    !ok: 2d
    '''
    terms = re.split('[+-]', a_string)
    is_valid = next((False for t in terms if not re.match('^(\d+d\d+|\d+d\d+[hl]{1,1}\d+|\d+)$', t,re.IGNORECASE)), True)
    return is_valid

def compile_dices_re():
    pattern = '([+-]{0,1}\d+d\d+(?:[hl]{1,1}\d+){0,1})'
    return re.compile(pattern, re.IGNORECASE)

def get_dices_expressions(a_string):
    return compile_dices_re().findall(a_string)

def get_constants_expressions(a_string):
    cs = compile_dices_re().sub('', a_string)
    pattern = '([+-]*\d+)'
    compiled_expr = re.compile(pattern, re.IGNORECASE)
    return compiled_expr.findall(cs)

def calculate_constant(a_string):
    k = 0
    cs = get_constants_expressions(a_string)
    for c in cs:
        if c[0] == '-':
            k -= int(c[1:])
        else:
            k+= int(c)
    return k

def process_dice_expression(a_string):
    groups = re.findall('([+-]){0,1}(\d+)(?:d)(\d+)([hl]\d+){0,1}', a_string, flags=re.IGNORECASE)[0]
    is_negative = bool(re.match('-', groups[0]))
    ammount = groups[1]
    sides = groups[2]
    take_highest_n = None
    take_lowest_n = None
    if groups[3]:
        if re.match('h', groups[3],flags=re.IGNORECASE):
            take_highest_n = int(groups[3][1:])
        else:
            take_lowest_n = int(groups[3][1:])
    return {
            'ammount': ammount,
            'sides': sides,
            'is_negative': is_negative,
            'take_highest_n': take_highest_n,
            'take_lowest_n': take_lowest_n
    }

def get_dices_terms(a_string):
    terms = []
    for dice_expr in get_dices_expressions(a_string):
        terms.append(process_dice_expression(dice_expr))
    return terms

def build_dice_expr_terms(expression):
    dice_expression_terms = []
    for dice_term in get_dices_terms(expression):
        ammount = int(dice_term['ammount'])
        sides = int(dice_term['sides'])
        is_negative = dice_term['is_negative']
        take_highest_n = dice_term['take_highest_n']
        take_lowest_n = dice_term['take_lowest_n']
        dices = []
        for i in range(0, ammount):
            dices.append(Dice(sides))
        dice_expression_terms.append(DiceExpressionTerm(DiceBag(dices), is_negative, take_highest_n, take_lowest_n))
    return dice_expression_terms

def build_named_dice_collection(name, expression):
    constant = calculate_constant(expression)
    d_terms = build_dice_expr_terms(expression)
    return NamedDiceCollection(expression, name, constant, d_terms)
