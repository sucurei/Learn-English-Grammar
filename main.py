import nltk
import clips
import re


# functie de parsare, ce primeste path catre un fisier, extrage propozitiile,
# si va scrie intr-un alt fisier,
# analiza acelor propozitii (engleza)
def read_data_to_write_in_file(path):
    with open(path, 'r') as file:
        data = file.read()
        data = ''.join(data.splitlines())
        data = re.split('[.?!]', data)
    with open('data.txt', 'w') as file:
        for line in data[:-1]:
            tokens = nltk.word_tokenize(line.lstrip())
            tagged = nltk.pos_tag(tokens)
            buffer = []
            for index in range(len(tagged)):
                buffer.append(tagged[index][1])
            current = ''
            for i in buffer:
                if i not in ',:;)(':
                    file.write(str(i) + ' ')
            file.write('\n')


'''
    Reads sentence from console and returns it
    @:return the sentence read from the console
'''


def read_sentence():
    while True:
        sentence = input("Sentence:")
        if sentence[-1] not in ['.', '?', '!', ';']:
            print("You didn't finished the sentence properly.")
        else:
            cnt = 0
            for i in sentence:
                if i in ['.', '?', '!', ';']:
                    cnt = cnt + 1
            if cnt == 1:
                return sentence
            else:
                print("Read only one sentence at a time.")


def words_tagging(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    return tagged


'''
    Get rules from file 'rules' as string array
    
'''


def get_rules():
    lines = []
    file = open('rules', 'r')
    while True:
        line = file.readline()
        if not line:
            break
        lines.append(line)
    file.close()
    for i, line in enumerate(lines):
        lines[i] = lines[i][:-1]
    return lines


def validate_sentence_by_rules(rules, architecture):
    env = clips.Environment()
    for cnt, i in enumerate(rules):
        rule = '''
        (defrule rule%s
            (sentence %s)
            =>
            (printout t "The sentence is correct." crlf))
        ''' % (str(cnt), i)
        env.build(rule)
    rule = '''
    (defrule wrong
        =>
        (printout t "The sentence is wrong." crlf))
    '''
    env.build(rule)

    sentence = ''
    for i in architecture:
        sentence = sentence + i + ' '
    sentence = sentence[:-1]

    # print(sentence)

    fact_string = f'(sentence {sentence})'
    fact = env.assert_string(fact_string)
    template = fact.template

    assert template.implied == True

    validation_result = env.run()
    return validation_result


def get_result_handler_console(sentence, architecture, correctitude):
    print("The sentence:", end=" ")
    print(sentence)
    print()
    print("With the next morphology syntax:")
    print(architecture)
    print()
    print("Seems to be:", end=" ")
    if correctitude == 1:
        print("WRONG")
        print()
        final = input("Is our answer correct? (y = yes , n = no) --> ")
        if final == 'n':
            print()
            print("Thank you for your feedback.")
            print("Next time we will know the correct answer for this type of sentence.")
            append_architecture_to_existing_rules(architecture)
    else:
        print("CORRECT")


def append_architecture_to_existing_rules(architecture):
    rule = ''
    for morph in architecture:
        rule = rule + morph + ' '
    rule = rule[:-1]
    file = open("rules", "a")
    file.write(rule)
    file.write('\n')


def solve_single_sentence(user_sentence):
    pattern_to_be_validated = get_pattern_from_sentence(user_sentence)
    user_sentence_validation_result = validate_sentence_by_rules(get_rules(), pattern_to_be_validated)
    print()
    get_result_handler_console(user_sentence, pattern_to_be_validated, user_sentence_validation_result)


def get_pattern_from_sentence(sentence):
    pattern_to_be_validated = []
    for i in words_tagging(sentence):
        pattern_to_be_validated.append(i[1])
    return pattern_to_be_validated


def parse_from_console():
    solve_single_sentence(read_sentence())


def parse_from_file(file_path_user_input):
    sentences = read_from_file(file_path_user_input)
    print('Parsing sentences...')
    parsing_result = parsing_sentence_array(sentences)
    print('The result of the parsing process shown below ...')
    for i in range(len(parsing_result)):
        print(parsing_result[i])

    add_all_sentences_as_rules = input('Do you wish to add the invalid sentences as rules ? (y/n)')
    if add_all_sentences_as_rules == 'y':
        add_all_sentences_as_rules = True
    else:
        add_all_sentences_as_rules = False
    if add_all_sentences_as_rules:
        for i in range(len(parsing_result)):
            if not parsing_result[i]["parsingResult"]:
                append_architecture_to_existing_rules(parsing_result[i]["pattern"])
        print('All the needed rules added successfully!')


def parsing_sentence_array(sentences):
    rules = get_rules()
    parse_result = []
    for i in range(len(sentences)):
        current_sentence_pattern = get_pattern_from_sentence(sentences[i])

        current_sentence_is_valid = validate_sentence_by_rules(rules, current_sentence_pattern)
        if current_sentence_is_valid == 2:
            current_sentence_is_valid = True
        else:
            current_sentence_is_valid = False

        parse_result.append({
            "sentence": sentences[i],
            "parsingResult": current_sentence_is_valid,
            "pattern": current_sentence_pattern
        })
    return parse_result


def read_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return nltk.sent_tokenize(data)


def main():
    option = int(input('''
        Press the corresponding number of the desired action:
        1. Parse from console
        2. Parse from file (path required)
    '''))

    if option == 1:
        parse_from_console()
        return
    if option == 2:
        file_path_user_input = input('Write the path to the file: ')
        parse_from_file(file_path_user_input)
        return
    print('Invalid option number')


if __name__ == "__main__":
    main()
