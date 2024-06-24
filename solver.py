### GET NYT METADATA FOR TODAY'S PUZZLE ###

def get_todays_metadata():
    import requests, json
    r = requests.get("https://www.nytimes.com/puzzles/letter-boxed")
    # identify gameData from console
    start_string = r.text.index("window.gameData")
    start_parens = start_string + r.text[start_string:].index("{")
    end_string = start_parens+ r.text[start_parens:].index(",\"dictionary")
    todays_metadata = json.loads(r.text[start_parens:end_string]+"}")
    return {'sides': todays_metadata['sides'], 'nyt_solution': todays_metadata['ourSolution']}



def chars_to_pos(charwords, formatted=False):
    # 'mec, tal, vyr, iph'

    if not formatted:

        charwords = charwords.split(',')
        charwords = [char.strip().upper() for char in charwords]

    
    pos = {}
    # three per side with three sides:

    charno = 3
    sideno = 4
    sides = ['left','top','right','bottom']
    curr_side = 0
    curr_char = 0
    for chars in charwords:
        for char in chars:
            pos[char] = sides[curr_side]
            curr_char = curr_char + 1
            if curr_char == charno:
                curr_side = curr_side + 1
                curr_char = 0

    # print(pos)
    return pos


def get_words(file, pos, chars):

    with open(file) as word_file:
        actual_words = sorted(set(list(word.strip().upper() for word in word_file)))
        actual_words = [w for w in actual_words if len(w) >= 3]
        valid_words = [w for w in actual_words if set(w)-chars==set()]

        toss = []
        for word in valid_words:
            ## make sure letters aren't adjacent and don't repeat
            letters = list(word)
            num = 1
            while num < len(letters):
                if (pos[letters[num]] == pos[letters[num-1]]):
                    toss.append(word)
                    num = len(letters)
                else:
                    num += 1
        return [w for w in valid_words if w not in toss]

def to_base(str):
    return ''.join(sorted(set(str)))

# find one word solutions
def one_word_solution(word_list, chars):
    return [w for w in word_list if set(w) == chars]

# find two word solutions
def two_word_solution(word_list, chars):
    output = []
    for word in word_list:
        last = word[len(word)-1]
        matches = [w for w in word_list if w[0] == last and w!= word]
        for m in matches:
            pair = word + m
            if set(pair) == chars:
                output.append([word,m])
    return output

# find three word solutions
def three_word_solution(word_list, chars):
    ab = [a+b for a in word_list for b in word_list if a[-1]==b[0]]

    candidates = list(set([to_base(a)+a[-1] for a in ab]))

    # solutions = {a:b for a in candidates for b in word_list if set(a+b)==chars and a[-1]==b[0]} # why no palm

    solutions = {}
    for a in candidates:

        for b in word_list:


            if set(a+b) == chars and a[-1] == b[0]:
                if a not in solutions:
                    solutions[a] = []

                solutions[a].append(b)

    ext = [[a+'-'+b,to_base(a+b)+b[-1]] for a in word_list for b in word_list if a!=b and a[-1]==b[0]]

    # vals = ['-'.join([e[0],solutions[e[1]]]) for e in ext if e[1] in solutions.keys()]

    vals = []
    for e in ext:
        if e[1] in solutions:
            for c in solutions[e[1]]:
                vals.append('-'.join([e[0], c]))


    return [v.split('-') for v in vals]


num_map = {'1': {'text': 'one', 'function': one_word_solution},
           '2': {'text': 'two', 'function': two_word_solution},
           '3': {'text': 'three', 'function': three_word_solution}}



def solve_puzzle(pos, num, wordfile, exclude = [], include = []): # optionally exclude a list of answers

    # check for cached solution if already exists

    chars = set(pos.keys())
    # print(chars)
    wordset = get_words(wordfile, pos, chars)
    # print(f"{len(wordset) = }")
    answers = num_map[num]['function'](wordset, chars)

    answers = [x for x in answers if x not in exclude]

    for included in include:
        answers = [x for x in answers if included in x]

    answers = sorted(answers, key=lambda x: sum(len(elem) for elem in x))

    # for answer in answers:
    #     print(answer)

    return answers, num




# charwords = 'veo, ims, cap, frn' ############
todays_metadata = get_todays_metadata()
print(todays_metadata)



# wordfile = "words_scrabble.txt"
wordfile = "words_easy.txt"

pos = chars_to_pos(todays_metadata['sides'], formatted=True)
easy_answers_1, num = solve_puzzle(pos, '1', wordfile)
easy_answers_2, num = solve_puzzle(pos, '2', wordfile)
easy_answers_3, num = solve_puzzle(pos, '3', wordfile, include=[])

all_answers = easy_answers_1 + easy_answers_2 + easy_answers_3
print(f"{ len(all_answers) = }")

if todays_metadata['nyt_solution'] in all_answers:
    print(f"found today's answer: {todays_metadata['nyt_solution']}")


import datetime
now = datetime.datetime.now()
file_name = f"solves/solve_{now.strftime('%Y-%m-%d')}_{','.join(todays_metadata['sides'])}.txt"
# output = f"Current date and time: {now}"
with open(file_name, "w", encoding="utf-8") as file:
    
    file.write(f"{len(all_answers)} solutions to {now.strftime('%d/%m/%Y')}'s letter-boxed\n")
    for answer in all_answers:

        if answer == todays_metadata['nyt_solution']:
            file.write(f"{answer} - ⭐️ NYT solution\n")
        
        else:
            file.write(f"{answer}\n")

print(file_name)  # Print the file name to cap


