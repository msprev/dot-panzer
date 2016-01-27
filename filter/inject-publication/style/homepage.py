#######################
#  default formatter  #
#######################

def default(e):
    o = str()
    o += e['title']
    o += '  -- WARNING: default formatter activated!'
    return o

###########################################
#  formmatters for each publication type  #
###########################################

def article(e):
    o = str()
    o += "'%s'" % e['title']
    if 'coauthor' in e:
        o += ' (with '
        o += concat(e['coauthor'], ', ', ' and ')
        o += ')'
    o += add_urls(e)
    o += '<br>' + '\n'
    o += '*%s* (%s)' % (e['journal'], str(e['year']))
    if 'volume' in e:
        o += ' %d' % e['volume']
    if 'pages' in e:
        o += ', %s' % e['pages']
    o += add_note(e)
    return o

def bookreview(e):
    return article(e)

def book(e):
    o = str()
    o += "*%s*" % e['title']
    if 'coauthor' in e:
        o += ' (with '
        o += concat(e['coauthor'], ', ', ' and ')
        o += ')'
    o += add_urls(e)
    o += '<br>' + '\n'
    o += "%s: %s (%s), %s" % (e['publisher'], e['address'], str(e['year']), e['length'])
    o += add_note(e)
    return o

def collection(e):
    o = str()
    o += "*%s*" % e['title']
    if 'coeditor' in e:
        o += ' (with '
        o += concat(e['coeditor'], ', ', ' and ')
        o += ')'
    o += add_urls(e)
    o += '<br>' + '\n'
    o += "%s: %s (%s), %s" % (e['publisher'], e['address'], str(e['year']), e['length'])
    o += add_note(e)
    return o

def specialissue(e):
    o = str()
    o += "%s" % e['title']
    if 'coeditor' in e:
        o += ' (with '
        o += concat(e['coeditor'], ', ', ' and ')
        o += ')'
    o += add_urls(e)
    o += '<br>' + '\n'
    o += "*%s* (%s), %s" % (e['journal'], str(e['year']), e['length'])
    o += add_note(e)
    return o

def incollection(e):
    o = str()
    if 'title' in e:
        o += "'%s'" % e['title']
    elif 'description' in e:
        o += "%s" % e['description']
    if 'coauthor' in e:
        o += ' (with '
        o += concat(e['coauthor'], ', ', ' and ')
        o += ')'
    o += add_urls(e)
    o += '<br>' + '\n'
    o += 'in '
    o += concat(e['editor'], ', ', ' and ')
    o += ', '
    if len(e['editor']) > 1:
        o += '(Eds.)'
    else:
        o += '(Ed.)'
    o += ' '
    o += '*%s* (%s), %s: %s' % (e['booktitle'], str(e['year']), e['publisher'], e['address'])
    if 'pages' in e:
        o += ', pp. %s' % e['pages']
    o += add_note(e)
    return o

def misc(e):
    return incollection(e)

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

def add_note(e):
    o = str()
    if 'note' in e:
        o += ' (%s)' % e['note']
    return o

def add_urls(e):
    o = str()
    if 'pdf' in e:
        o += '[[PDF]](%s)' % e['pdf']
    if 'doi' in e:
        o += ' '
        o += '[[DOI]](http://dx.doi.org/%s)' % e['doi']
    if 'url' in e:
        for u in e['url']:
            o += ' '
            o += '[[%s]](%s)' % (u['title'], u['url'])
    if o:
        return ' -- ' + o
    return o
