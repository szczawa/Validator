import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

class Scanner:
    def __init__(self, input_string):
        self.tokens = []
        self.current_token_number = 0
        self.indent_levels = [0]  
        for token in self.tokenize(input_string):
            self.tokens.append(token)

    def tokenize(self, input_string):
        token_specification = [
            ('NEWLINE', r'\n[\t ]*'),                            
            ('IMPORTANT', r'!important'),
            ('URL', r'url\([^)]+\)'),                                                     
            ('COLON', r' *: *'),                                                                                
            ('ADD', r' *\+ *'),              
            ('CHILD', r' *> *'),                  
            ('COMA', r' *, *'),
            ('HASH', r'#'),                                      
            ('SEMICOLON', r' *; *'),
            ('UNDERSCORE', r'_'),
            ('STRING', r'\"[^"]*\"'),                                     
            ('COMMENT', r'\/\/[^\n]*'),
            ('IDENTIFIER', r'[A-Za-z0-9%-]+ *'),
            ('SPECIAL_IDENTIFIER', r'\* *'),
            ('DOT', r'\.')                           
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        numberofline = 1
        current_position = 0 
        start_line = 0
        match = get_token(input_string)
        indentationlvl = 1
        while match is not None:
            token_type = match.lastgroup
            if token_type == 'NEWLINE':
                numberofline += 1
                value = len(match.group(token_type))
                if value not in (1,2):
                    raise RuntimeError('Bad Indent')
                elif value > indentationlvl:
                  yield Token("INDENT", '', numberofline, match.start() - start_line)
                elif value < indentationlvl:
                  yield Token("DEDENT", '', numberofline, match.start() - start_line)  
                indentationlvl =  value
                start_line = current_position
            elif token_type == 'COMMENT':
                pass
            else:
                value = match.group(token_type)
                yield Token(token_type, value, numberofline, match.start() - start_line)
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            print(self.tokens)
            raise RuntimeError('Error: Unexpected character %r on line %d' %
                               (input_string[current_position], numberofline))
        yield Token('EOF', '', numberofline, current_position - start_line)

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number - 1 < len(self.tokens):
            return self.tokens[self.current_token_number - 1]
        else:
            raise RuntimeError('Error: No more tokens')
    


