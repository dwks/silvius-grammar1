from ast import AST

class EnglishGrammarMixin(object):

    def __init__(self, *args, **kwargs):
        # register this subgrammar on the main grammar in CoreParser
        self.add_subgrammar(["english", "word_sentence", "word_phrase"])

    
    def p_english(self, args):
        '''
            english ::= word ANY
        '''
        return AST('sequence', [ args[1].extra ])

    def p_word_sentence(self, args):
        '''
            word_sentence ::= sentence word_repeat
        '''
        if(len(args[1].children) > 0):
            args[1].children[0].meta = args[1].children[0].meta.capitalize()
        return args[1]

    def p_word_phrase(self, args):
        '''
            word_phrase ::= phrase word_repeat
        '''
        return args[1]

    def p_word_repeat(self, args):
        '''
            word_repeat ::= raw_word
            word_repeat ::= raw_word word_repeat
        '''
        if(len(args) == 1):
            return AST('word_sequence', None,
                [ AST('null', args[0]) ])
        else:
            args[1].children.insert(0, AST('null', args[0]))
            return args[1]

    def p_raw_word(self, args):
        '''
            raw_word ::= ANY
            raw_word ::= zero
            raw_word ::= one
            raw_word ::= two
            raw_word ::= three
            raw_word ::= four
            raw_word ::= five
            raw_word ::= six
            raw_word ::= seven
            raw_word ::= eight
            raw_word ::= nine
            raw_word ::= to
            raw_word ::= for
        '''
        if(args[0].type == 'ANY'):
            return args[0].extra
        return args[0].type
