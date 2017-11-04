import re
from dice_classes import NamedDiceCollection, DiceExprTerm, DiceBag, Dice

def check_string_format(a_string):
    terms = re.split('[+-]', a_string)
    is_valid = next((False for t in terms if not re.match('^(\d+d\d+|\d+)$', t)), True)
    return is_valid

def compile_dices_re():
    pattern = '([+-]{0,1}\d+d\d+)'
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

def get_dices_terms(a_string):
    terms = []
    for dice_expressions in get_dices_expressions(a_string):
        is_negative = dice_expressions[0] == '-'
        usigned_dice_expression = re.sub('[+-]','', dice_expressions)
        (ammount,sides) = re.split('d',usigned_dice_expression,0,re.IGNORECASE)
        terms.append( {
            'ammount': ammount,
            'sides': sides,
            'is_negative': is_negative
        })
    return terms

def build_dice_expr_terms(expression):
    l = []
    for dice_term in get_dices_terms(expression):
        ammount = int(dice_term['ammount'])
        sides = int(dice_term['sides'])
        is_negative = dice_term['is_negative']
        #keep_highest_n = dice_term['keep_highest_n']
        #drop_lowest_n = dice_term['drop_lowest_n']
        dices = []
        for i in range(0, ammount):
            dices.append(Dice(sides))
        l.append(DiceExprTerm(DiceBag(dices), is_negative))
    return l

def build_named_dice_collection(name, expression):
    constant = calculate_constant(expression)
    # signed_dice_bags = build_signed_dice_bags(expression)
    d_terms = build_dice_expr_terms(expression)
    return NamedDiceCollection(name, constant, d_terms)
