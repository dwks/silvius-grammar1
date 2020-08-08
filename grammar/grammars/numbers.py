from ast import AST


class NumberGrammarMixin(object):

    def __init__(self, *args, **kwargs):
        # register this subgrammar on the main grammar in CoreParser
        # "number_rule" is the name of the 'top-level' rule in this
        # subgrammar (see method 'p_rule_number'
        self.add_subgrammar(["number_rule"])
        
    small_numbers = {
        'zero'      : 0,
        'one'       : 1,
        'two'       : 2,
        'three'     : 3,
        'four'      : 4,
        'five'      : 5,
        'six'       : 6,
        'seven'     : 7,
        'eight'     : 8,
        'nine'      : 9,
        'ten'       : 10,
        'eleven'    : 11,
        'twelve'    : 12,
        'thirteen'  : 13,
        'fourteen'  : 14,
        'fifteen'   : 15,
        'sixteen'   : 16,
        'seventeen' : 17,
        'eighteen'  : 18,
        'nineteen'  : 19,

        # sadly, kaldi often recognizes these by accident
        'to'        : 2,
        'for'       : 4,
    }
    def p_number_rule(self, args):
        '''
            number_rule ::= number number_set
            number_rule ::= number thousand_number_set
            number_rule ::= number million_number_set
            number_rule ::= number billion_number_set
        '''
        return AST('sequence', [ str(args[1]) ])
    def p_number_set(self, args):
        '''
            number_set ::= _firstnumbers
            number_set ::= _tens
            number_set ::= _tens _ones
            number_set ::= _hundreds
            number_set ::= _hundreds _firstnumbers
            number_set ::= _hundreds _tens
            number_set ::= _hundreds _tens _ones
        '''
        return sum(args)
    def p__ones(self, args):
        '''
            _ones ::= one
            _ones ::= two
            _ones ::= three
            _ones ::= four
            _ones ::= five
            _ones ::= six
            _ones ::= seven
            _ones ::= eight
            _ones ::= nine
            _ones ::= to
            _ones ::= for
        '''
        return self.small_numbers[args[0].type]
    def p__firstnumbers(self, args):
        '''
            _firstnumbers ::= zero
            _firstnumbers ::= one
            _firstnumbers ::= two
            _firstnumbers ::= three
            _firstnumbers ::= four
            _firstnumbers ::= five
            _firstnumbers ::= six
            _firstnumbers ::= seven
            _firstnumbers ::= eight
            _firstnumbers ::= nine
            _firstnumbers ::= ten
            _firstnumbers ::= eleven
            _firstnumbers ::= twelve
            _firstnumbers ::= thirteen
            _firstnumbers ::= fourteen
            _firstnumbers ::= fifteen
            _firstnumbers ::= sixteen
            _firstnumbers ::= seventeen
            _firstnumbers ::= eighteen
            _firstnumbers ::= nineteen
            _firstnumbers ::= to
            _firstnumbers ::= for
        '''
        return self.small_numbers[args[0].type]
    def p__tens(self, args):
        '''
            _tens ::= twenty
            _tens ::= thirty
            _tens ::= forty
            _tens ::= fifty
            _tens ::= sixty
            _tens ::= seventy
            _tens ::= eighty
            _tens ::= ninety
        '''
        value = {
            'twenty'   : 20,
            'thirty'   : 30,
            'forty'    : 40,
            'fifty'    : 50,
            'sixty'    : 60,
            'seventy'  : 70,
            'eighty'   : 80,
            'ninety'   : 90
        }
        return value[args[0].type]
    def p__hundreds(self, args):
        '''
            _hundreds ::= _ones hundred
        '''
        return args[0] * 100
    def p_thousand_number_set(self, args):
        '''
            thousand_number_set ::= number_set thousand
            thousand_number_set ::= number_set thousand number_set
        '''
        total = args[0] * 1000
        if len(args) > 2: total += args[2]
        return total
    def p_million_number_set(self, args):
        '''
            million_number_set ::= number_set million
            million_number_set ::= number_set million number_set
            million_number_set ::= number_set million thousand_number_set
        '''
        total = args[0] * 1000000
        if len(args) > 2: total += args[2]
        return total
    def p_billion_number_set(self, args):
        '''
            billion_number_set ::= number_set billion
            billion_number_set ::= number_set billion number_set
            billion_number_set ::= number_set billion thousand_number_set
            billion_number_set ::= number_set billion million_number_set
        '''
        total = args[0] * 1000000000
        if len(args) > 2: total += args[2]
        return total
