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

print(todays_metadata)


