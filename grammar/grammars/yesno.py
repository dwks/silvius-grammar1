from ast import AST

class YesNoGrammarMixin(object):

    def __init__(self, *args, **kwargs):
        # register this subgrammar on the main grammar in CoreParser
        self.add_subgrammar(["yesno"])


    def p_yesno(self, args):
        '''
            yesno ::= yes
            yesno ::= no
        '''
        return AST('sequence', [ args[0].type ])

