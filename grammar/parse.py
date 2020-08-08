# Parser, based on John Aycock's SPARK examples

from spark import GenericParser
from spark import GenericASTBuilder
from ast import AST

# subgrammars are loaded from the grammars/ subpackage
from grammars import numbers
from grammars import english
from grammars import yesno

class GrammaticalError(Exception):
    def __init__(self, string):
        self.string = string
    def __str__(self):
        return self.string

# include the subgrammars as mixin classes. This makes all the rule
# functions accessible in the CoreParser (and the actual parser in
# GenericParser), and allows the subgrammar classes to call
# 'add_subgrammar' from their __init__ methods.
class CoreParser(GenericParser,
                 numbers.NumberGrammarMixin,
                 english.EnglishGrammarMixin,
                 yesno.YesNoGrammarMixin):

    def __init__(self, start):
        # call __init__ on all mixin classes
        # skip GenericParser, we'll call that as the last one
        for base in CoreParser.__bases__:
            if base.__name__ is not "GenericParser":
                base.__init__(self, start)
        # now set up the actual parser
        GenericParser.__init__(self, start)

    # this method will be called by any subgrammars that want
    # to hook themselves into the main grammar.
    # this adds one or more rules to the 'single_command' ruleset.
    def add_subgrammar(self, subgrammar_start_rule_names):
        func = CoreParser.__dict__['p_single_command']
        for start_rule_name in subgrammar_start_rule_names:
            func.__doc__ += ("single_command ::= " + start_rule_name + "\n")


    def typestring(self, token):
        return token.type

    def error(self, token):
        raise GrammaticalError(
            "Unexpected token `%s' (word number %d)" % (token, token.wordno))

    def p_chained_commands(self, args):
        '''
            chained_commands ::= single_command
            chained_commands ::= single_command chained_commands
        '''
        if(len(args) == 1):
            return AST('chain', None, [ args[0] ])
        else:
            args[1].children.insert(0, args[0])
            return args[1]

    def p_single_command(self, args):
        '''
            single_command ::= letter
            single_command ::= sky_letter
            single_command ::= movement
            single_command ::= character
            single_command ::= editing
            single_command ::= modifiers
        '''
        return args[0]

    def p_movement(self, args):
        '''
            movement ::= up     repeat
            movement ::= down   repeat
            movement ::= left   repeat
            movement ::= right  repeat
        '''
        if args[1] != None:
            return AST('repeat', [ args[1] ], [
                AST('movement', [ args[0] ])
            ])
        else:
            return AST('movement', [ args[0] ])

    def p_repeat(self, args):
        '''
            repeat ::=
            repeat ::= number_set
        '''
        if len(args) > 0:
            return args[0]
        else:
            return None


    def p_sky_letter(self, args):
        '''
            sky_letter ::= sky letter
        '''
        ast = args[1]
        ast.meta[0] = ast.meta[0].upper()
        return ast

    def p_letter(self, args):
        '''
            letter ::= arch
            letter ::= bravo
            letter ::= charlie
            letter ::= delta
            letter ::= eco
            letter ::= echo
            letter ::= fox
            letter ::= golf
            letter ::= hotel
            letter ::= india
            letter ::= julia
            letter ::= kilo
            letter ::= line
            letter ::= mike
            letter ::= november
            letter ::= oscar
            letter ::= papa
            letter ::= queen
            letter ::= romeo
            letter ::= sierra
            letter ::= tango
            letter ::= uniform
            letter ::= victor
            letter ::= whiskey
            letter ::= whisky
            letter ::= xray
            letter ::= expert
            letter ::= yankee
            letter ::= zulu
        '''
        if(args[0].type == 'expert'): args[0].type = 'x'
        return AST('char', [ args[0].type[0] ])

    def p_character(self, args):
        '''
            character ::= act
            character ::= colon
            character ::= semicolon
            character ::= single quote
            character ::= double quote
            character ::= equal
            character ::= space
            character ::= tab
            character ::= bang
            character ::= hash
            character ::= dollar
            character ::= percent
            character ::= carrot
            character ::= ampersand
            character ::= star
            character ::= late
            character ::= rate
            character ::= minus
            character ::= dash
            character ::= underscore
            character ::= plus
            character ::= backslash
            character ::= dot
            character ::= dit
            character ::= slash
            character ::= question
            character ::= comma
        '''
        value = {
            'act'   : 'Escape',
            'colon' : 'colon',
            'semicolon' : 'semicolon',
            'single': 'apostrophe',
            'double': 'quotedbl',
            'equal' : 'equal',
            'space' : 'space',
            'tab'   : 'Tab',
            'bang'  : 'exclam',
            'hash'  : 'numbersign',
            'dollar': 'dollar',
            'percent': 'percent',
            'carrot': 'caret',
            'ampersand': 'ampersand',
            'star': 'asterisk',
            'late': 'parenleft',
            'rate': 'parenright',
            'minus': 'minus',
            'dash': 'minus',
            'underscore': 'underscore',
            'plus': 'plus',
            'backslash': 'backslash',
            'dot': 'period',
            'dit': 'period',
            'slash': 'slash',
            'question': 'question',
            'comma': 'comma'
        }
        return AST('raw_char', [ value[args[0].type] ])

    def p_editing(self, args):
        '''
            editing ::= slap        repeat
            editing ::= scratch     repeat
        '''
        value = {
            'slap'  : 'Return',
            'scratch': 'BackSpace'
        }
        if args[1] != None:
            return AST('repeat', [ args[1] ], [
                AST('raw_char', [ value[args[0].type] ])
            ])
        else:
            return AST('raw_char', [ value[args[0].type] ])

    def p_modifiers(self, args):
        '''
            modifiers ::= control single_command
            modifiers ::= alt single_command
            modifiers ::= alternative single_command
            modifiers ::= super single_command
            modifiers ::= shift single_command
        '''
        value = {
            'control' : 'ctrl',
            'alt' : 'alt',
            'alternative' : 'alt',
            'super' : 'Super_L',
            'shift' : 'Shift_L'
        }
        if(args[1].type == 'mod_plus_key'):
            args[1].meta.insert(0, value[args[0].type])
            return args[1]
        else:
            return AST('mod_plus_key', [ value[args[0].type] ], [ args[1] ] )


