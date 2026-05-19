
def world_cup(data):
    while len(data) != 1:
        bracket = [[data[x], data[x+1]] for x in range(0,len(data),2)]
        aux_list=[]
        for x in bracket:
            choice = input(f'1.- {x[0]}\n2.- {x[1]}\nSelecciona una, 1 o 2: ')
            aux_list.append(x[int(choice)-1])
        data = aux_list
    
    print(f'{data[0]} WINS!!')