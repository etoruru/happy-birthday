PRODUCT_LIST = ['amount', 'unit']
DISH_LIST = ['people', 'count_stuff', 'stuff']
PRICE_LIST = ['price','amount','unit']
ENERGYVAL_LIST = ['amount', 'unit', 'pr', 'fats', 'chd','cal']

stuff = {}
amount_to_cook = {}
num_food = {}
energy_value = {}

n = []

dish = {}
price_dishes = {}
info_food = {}

def read_file():
    with open('file.txt', 'r') as f:
        text =[line.split(' ') for line in f]
    return text


text = read_file()


def create_dict(l, i):
    global text
    line = [text[i][n+1] for n in range(len(text[i])-1)]
    result = dict(zip(l,line))
    return result

def create(stuff, dish, price_dishes,info_food):
    i = 0
    while i != len(text):
        if len(text[i]) == 1:
            n.append(text[i])
            i += 1
        elif len(text[i]) == 3:
            name_food = [text[i][j] for j in range(len(text[i]))]
            name = name_food[0]
            name_food.pop(0)
            people = int(name_food[0])
            count_stuff = int(name_food[1])
            i += 1
            j = 0
            while j != count_stuff:
                name_stuff = text[i][0]
                st = create_dict(PRODUCT_LIST, i)
                stuff.update({name_stuff: st})
                j += 1
                i += 1
            di = dict(zip(DISH_LIST, [people, count_stuff,stuff]))
            dish.update({name: di})
            stuff = {}
        elif len(text[i]) == 4:
            name_stuff = text[i][0]
            price_dish = create_dict(PRICE_LIST, i)
            price_dishes.update({name_stuff: price_dish})
            i += 1
        else:
            name_stuff = text[i][0]
            info_f = create_dict(ENERGYVAL_LIST, i)
            info_food.update({name_stuff: info_f})
            i += 1

create(stuff, dish, price_dishes,info_food)
#===============================================================

def count_amount_to_cook():
    global dish
    sum = 0
    list_result = []
    result = {}
    for i in dish.keys():
        dish_keys = list(dish[i].keys())
        num_people = dish[i][dish_keys[0]]
        stuff = dish[i][dish_keys[len(dish_keys)-1]]
        stuff_keys = list(stuff.keys())
        line = {j: [int(stuff[j]['amount'])*num_people, stuff[j]['unit']]for j in stuff_keys}
        list_result.append(line)
    for key1 in list_result[0]:
        for key2 in list_result[1]:
            if key1 == key2:
                a = list_result[0][key1][0]
                b = list_result[1][key2][0]
                sum = a + b
                list_result[1][key2][0] = sum
    for i in list_result:
        result.update(i)
    return result


def convert_unit(name_food, dict_):
    if  dict_[name_food]['unit'] == 'l\n' or dict_[name_food]['unit'] == 'l':
        dict_[name_food]['unit'] = 'ml'
        dict_[name_food]['amount'] = int(dict_[name_food]['amount']) * 1000
    elif dict_[name_food]['unit'] == 'tens\n':
        dict_[name_food]['unit'] = 'cnt'
        dict_[name_food]['amount'] = int(dict_[name_food]['amount']) * 10
    elif dict_[name_food]['unit'] == 'kg':
        dict_[name_food]['unit'] = 'g'
        dict_[name_food]['amount'] = int(dict_[name_food]['amount']) * 1000


def count_amount_to_buy(name_food, d):   # name_food: string; d: dict;
    global price_dishes
    counter = 1
    if name_food in d:
        if d[name_food][1] != price_dishes[name_food]['unit']:
            convert_unit(name_food, price_dishes)
        if d[name_food][0] < int(price_dishes[name_food]['amount']):
            return counter
        else:
            amount = d[name_food][0]
            while amount > int(price_dishes[name_food]['amount']):
                counter += 1
                amount -= int(price_dishes[name_food]['amount'])
            return counter
    else:
        counter = 0
    return counter


def count_price(d):       # d:dict
    global price_dishes
    sum = 0
    for key in list(price_dishes.keys()):
        if key in d:
            sum += int(price_dishes[key]['price']) * d[key]
    return sum


def num_proteins(name_food, info_food, dish):
    sum = 0
    for key in list(dish[name_food]['stuff'].keys()):
        if key in list(info_food.keys()):
            sum += float(info_food[key]['pr']) * float(dish[name_food]['stuff'][key]['amount']) / float(info_food[key]['amount'])
    return sum


def num_fats(name_food, info_food, dish):
    sum = 0
    for key in list(dish[name_food]['stuff'].keys()):
        if key in list(info_food.keys()):
            sum += float(info_food[key]['fats']) * float(dish[name_food]['stuff'][key]['amount']) / float(info_food[key]['amount'])
    return sum


def num_carbohydrates(name_food, info_food, dish):
    sum = 0
    for key in list(dish[name_food]['stuff'].keys()):
        if key in list(info_food.keys()):
            sum += float(info_food[key]['chd']) * float(dish[name_food]['stuff'][key]['amount']) / float(info_food[key]['amount'])
    sum = round(sum, 3)
    return sum


def count_cal(name_food, info_food, dish):  # s:string
    cal = 0
    for key in list(dish[name_food]['stuff'].keys()):
        if info_food[key]['unit'] != dish[name_food]['stuff'][key]['unit']:
            convert_unit(key, info_food)
        if key in list(info_food.keys()):
            info_food[key]['cal'] = info_food[key]['cal'].replace('\n', '')
            cal += (float(info_food[key]['cal']) * float(dish[name_food]['stuff'][key]['amount']) / float(info_food[key]['amount']))
    return cal


def write_to_file(sum,num_food,energy_value):
    with open('result.txt','w') as f:
        f.writelines(str(sum) + '\n')
        for key,value in num_food.items():
            string = key + ' ' + str(value)
            f.writelines(string + '\n')
        for key, value in energy_value.items():
            val = ''.join(str(value))
            string = key + ' ' + val
            f.writelines(string + '\n')



if __name__ == '__main__':
    amount_to_cook = count_amount_to_cook()
    for i in list(price_dishes.keys()):
        c = count_amount_to_buy(i,amount_to_cook)
        num_food.update({i: c})
    sum = count_price(num_food)
    for key in list(dish.keys()):
        cal = count_cal(key, info_food,dish)
        proteins = num_proteins(key, info_food,dish)
        fats = num_fats(key, info_food,dish)
        carbohydrates = num_carbohydrates(key, info_food,dish)
        energy_value.update({key: [proteins,fats,carbohydrates,cal]})
    write_to_file(sum,num_food,energy_value)
