prd = ['amount', 'unit']
ls = ['people', 'count_stuff', 'stuff']
prs = ['price','amount','unit']
info = ['amount', 'unit', 'pr', 'fats', 'chd','cal']
stuff = {}
result = []
result1 = {}
num_food = {}
cpfch = {}

n = []

dish = {}
price_d = {}
info_food = {}

def read_file():
    with open('file.txt', 'r') as f:
        text =[line.split(' ') for line in f]
    return text


text = read_file()


def create_dict(d, l):
    global text, i
    res = {}
    n_s = text[i][0]
    p = [text[i][n+1] for n in range(len(text[i])-1)]
    c = dict(zip(l,p))
    d.update({n_s: c})
    return d


i = 0
while i != len(text):
    if len(text[i]) == 1:
        n.append(text[i])
        i += 1
    elif len(text[i]) == 3:
        name_food = [text[i][j] for j in range(len(text[i]))]
        n_f = name_food[0]
        name_food.pop(0)
        people = int(name_food[0])
        count_stuff = int(name_food[1])
        i += 1
        j = 0
        while j != count_stuff:
            st = create_dict(stuff, prd)
            j += 1
            i += 1
        di = dict(zip(ls,[people, count_stuff,st]))
        dish.update({n_f: di})
        stuff = {}
    elif len(text[i]) == 4:
        price_dishes = create_dict(price_d, prs)
        i += 1
    else:
        info_f = create_dict(info_food, info)
        i += 1

#===============================================================

def count_amount_to_cook():
    global dish
    c = 0
    for i in dish.keys():
        d = list(dish[i].keys())                          #people,count_stuff, stuff
        c = dish[i][d[0]]                                   #people
        k = dish[i][d[len(d)-1]]
        l = list(k.keys())
        r = {j: [int(k[j]['amount'])*c, k[j]['unit']]for j in l}
        result.append(r)
    for key1 in result[0]:
        for key2 in result[1]:
            if key1 == key2:
                a = result[0][key1][0]
                b = result[1][key2][0]
                c = a + b
                result[1][key2][0] = c
    for i in result:
        result1.update(i)
    return result1


def convert_unit(s, d): #s:string, r:string
    if  d[s]['unit'] == 'l\n' or d[s]['unit'] == 'l':
        d[s]['unit'] = 'ml'
        d[s]['amount'] = int(d[s]['amount']) * 1000
    elif d[s]['unit'] == 'tens\n':
        d[s]['unit'] = 'cnt'
        d[s]['amount'] = int(d[s]['amount']) * 10
    elif d[s]['unit'] == 'kg':
        d[s]['unit'] = 'g'
        d[s]['amount'] = int(d[s]['amount']) * 1000


def count_amount_to_buy(r, d):   # r: string; d: dict;
    global price_dishes
    c = 1
    if r in d:
        if d[r][1] != price_dishes[r]['unit']:
            convert_unit(r, price_dishes)
        if d[r][0] < int(price_dishes[r]['amount']):
            return c
        else:
            s = d[r][0]
            while s > int(price_dishes[r]['amount']):
                c += 1
                s -= int(price_dishes[r]['amount'])
            return c
    else:
        c = 0
    return c


def count_price(d):       # d:dict
    global price_dishes
    sum = 0
    for key in list(price_dishes.keys()):
        if key in d:
            sum += int(price_dishes[key]['price']) * d[key]
    return sum


def num_proteins(f):
    global info_f, dish
    sum = 0
    for key in list(dish[f]['stuff'].keys()):
        if key in list(info_f.keys()):
            sum += float(info_f[key]['pr']) * float(dish[f]['stuff'][key]['amount']) / float(info_f[key]['amount'])
    return sum


def num_fats(f):
    global info_f, dish
    sum = 0
    for key in list(dish[f]['stuff'].keys()):
        if key in list(info_f.keys()):
            sum += float(info_f[key]['fats']) * float(dish[f]['stuff'][key]['amount']) / float(info_f[key]['amount'])
    return sum


def num_carbohydrates(f):
    global info_f, dish
    sum = 0
    for key in list(dish[f]['stuff'].keys()):
        if key in list(info_f.keys()):
            sum += float(info_f[key]['chd']) * float(dish[f]['stuff'][key]['amount']) / float(info_f[key]['amount'])
    sum = round(sum, 3)
    return sum


def count_cal(s):  # s:string
    global dish, info_f
    cal = 0
    for key in list(dish[s]['stuff'].keys()):
        if info_f[key]['unit'] != dish[s]['stuff'][key]['unit']:
            convert_unit(key, info_f)
        if key in list(info_f.keys()):
            info_f[key]['cal'] = info_f[key]['cal'].replace('\n', '')
            cal += (float(info_f[key]['cal']) * float(dish[s]['stuff'][key]['amount']) / float(info_f[key]['amount']))
    return cal


def write_to_file(sum,n,c):
    with open('result.txt','w') as f:
        f.writelines(str(sum) + '\n')
        for key,value in n.items():
            s = key + ' ' + str(value)
            f.writelines(s + '\n')
        for key, value in c.items():
            v = ''.join(str(value))
            s = key + ' ' + v
            f.writelines(s + '\n')



if __name__ == '__main__':
    result = count_amount_to_cook()
    for i in list(price_dishes.keys()):
        c = count_amount_to_buy(i,result)
        num_food.update({i: c})
    sum = count_price(num_food)
    for key in list(dish.keys()):
        c = count_cal(key)
        p = num_proteins(key)
        f = num_fats(key)
        ch = num_carbohydrates(key)
        cpfch.update({key: [p,f,ch,c]})
    write_to_file(sum,num_food,cpfch)