class SingleInputParser(CoreParser):
    def __init__(self):
        # if you have the issue that commands fail because spurious
        # tokens ('i', 'the',...) are prepended to the acual command,
        # try commenting the 'single_input' line, and uncommenting
        # the 'single_input_discard_junk' line.
        CoreParser.__init__(self, 'single_input')
        #CoreParser.__init__(self, 'single_input_discard_junk')
        self.sleeping = False

    def p_sleep_commands(self, args):
        '''
            sleep_commands ::= go to sleep
            sleep_commands ::= start listening
        '''
        if args[-1].type == 'sleep':
            self.sleeping = True
            print 'Going to sleep.'
        else:
            self.sleeping = False
            print 'Waking from sleep'
        return AST('')

    def p_single_input(self, args):
        '''
            single_input ::= END
            single_input ::= sleep_commands END
            single_input ::= chained_commands END
        '''
        if len(args) > 0 and not self.sleeping:
            return args[0]
        else:
            return AST('')

    def p_single_input_discard_junk(self, args):
        '''
            single_input_discard_junk ::= END
            single_input_discard_junk ::= junk_tokens sleep_commands END
            single_input_discard_junk ::= junk_tokens chained_commands END
        '''
        if len(args) > 1 and not self.sleeping:
            return args[1]
        else:
            return AST('')

    # With some models, Kaldi may return spurious tokens in response
    # to noise. If that happens just before we say a command, it will
    # make the command fail. This "dummy" rule will swallows these tokens.
    def p_junk_tokens(self, args):
        '''
            junk_tokens ::=
            junk_tokens ::= i junk_tokens
            junk_tokens ::= the junk_tokens
            junk_tokens ::= a junk_tokens
            junk_tokens ::= and junk_tokens
        '''
        return AST('')


def parse(parser, tokens):
    return parser.parse(tokens)
