#######################
#  default formatter  #
#######################

def default(e):
    o = '**WARNING**: default formatter activated!'
    return o

###########################################
#  formmatters for each publication type  #
###########################################

def incollection(e):
    o = str()
    o += prefix(e)
    o += concat(e['editor'], ', ', ' & ')
    o += ' '
    if len(e['editor']) > 1:
        o += '(Eds.)'
    else:
        o += '(Ed.)'
    o += ' '
    o += "*%s*" % e['booktitle']
    if type(e['year']) is int:
        o += ' (%d)' % e['year']
    o += ', '
    o += '%s: %s' % (e['address'], e['publisher'])
    if 'page' in e:
        o += ', pp. %s' % e['pages']
    o += '.'
    return o

######################
#  helper functions  #
######################

def concat(l, sep, final_sep):
    o = str()
    if not l:
        return o
    o += l[0]['first'] + ' ' + l[0]['last']
    if len(l) == 1:
        return o
    for i in range(1, len(l) - 1):
        o += sep
        o += l[i]['first'] + ' ' + l[i]['last']
    o += final_sep
    o += l[-1]['first'] + ' ' + l[-1]['last']
    return o

def prefix(e):
    o = str()
    if type(e['year']) is int:
        return 'Published in '
    elif e['year'] == 'forthcoming':
        return 'Forthcoming in '
    else:
        return '*Rough draft only. Please do not cite without permission.*'

