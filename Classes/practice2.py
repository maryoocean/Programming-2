#Задание 5.1

vowels = "aoe"
consonants = "bcd"
vowels_list = [i for i in vowels]
consonants_list = [i for i in consonants]
for i in vowels_list:
    n = 0
    k = 0
    while n < len(vowels_list):
        syl = consonants_list[k] + i
        print(syl)
        k += 1
        n += 1

#Задание 5.2

nouns = 'мама рама папа'
verbs = 'мыла красила'
for noun in nouns.split():
    for verb in verbs.split():
        for noun_o in nouns.split():
            print(noun + ' '+ verb + ' ' + noun_o)

#Задание 1

nums_list = [1, 2, 3, 4, 5, 6]
if len(nums_list) != 0:
    average = sum(nums_list)/len(nums_list)
    print(average)

vals = nums_list
def mean(vals):
    if len(vals) > 0:
        res = float(sum(vals))/len(vals)
    else:
        print('n/a')
    return res
    

print(mean(vals))

        
    

        


