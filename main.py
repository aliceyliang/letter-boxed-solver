from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
import os

app = Flask(__name__)

### CACHING ###
config = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 86400, # 1 day
    "CACHE_REDIS_HOST": os.environ.get('REDISHOST', 'localhost'),
    "CACHE_REDIS_PORT": int(os.environ.get('REDISPORT', 6379))
}
app.config.from_mapping(config)
cache = Cache(app)

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

todays_metadata = get_todays_metadata() # run function on load

### FUNCTIONS FOR SOLVING THE PUZZLE ### 

def get_letters(side):
  let = request.args.get(side)
  let = ''.join(filter(str.isalpha, let))
  let_list = list(let.upper())
  return dict((s, side) for s in let_list)

def clean_letters(l, t, r, b):
    left = get_letters(l)
    top = get_letters(t)
    right = get_letters(r)
    bottom = get_letters(b)
    pos = {**left, **top, **right, **bottom}
    return pos

def get_words(file, pos, chars):

    with open(file) as word_file:
        actual_words = sorted(set(list(word.strip().upper() for word in word_file) + todays_metadata['nyt_solution']))
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

# helper function
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
    solutions = {a:b for a in candidates for b in word_list if set(a+b)==chars and a[-1]==b[0]}
    ext = [[a+'-'+b,to_base(a+b)+b[-1]] for a in word_list for b in word_list if a!=b and a[-1]==b[0]]
    vals = ['-'.join([e[0],solutions[e[1]]]) for e in ext if e[1] in solutions.keys()]
    return [v.split('-') for v in vals]

num_map = {'1': {'text': 'one', 'function': one_word_solution},
           '2': {'text': 'two', 'function': two_word_solution},
           '3': {'text': 'three', 'function': three_word_solution}}


def display_answers(sets, num):
    nyt_solution_today = todays_metadata['nyt_solution']
    if sets == []:
        return "No " + num_map[num]['text'] + "-word solutions found!"
    else:
        output = ""
        for s in sets:
            if s == nyt_solution_today:
                output += "<ul>" + " — ".join(s) + " ⭐️ <i><b>NYT Solution</b></i>" +  "</ul>"
            else:
                output += "<ul>" + " — ".join(s) + "</ul>"
        return "<span>" + output + "</span>"

def solve_puzzle(pos, num, wordfile, exclude = []): # optionally exclude a list of answers
    chars = set(pos.keys())
    wordset = get_words(wordfile, pos, chars)
    answers = num_map[num]['function'](wordset, chars)
    
    answers = [x for x in answers if x not in exclude]

    return answers, num

def get_html(pos, number, wordfile, exclude = []):
    if len(pos)==12:
        answers, num = solve_puzzle(pos, number, wordfile, exclude)
        result = display_answers(answers,num)
        return jsonify({'html': str(result)})
    else:
        return jsonify({'html': "Please input 3 distinct letters per side!"})

### RUN APP ON FLASK ### 

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/populate')
def auto_populate():
    return todays_metadata['sides']

def make_cache_key_maker(route):
    def make_cache_key():
        number = request.args.get('number')
        pos = clean_letters('left','top','right','bottom')
        left = sorted([k for k, v in pos.items() if v == 'left'])
        top = sorted([k for k, v in pos.items() if v == 'top'])
        right = sorted([k for k, v in pos.items() if v == 'right'])
        bottom = sorted([k for k, v in pos.items() if v == 'bottom'])
        all = "|".join(sorted(["".join(left), "".join(top), "".join(right), "".join(bottom)]))
        return ",".join([route, number, all])
    return make_cache_key

@app.route('/transform')
@cache.cached(make_cache_key=make_cache_key_maker("transform"))
def transform():
    number = request.args.get('number')
    pos = clean_letters('left','top','right','bottom')
    return get_html(pos, number, "words_easy.txt")

@app.route('/transform_hard')
@cache.cached(make_cache_key=make_cache_key_maker("transform_hard"))
def transform_hard():
    number = request.args.get('number')
    pos = clean_letters('left','top','right','bottom')
    easy_answers, num = solve_puzzle(pos, number, "words_easy.txt")
    return get_html(pos, number, "words_hard.txt", exclude=easy_answers)

if __name__ == "__main__":
    app.run(debug=True)
