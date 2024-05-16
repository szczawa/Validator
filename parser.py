class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None

    def parse(self):
        self.current_token = self.scanner.next_token()
        return self.start()

    def error(self, message):
        raise RuntimeError(f'Error at line {self.current_token.line}, column {self.current_token.column}: {message}')

    def start(self):
        blocks = self.blocks()
        if self.current_token.type != 'EOF':
            self.error(f'Unexpected token {self.current_token.value}')
        return blocks

    def blocks(self):
        blocks = []
        while self.current_token.type != 'EOF':
            block = self.block()
            blocks.append(block)
        return blocks

    def block(self):
        selectors = self.selectors()
        if self.current_token.type != 'INDENT':
            self.error('Expected INDENT')
        self.match('INDENT')
        assignments = self.assignments()
        if self.current_token.type != 'DEDENT':
            self.error('Expected DEDENT')
        self.match('DEDENT')
        return (selectors, assignments)

    def selectors(self):
        selectors = [self.selector()]
        while self.current_token.type in ['ADD', 'CHILD', 'COMA', 'COLON', 'IDENTIFIER', 'HASH', 'DOT', 'COLON', 'UNDERSCORE']:
            symbol = None
            if self.current_token.type in ['ADD', 'CHILD', 'COMA', 'COLON']:
                symbol = self.match(self.current_token.type)
            elif self.current_token.type == 'IDENTIFIER':
                symbol = None
            selectors.append((symbol, self.selector()))
        return selectors

    def selector(self):
        prefix = None
        if self.current_token.type in ['HASH', 'DOT', 'COLON', 'UNDERSCORE']:
            prefix = self.match(self.current_token.type)
        if self.current_token.type == 'IDENTIFIER':
            return (prefix, self.match('IDENTIFIER'))
        elif self.current_token.type == 'SPECIAL_IDENTIFIER':
            return self.match('SPECIAL_IDENTIFIER')
        else:
            self.error(f'Unexpected token {self.current_token.value}')

    def assignments(self):
        assignments = []
        while self.current_token.type not in ['DEDENT', 'EOF']:
            assignment = self.assignment()
            assignments.append(assignment)
            if self.current_token.type not in ['DEDENT', 'EOF']:
                if self.current_token.type != 'SEMICOLON':
                    self.error('Expected SEMICOLON')
                else:
                    self.match('SEMICOLON')
        return assignments

    def assignment(self):
        identifier = self.match('IDENTIFIER')
        self.match('COLON')
        values = [self.value()]
        while self.current_token.type in ['URL', 'STRING', 'IDENTIFIER', 'IMPORTANT', 'HASH']:
            values.append(self.value())
        return (identifier, values)

    def value(self):
        if self.current_token.type == 'URL':
            return self.match('URL')
        elif self.current_token.type == 'STRING':
            return self.match('STRING')
        elif self.current_token.type == 'IDENTIFIER':
            return self.match('IDENTIFIER')
        elif self.current_token.type == 'IMPORTANT':
            return self.match('IMPORTANT')
        elif self.current_token.type == 'HASH':
            return self.match('HASH')
        else:
            self.error(f'Unexpected token {self.current_token.value}')

    def match(self, token_type):
        if self.current_token.type == token_type:
            value = self.current_token.value
            self.current_token = self.scanner.next_token()
            return value
        else:
            self.error(f'Expected {token_type}, but found {self.current_token.type}')
