'''
Assignment 1 - Lexical Analyzer
CPSC 323 Spring 2019
Maxfield Wilhoite
'''

class Lexer:
    """A lexical analyzer that utilizes a Finite State Machine."""
    def __init__(self, source_file):
        self.source_file = source_file
        self.transition_table = []
        self.output_table = []
        self.column_dict = {}
        self.token_list = {5: 'Integer', 6: 'Real', 7: 'Separator', 8: 'Operator', 12: 'Unknown'}
        self.keyword_list = ['int', 'float', 'bool', 'if', 'else', 'then', 'do', 'while', 'whileend',
                             'do', 'doend', 'for', 'and', 'or', 'function']
        self.block_comment = False
        self.create_transition_table()
        self.create_column_dict()

    def analyze(self):
        """Analyze the input source file and determine which token category the lexeme is associated with."""
        for line in self.source_file:
            # Continue block comment between lines
            if self.block_comment:
                current_state = 9
            else:
                current_state = 0
            next_char_ind = 0
            current_lexeme = ''
            column = 0
            
            while next_char_ind <= len(line):
                # Reset state depended flags
                get_next_char = False
                
                # Assign the current character
                if next_char_ind == len(line):
                    current_char = ' '
                else:
                    current_char = line[next_char_ind]
                
                # Initial State
                if current_state == 0:
                    current_lexeme = ''
                    column = self.get_column_num(current_char)
                    get_next_char = True

                # Keyword or Identifier On Going
                elif current_state == 1:
                    column = self.get_column_num(current_char)
                    if column == 0 or column == 1 or column == 21:
                        get_next_char = True

                # Integer or Real On Going
                elif current_state == 2:
                    column = self.get_column_num(current_char)
                    if column == 1 or column == 10:
                        get_next_char = True

                # Real On Going
                elif current_state == 3:
                    column = self.get_column_num(current_char)
                    if column == 1:
                        get_next_char = True

                # Keyword or Identifier Done
                elif current_state == 4:
                    if current_lexeme in self.keyword_list:
                        self.output_table.append(['Keyword', current_lexeme])
                    else:
                        self.output_table.append(['Identifier', current_lexeme])

                # Comment On Going
                elif current_state == 9:
                    column = self.get_column_num(current_char)
                    get_next_char = True
                    self.block_comment = True

                # Comment Done
                elif current_state == 10:
                    column = self.get_column_num(current_char)
                    self.block_comment = False

                # Unknown Lexeme
                elif current_state == 11:
                    column = self.get_column_num(current_char)
                    if column != 22 and column != 23 and column != 24:
                        get_next_char = True
                    
                # Accepting States: Integer, Real, Separator, Operator, Unknown
                elif current_state == 5 or current_state == 6 or current_state == 7 or current_state == 8 or current_state == 12:
                    self.output_table.append([self.token_list[current_state], current_lexeme])
                
                # Dead State
                elif current_state == 13:
                    pass
                
                # Add the next char to the current lexeme if it is flagged by the current state
                if get_next_char:
                    current_lexeme += current_char
                    next_char_ind += 1
                    
                # Get new state
                current_state = self.transition_table[current_state][column]

    def results(self):
        """Output the final table with lexemes and their token category."""
        output_file = open('output_file.txt', 'w+')
        print("File successfully parsed.\nLexeme Table output into output.txt file")
        output_file.write("TOKENS\t\t\tLEXEMES\n\n")
        for lexeme in self.output_table:
            if len(lexeme[0]) < 8:
                output_file.write(lexeme[0] + "\t\t=\t" + lexeme[1] + "\n")
            else:
                output_file.write(lexeme[0] + "\t=\t" + lexeme[1] + "\n")
                
    def get_column_num(self, current_char):
        """Get the column in the transition table based on the passed in character."""
        if current_char.isalpha():
            return 0
        elif current_char.isdigit():
            return 1
        elif current_char in self.column_dict:
            return self.column_dict[current_char]
        else:
            return 26

    def create_transition_table(self):
        """Define the transition table used by the Finite State Machine to switch states."""
        self.transition_table.append([1, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 11, 13, 9, 13, 13, 11])
        self.transition_table.append([1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4, 11])
        self.transition_table.append([11, 2, 5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 11, 5, 5, 5, 5, 11])
        self.transition_table.append([6, 3, 6, 6, 6, 6, 6, 6, 6, 6, 11, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 11])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 9, 9, 9])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
                                      11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 11])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def create_column_dict(self):
        """Creates the column dictionary for the transition table."""
        self.column_dict["'"] = 2
        self.column_dict["("] = 3
        self.column_dict[")"] = 4
        self.column_dict["{"] = 5
        self.column_dict["}"] = 6
        self.column_dict["["] = 7
        self.column_dict["]"] = 8
        self.column_dict[","] = 9
        self.column_dict["."] = 10
        self.column_dict[":"] = 11
        self.column_dict[";"] = 12
        self.column_dict["*"] = 13
        self.column_dict["+"] = 14
        self.column_dict["-"] = 15
        self.column_dict["="] = 16
        self.column_dict["/"] = 17
        self.column_dict[">"] = 18
        self.column_dict["<"] = 19
        self.column_dict["%"] = 20
        self.column_dict["$"] = 21
        self.column_dict[" "] = 22
        self.column_dict["!"] = 23
        self.column_dict['\n'] = 24
        self.column_dict['\t'] = 25
