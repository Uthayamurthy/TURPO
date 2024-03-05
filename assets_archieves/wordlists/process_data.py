# Extract words from eff_large_wordlist.txt and write them to a wordlist.txt file.

clean_list = []

with open('eff_large_wordlist.txt') as f:
    for line in f:
        line=line.strip()
        if line == '' or line == ' ' : continue 
        clean_list.append(line[6:])

with open('wordlist.txt', 'w') as nf:
    for word in clean_list:
        print(word)
        nf.write(word + '\n')

print('Done !')
