from util import there

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
    info = e['published']
    if there('journal', info):
        o += '*' + info['journal'] + '*'
        o += ' '
    if there('year', info):
        o += '(' + str(info['year']) + ')'
        o += ' '
    if there('volume', info):
        o +=  str(info['volume'])
        o += ': '
    if there('pages', info):
            o +=  info['pages']
    o = o.rstrip()
    return o

def incollection(e):
    o = str()
    o += prefix(e)
    info = e['published']
    if there('editor', info):
        o += concat_useinitials(info['editor'], ', ', ' & ')
        o += ' '
        if len(info['editor']) > 1:
            o += '(Eds.)'
        else:
            o += '(Ed.)'
        o += ' '
    if there('booktitle', info):
        o += '*' + info['booktitle'] + '*'
    if there('year', info) and type(info['year']) is int:
        o += ' '
        o += '(' + str(info['year']) + ')'
    if there('address', info):
        o += ', '
        o += info['address']
        o += ': '
    if there('publisher', info):
        o += info['publisher']
    if there('pages', info):
        o += ', '
        o += 'pp. ' + info['pages']
    elif there('chapter', info):
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
            return 'Final version due to appear in '
    return 'Final version due to appear in '
