with open('./ft_compress/VERSION') as inp:
    data = inp.read()
    data = data.split('.')
if len(data)!=3:
    print ('Bad version')
    exit(1)
patch = str(int(data[2])+1)
with open('./ft_compress/VERSION', 'w') as out:
    out.write('.'.join(data[:2]+[patch]))
