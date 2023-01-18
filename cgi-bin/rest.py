print('Content-type application/json')
print('')
import random
import json

obj = None
with open('example.json', 'r') as file: 
    obj = json.load(file)

obj['temperature'] = random.randint(-15, 30)
obj['humidity'] = random.randint(35, 100)
obj['meter']['electricity']['reading'] = random.randint(10000,100000)/10
obj['meter']['electricity']['consumption'] = random.randint(1,20)/10
obj['meter']['gas']['reading'] = random.randint(10000,100000)/10
obj['meter']['gas']['consumption'] = random.randint(1,20)/10
obj['meter']['water']['reading'] = random.randint(10000,100000)/10
obj['meter']['water']['consumption'] = random.randint(1,20)/10

#  obj['boiler']['isRun'] - здесь рандом неуместен, тк пользователь сам устанавливает значение 

obj['boiler']['temperature'] = random.randint(60, 80)
obj['boiler']['pressure'] = random.randint(10,20)/10

print(json.dumps(obj))