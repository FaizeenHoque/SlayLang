class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.current_token = self.tokens[self.index]
        
        if self.tokens == []:
            raise Exception("bestie... no tokens to parse 💀")  
