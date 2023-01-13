## THIS FILE IS NOT RUN IN THE APP ##


#### This cleaning is previously applied to the original wordlist txt files as referenced in the readme
## def clean_words(file):
##     with open(file) as word_file:
##         actual_words = list(word.strip().upper() for word in word_file)
##         valid_words = [w for w in actual_words if len(w)>=3]
##
##         toss = []
##         for word in valid_words:
##             ## make sure letters don't repeat
##             letters = list(word)
##             num = 1
##             while num < len(letters):
##                 if (letters[num] == letters[num-1]):
##                     toss.append(word)
##                     num = len(letters)
##                 else:
##                     num += 1
##         return [w for w in valid_words if w not in toss]
