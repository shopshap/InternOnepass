### split

result = []
a = ['a','b c','d','e','f']
for i in range(len(a)):
    if i == 1:
        date = a[i].split(" ")[0]
        time = a[i].split(" ")[1]
        result.append(date)
        result.append(time)
    else:
        result.append(a[i])
        
print(result)



## add
d = input()
t = input()
y = ['01','som','TOG']
y.insert(1,d+" "+t)
print(y)


