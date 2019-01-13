from flask import Flask, render_template, redirect, url_for, request, jsonify
app = Flask(__name__)

def get_letters(side):
  let = request.args.get(side)
  let = ''.join(filter(str.isalpha, let))
  let_list = list(let.upper())
  return dict((s, side) for s in let_list)

def get_words(pos, chars):
    with open("words.txt") as word_file:
        actual_words = list(word.strip().upper() for word in word_file)
        valid_words = [w for w in actual_words if len(w)>=3 and set(w)-chars==set()]

        toss = []
        for word in valid_words:
            ## make sure letters aren't adjacent and don't repeat
            letters = list(word)
            num = 1
            while num < len(letters):
                if (pos[letters[num]] == pos[letters[num-1]]) or (letters[num] == letters[num-1]):
                    toss.append(word)
                    num = len(letters)
                else:
                    num += 1
        return [w for w in valid_words if w not in toss]

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

def display_answers(sets):
    output = ""
    for s in sets:
        output += "<ul>" + s[0] + " — " + s[1] + "</ul>"
    return output

def solve_puzzle(pos):
    chars = set(pos.keys())
    wordset = get_words(pos, chars)
    answers = two_word_solution(wordset, chars)
    return display_answers(answers)

@app.route('/')
def home():
    return "hello hello"

@app.route('/index', methods=['GET','POST'])
def index():
    # error = None
    # if request.method == 'POST':
    #     return request.form['text']
    return render_template('index.html')

# http://127.0.0.1:5000/transform?left=HAO&top=IED&right=PMT&bottom=UNR
# humanitarian notepad

#
@app.route('/transform')
def transform():
    left = get_letters('left')
    top = get_letters('top')
    right = get_letters('right')
    bottom = get_letters('bottom')
    pos = {**left, **top, **right, **bottom}
    if len(pos)==12:
        result = solve_puzzle(pos)
        return jsonify({'html': str(result)})
    else:
        return jsonify({'html': "Please input 3 distinct letters per side"})

if __name__ == "__main__":
    app.run(debug=True)
