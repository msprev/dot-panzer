#######################
#  default formatter  #
#######################

def default(e):
    o = '**WARNING**: default formatter activated!'
    return o

###########################################
#  formmatters for each publication type  #
###########################################

def article(e):
    o = str()
    o += prefix(e)
    info = e['publication']
    if 'journal' in info:
        o += '*' + info['journal'] + '*'
        o += ' '
    if 'year' in info:
        o += '(' + str(info['year']) + ')'
        o += ' '
    if 'volume' in info:
        o +=  str(info['volume'])
        o += ': '
        if 'pages' in info:
            o +=  info['pages']
    o = o.rstrip()
    return o

def incollection(e):
    o = str()
    o += prefix(e)
    info = e['publication']
    if 'editor' in info:
        o += concat_useinitials(info['editor'], ', ', ' & ')
        o += ' '
        if len(info['editor']) > 1:
            o += '(Eds.)'
        else:
            o += '(Ed.)'
        o += ' '
    if 'booktitle' in info:
        o += '*' + info['booktitle'] + '*'
        o += ' '
    if 'year' in info:
        o += '(' + str(info['year']) + ')'
        o += ', '
    if 'address' in info:
        o += info['address']
        o += ': '
    if 'publisher' in info:
        o += info['publisher']
        o += ', '
    if 'pages' in info:
        o += 'pp. ' + info['pages']
    elif 'chapter' in info:
        o += 'chapter ' + info['chapter']
    o = o.rstrip()
    o = o.rstrip(',')
    return o

def bookreview(e):
    return article(e)

######################
#  helper functions  #
######################

def name2initials(name):
   return ' '.join([n[0] + '.' for n in name.split()])

def concat_useinitials(l, sep, final_sep):
    o = str()
    # no one in list
    if not l:
        return o
    # first person in list
    o += name2initials(l[0]['name_first'])
    o += ' '
    o += l[0]['name_last']
    if len(l) == 1:
        return o
    # everyone else until penultimate person
    for i in range(1, len(l) - 1):
        o += sep
        o += name2initials(l[i]['name_first'])
        o += ' '
        o += l[i]['name_last']
    # last person in list
    o += final_sep
    o += name2initials(l[-1]['name_first'])
    o += ' '
    o += l[-1]['name_last']
    return o

def prefix(e):
    if 'status' in e:
        if e['status'] == 'published':
            return 'Published in '
        elif e['status'] == 'forthcoming':
            return 'Forthcoming in '
    else:
        return '*Rough draft only. Please do not cite without permission.*'

