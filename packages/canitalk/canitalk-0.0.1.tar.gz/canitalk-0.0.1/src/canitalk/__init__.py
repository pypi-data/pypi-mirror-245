def talk(names):
    name = []
    for i in names:
        if not i in name and i != " ":
            name.append(i)
    name = len(name)
    if name % 2  == 0:
        print("CHAT WITH HER!")
    else:
        print("IGNORE HIM!")
