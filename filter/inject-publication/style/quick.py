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
    o += add_coauthors(e)
    try:
        if e['published']['journal']:
            o += ', *%s*' % e['published']['journal']
    except KeyError:
        pass
    try:
        if e['published']['year']:
            o += ' (%s)' % str(e['published']['year'])
        else:
            o += ' (%s)' % e['status']
    except KeyError:
        pass
    try:
        if e['published']['volume']:
            o += ' %s' % str(e['published']['volume'])
    except KeyError:
        pass
    try:
        if e['published']['pages']:
            o += ', %s' % e['published']['pages']
    except KeyError:
        pass
    o += add_note(e)
    o += add_urls(e)
    return o

def bookreview(e):
    return article(e)

def monograph(e):
    o = str()
    o += "*%s*" % e['title']
    o += add_coauthors(e)
    o += ', '
    try:
        if e['published']['publisher']:
            o += '%s' % e['published']['publisher']
    except KeyError:
        pass
    try:
        if e['published']['address']:
            o += ': %s' % e['published']['address']
    except KeyError:
        pass
    try:
        if e['published']['year']:
            o += ' (%s)' % str(e['published']['year'])
        else:
            o += ' (%s)' % e['status']
    except KeyError:
        pass
    try:
        if e['published']['length']:
            o += ', %s' % e['published']['length']
    except KeyError:
        pass
    o += add_note(e)
    o += add_urls(e)
    return o

def editedcollection(e):
    o = str()
    o += "*%s*" % e['title']
    o += add_coeditors(e)
    o += ', '
    try:
        if e['published']['publisher']:
            o += '%s' % e['published']['publisher']
    except KeyError:
        pass
    try:
        if e['published']['address']:
            o += ': %s' % e['published']['address']
    except KeyError:
        pass
    try:
        if e['published']['year']:
            o += ' (%s)' % str(e['published']['year'])
        else:
            o += ' (%s)' % e['status']
    except KeyError:
        pass
    try:
        if e['published']['length']:
            o += ', %s' % e['published']['length']
    except KeyError:
        pass
    o += add_note(e)
    o += add_urls(e)
    return o

def specialissue(e):
    o = str()
    o += "%s" % e['title']
    o += add_coeditors(e)
    o += ', '
    try:
        if e['published']['journal']:
            o += '*%s*' % e['published']['journal']
    except KeyError:
        pass
    try:
        if e['published']['year']:
            o += ' (%s)' % str(e['published']['year'])
        else:
            o += ' (%s)' % e['status']
    except KeyError:
        pass
    try:
        if e['published']['length']:
            o += ', %s' % e['published']['length']
    except KeyError:
        pass
    o += add_note(e)
    o += add_urls(e)
    return o

def incollection(e):
    o = str()
    if 'title' in e:
        o += "'%s'" % e['title']
    elif 'description' in e:
        o += "%s" % e['description']
    o += add_coauthors(e)
    o += ', '
    o += 'in '
    o += add_volumeeditors(e)
    o += ' '
    try:
        if e['published']['booktitle']:
            o += '*%s*' % e['published']['booktitle']
    except KeyError:
        pass
    try:
        if e['published']['year']:
            o += ' (%s)' % str(e['published']['year'])
        else:
            o += ' (%s)' % e['status']
    except KeyError:
        pass
    try:
        if e['published']['publisher']:
            o += ', %s' % e['published']['publisher']
    except KeyError:
        pass
    try:
        if e['published']['address']:
            o += ': %s' % e['published']['address']
    except KeyError:
        pass
    try:
        if e['published']['pages']:
            o += ', %s' % e['published']['pages']
    except KeyError:
        pass
    o += add_note(e)
    o += add_urls(e)
    return o

def misc(e):
    return incollection(e)

######################
#  helper functions  #
######################


def add_coauthors(e):
    o = str()
    if len(e['author']) == 1:
        return o
    o += ' (with '
    a_list = [a
              for a in e['author']
              if a['name_last'] != 'Sprevak' and a['name_first'] != 'Mark']
    o += concat(a_list, ', ', ' and ')
    o += ')'
    return o

def add_coeditors(e):
    o = str()
    if len(e['editor']) == 1:
        o += ' (Ed.)'
        return o
    o += ' (with '
    a_list = [a
              for a in e['editor']
              if a['name_last'] != 'Sprevak' and a['name_first'] != 'Mark']
    o += concat(a_list, ', ', ' and ')
    o += ')'
    o += ' (Eds.)'
    return o

def add_volumeeditors(e):
    o = str()
    try:
        if not e['published']['editor']:
            return o
    except KeyError:
        return o
    o += concat_useinitials(e['published']['editor'], ', ', ' and ')
    if len(e['published']['editor']) > 1:
        o += ' (Eds.)'
    else:
        o += ' (Ed.)'
    return o

def name2initials(name):
   return ' '.join([n[0] + '.' for n in name.split()])

def concat(l, sep, final_sep):
    o = str()
    if not l:
        return o
    o += l[0]['name_first'] + ' ' + l[0]['name_last']
    if len(l) == 1:
        return o
    for i in range(1, len(l) - 1):
        o += sep
        o += l[i]['name_first'] + ' ' + l[i]['name_last']
    o += final_sep
    o += l[-1]['name_first'] + ' ' + l[-1]['name_last']
    return o

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

def add_note(e):
    o = str()
    if 'published' in e and 'note' in e['published'] and e['published']['note']:
        o += ' (%s)' % e['published']['note']
    return o

def add_urls(e):
    o = str()
    return o
