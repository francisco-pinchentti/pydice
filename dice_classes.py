import random

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
        history = []
        result = 0
        for dice in self.dices:
            result += dice.roll()
            history.append(
                {'description':dice.description(), 'result': dice.last()}
            )
        self.history.append({ 'result' : result, 'history': history })
        return result
    
    def avg(self):
        return mean([roll['result'] for roll in self.history])

    def get_last_history(self):
        return self.history[len(self.history)-1]

class SignedDiceBag(DiceBag):

    def __init__(self, dices, is_negative):
        super(SignedDiceBag, self).__init__(dices)
        self.is_negative = is_negative

    def roll(self):
        roll = super(SignedDiceBag, self).roll()
        return -roll if self.is_negative else roll

class NamedDiceCollection:

    def __init__(self, name = '', constant = 0, dice_bags = []):
        self.history = []
        self.dice_bags = dice_bags
        self.name = name
        self.constant = constant
    
    def roll(self):
        result = self.constant
        _history_entries = []
        for dice_bag in self.dice_bags:
            result += dice_bag.roll()
            _history_entries.append(dice_bag.get_last_history())
        self.history.append({
            'result': result,
            'history': _history_entries
        })
        return result

    def avg(self):
        return mean([roll['result'] for roll in self.history])

    def get_print_string(self, expression, total_run_count, include_average = False):
        display_string = 'Results for {0} : {1}'.format(expression, self.name)
        i = 0
        for roll_history in self.history:
            i += 1
            result = roll_history['result']
            dices = [rh['history'] for rh in roll_history['history']]
            constant = self.constant
            display_string += '\n\troll number {0}\n\t\t...result was {1}\n\t\t...dices rolled {2} + {3}'.format(i, result, dices, constant)
        if include_average:
            display_string += '\n\t...the average is {0} on a total of {1} execution(s)'.format(self.avg(), total_run_count)
        return display_string
