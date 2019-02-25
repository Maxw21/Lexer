
class Lexer:
    """A lexical analyzer that utilizes a Finite State Machine."""
    def __init__(self, source_file):
        self.source_file = source_file
        self.transition_table = []
        self.output_table = []
        self.column_dict = {}
        self.token_list = {5: 'Integer', 6: 'Real', 7: 'Separator', 8: 'Operator', 11: 'Unknown'}
        self.keyword_list = ['int', 'float', 'bool', 'if', 'else', 'then', 'do', 'while', 'whileend',
                             'do', 'doend', 'for', 'and', 'or', 'function']
        self.create_transition_table()
        self.create_column_dict()

    def analyze(self):
        """Analyze the input source file and determine which token category the lexeme is associated with."""
        for line in self.source_file:
            # line = line.replace('\n', '')
            current_state = 0
            # current_char = None
            next_char_ind = 0
            current_lexeme = ''
            column = 0
            while next_char_ind < len(line):
                # Initial State
                if current_state == 0:
                    current_lexeme = ''
                    current_char = line[next_char_ind]
                    current_lexeme += current_char
                    column = self.get_column(current_char)
                    current_state = self.transition_table[current_state][column]
                    next_char_ind += 1

                # Keyword or Identifier On Going
                elif current_state == 1:
                    current_char = line[next_char_ind]
                    column = self.get_column(current_char)
                    if column == 0 or column == 1 or column == 21:
                        current_lexeme += current_char
                        next_char_ind += 1
                    current_state = self.transition_table[current_state][column]

                # Integer or Real On Going
                elif current_state == 2:
                    current_char = line[next_char_ind]
                    column = self.get_column(current_char)
                    if column == 1 or column == 10:
                        current_lexeme += current_char
                        next_char_ind += 1
                    current_state = self.transition_table[current_state][column]

                # Real On Going
                elif current_state == 3:
                    current_char = line[next_char_ind]
                    column = self.get_column(current_char)
                    if column == 1:
                        current_lexeme += current_char
                        next_char_ind += 1
                    current_state = self.transition_table[current_state][column]

                # Keyword or Identifier Done
                elif current_state == 4:
                    if current_lexeme in self.keyword_list:
                        self.output_table.append(['Keyword', current_lexeme])
                    else:
                        self.output_table.append(['Identifier', current_lexeme])
                    current_state = self.transition_table[current_state][column]

                # Integer Done
                elif current_state == 5:
                    self.output_table.append([self.token_list[current_state], current_lexeme])
                    current_state = self.transition_table[current_state][column]

                # Real Done
                elif current_state == 6:
                    self.output_table.append([self.token_list[current_state], current_lexeme])
                    current_state = self.transition_table[current_state][column]

                # Separator
                elif current_state == 7:
                    self.output_table.append([self.token_list[current_state], current_lexeme])
                    current_state = self.transition_table[current_state][column]

                # Operator
                elif current_state == 8:
                    self.output_table.append([self.token_list[current_state], current_lexeme])
                    current_state = self.transition_table[current_state][column]

                # Comment On Going
                elif current_state == 9:
                    current_char = line[next_char_ind]
                    column = self.get_column(current_char)
                    current_lexeme += current_char
                    next_char_ind += 1
                    current_state = self.transition_table[current_state][column]

                # Comment Done
                elif current_state == 10:
                    current_char = line[next_char_ind]
                    column = self.get_column(current_char)
                    current_state = self.transition_table[current_state][column]

                # Unknown Lexeme
                elif current_state == 11:
                    current_char = line[next_char_ind]
                    column = self.get_column(current_char)
                    if column != 22 and column != 23 and column != 24:
                        current_lexeme += current_char
                        next_char_ind += 1
                    current_state = self.transition_table[current_state][column]

                # Unknown Lexeme Done
                elif current_state == 12:
                    self.output_table.append(['Unknown', current_lexeme])
                    current_state = self.transition_table[current_state][column]

                # Dead State
                elif current_state == 13:
                    current_state = self.transition_table[current_state][column]

    def results(self):
        """Output the final table with lexemes and their token category."""
        output_file = open('output_file.txt', 'w+')
        print("Table output into output.txt file")
        # print(self.output_table)
        output_file.write("TOKENS\t\t\tLexemes\n\n")
        for lexeme in self.output_table:
            if len(lexeme[0]) < 8:
                output_file.write(lexeme[0] + "\t\t=\t" + lexeme[1] + "\n")
            else:
                output_file.write(lexeme[0] + "\t=\t" + lexeme[1] + "\n")

    def get_column(self, current_char):
        """Get the column in the transition table based on the passed in character."""
        if current_char.isalpha():
            return 0
        elif current_char.isdigit():
            return 1
        else:
            return self.column_dict[current_char]

    def create_transition_table(self):
        """Define the transition table used by the Finite State Machine to switch states."""
        self.transition_table.append([1, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 11, 13, 9, 13])
        self.transition_table.append([1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4])
        self.transition_table.append([11, 2, 5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 11, 5, 5, 5])
        self.transition_table.append([6, 3, 6, 6, 6, 6, 6, 6, 6, 6, 11, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
                                      11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.transition_table.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def create_column_dict(self):
        """Creates the column dictionary for the transition tabl"""
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
