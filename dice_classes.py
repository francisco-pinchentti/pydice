import random

class InitializationError(ValueError):
    pass

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

class Dice:

    def __init__(self, sides):
        self.history = []
        self.sides = sides

    def roll(self):
        result = random.randint(1, self.sides)
        self.history.append(result)
        return result

    def description(self):
        return 'd'+str(self.sides)

    def avg(self):
        return mean(self.history)

    def last(self):
        return self.history[len(self.history)-1]

class DiceBag(object):

    def __init__(self, dices):
        self.history = []
        self.dices = dices

    def roll(self):
        _history = []
        result = 0
        for dice in self.dices:
            result += dice.roll()
            _history.append(
                {'description':dice.description(), 'result': dice.last()}
            )
        # @todo refactor history as "faces" or "rolls" or ...
        self.history.append({ 'result' : result, 'history': _history })
        return result

    def avg(self):
        return mean([roll['result'] for roll in self.history])

    def get_last_history(self):
        return self.history[len(self.history)-1]

    def get_last_highest(self, n):
        '''
        Returns a tuple (x,y) containg:
        the highest n results from the last history entry x
        and the remaining ones in y
        '''
        return self.__take_n_history_entries(n, take_highest = True)

    def get_last_lowest(self, n):
        '''
        Returns a tuple (x,y) containg:
        the lowest n results from last history entry in x
        and the remaining ones in y
        '''
        return self.__take_n_history_entries(n, take_highest = False)
    
    def __take_n_history_entries(self, n, take_highest):
        last_history = self.get_last_history()['history']
        sorted_history_entries = sorted(last_history, key=lambda h : h['result'], reverse=take_highest)
        return (
            sorted_history_entries[0:n],
            sorted_history_entries[n:]
        )

class DiceExpressionTerm(object):
    '''
    This class represents a dice set -or bag- and associated modifiers
    like negative term, keep n highest rolls or drop n lower rolls
    '''
    def __init__(self, dice_bag, is_negative, take_highest_n=None, take_lowest_n=None):
        if len(dice_bag.dices) < take_highest_n or len(dice_bag.dices) < take_lowest_n:
            raise InitializationError('Attempting to keep more dices than those found on bag')
        self.dice_bag = dice_bag
        self.is_negative = is_negative
        self.take_highest_n = take_highest_n
        self.take_lowest_n = take_lowest_n
        self.history = []

    def roll(self):
        self.dice_bag.roll()
        _kept = []
        _dropped = []
        if self.take_highest_n:
            (_kept, _dropped) = self.dice_bag.get_last_highest(self.take_highest_n)
        elif self.take_lowest_n:
            (_kept, _dropped) = self.dice_bag.get_last_lowest(self.take_lowest_n)
        else:
            _kept = self.dice_bag.get_last_history()['history']
        unsigned_roll_result = sum([h['result'] for h in _kept])
        signed_roll_result = -unsigned_roll_result if self.is_negative else unsigned_roll_result
        self.history.append({
            'result': signed_roll_result,
            'kept': _kept,
            'dropped': _dropped
        })
        return signed_roll_result
    
    def get_last_history(self):
        return self.history[len(self.history)-1]

class NamedDiceCollection:
    '''
    This class holds a collection of dice expression terms and
    other associated attributes -like name or constant modifiers-
    '''
    def __init__(self, expression = '', name = '', constant = 0, dice_terms_exprs = []):
        self.history = []
        self.dice_terms_exprs = dice_terms_exprs
        self.__name = name
        self.constant = constant
        self.__original_expression = expression

    def roll(self):
        result = self.constant
        _history_entries = []
        for det in self.dice_terms_exprs:
            result += det.roll()
            _history_entries.append(det.get_last_history())
        self.history.append({
            'result': result,
            'history': _history_entries
        })
        return result

    def avg(self):
        return mean([roll['result'] for roll in self.history])

    def get_print_string(self, total_run_count, include_average = False):
        display_string = 'Results for {0} : {1}'.format(self.__original_expression, self.__name)
        i = 0
        for roll_history in self.history:
            i += 1
            result = roll_history['result']
            # parsing DiceExpressionTerm history:
            kept = [det['kept'] for det in roll_history['history']]
            dropped = [det['dropped'] for det in roll_history['history']]
            kept_sum = sum( [ sum([roll['result'] for roll in k]) for k in kept ] )
            display_string += '\n\troll number {0}\n\t\t...total result is {1}'.format(i, result)
            # @todo split kept array on positive and negatives
            display_string += '\n\t\t\t...counting {0} from dices'.format(kept_sum)
            display_string += '\n\t\t\t...and {0} from constants'.format(self.constant)
            display_string += '\n\t\t...dices kept {0}'.format(kept)
            display_string += '\n\t\t...dices dropped {0}'.format(dropped)
        if include_average:
            display_string += '\n\t...the average is {0} on a total of {1} execution(s)'.format(self.avg(), total_run_count)
        return display_string
