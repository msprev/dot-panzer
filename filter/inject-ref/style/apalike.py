def default(e):
    # get the data
    author = author_or_editor(e, 5)
    year = myget(e, 'year', 'no year')
    title = myget(e, 'title', '=no title=')
    bibtex_key = e['ID']
    bibtex_type = e['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += "'%s'" % title
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text

def article(e):
    # get the data
    author = author_or_editor(e, 5)
    year = myget(e, 'year', 'no year')
    title = myget(e, 'title', '=no title=')
    journal = myget(e, 'journal', '=no journal=')
    volume = myget(e, 'volume', None)
    pages = myget(e, 'pages', None)
    bibtex_key = e['ID']
    bibtex_type = e['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += "'%s'" % title
    text += ', '
    text += '*%s*' % journal
    if volume:
        text += ' '
        text += volume
    if pages:
        text += ', '
        text += ' ' + pages
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text

def unpublished(e):
    # get the data
    author = author_or_editor(e, 5)
    year = myget(e, 'year', 'no year')
    title = myget(e, 'title', '=no title=')
    bibtex_key = e['ID']
    bibtex_type = e['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += "'%s'" % title
    text += ', '
    text += 'unpublished manuscript'
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text

def phdthesis(e):
    # get the data
    author = author_or_editor(e, 5)
    year = myget(e, 'year', 'no year')
    title = myget(e, 'title', '=no title=')
    school = myget(e, 'school', '=no school=')
    bibtex_key = e['ID']
    bibtex_type = e['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += "'%s'" % title
    text += ', '
    text += school
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text

def mastersthesis(e):
    return phdthesis(e)

def book(e):
    # get the data
    author = author_or_editor(e, 5)
    year = myget(e, 'year', 'no year')
    title = myget(e, 'title', '=no title=')
    publisher = myget(e, 'publisher', None)
    address = myget(e, 'address', None)
    edition = myget(e, 'edition', None)
    bibtex_key = e['ID']
    bibtex_type = e['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += '*%s*' % title
    if address or publisher:
        text += ', '
        if address:
            text += address
            text += ': '
        if publisher:
            text += publisher
    if edition:
        text += ', '
        if edition == '1':
            text += '1st'
        if edition == '2':
            text += '2nd'
        if edition == '3':
            text += '3rd'
        else:
            text += '%sth' % edition
        text += ' Edition'
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text

def incollection(e):
    # get the data
    author = author(e, 5)
    year = myget(e, 'year', 'no year')
    title = myget(e, 'title', '=no title=')
    publisher = myget(e, 'publisher', None)
    address = myget(e, 'address', None)
    editor = editor(e, 3)
    pages = myget(e, 'pages', None)
    booktitle = myget(e, 'booktitle', '=no booktitle=')
    bibtex_key = e['ID']
    bibtex_type = e['ENTRYTYPE']
    # build the string
    text = str()
    text += author
    text += ' '
    text += '(%s)' % year
    text += ' '
    text += '%s' % title
    if editor != '=no editor=' or booktitle != '=no booktitle=':
        text += ' in'
        if editor != '=no editor=':
            text += ' '
            text += editor
            text += ' '
            if len(e['editor']) == 1:
                text += '(Ed.)'
            else:
                text += '(Eds.)'
        text += ' '
        text += '*%s*' % booktitle
    if address or publisher:
        text += ', '
        if address:
            text += address
            text += ': '
        if publisher:
            text += publisher
    if pages:
        text += ', '
        text += 'pp. ' + pages
    # remove latex markup crap
    text = remove_latex_crap(text)
    return text

def inproceedings(e):
    return incollection(e)

def inbook(e):
    return incollection(e)


def myget(e, key, default):
    """
    return e.get(key, default)
    if bibtex version of key not found, use biblatex version
    """
    BIBLATEX = {'year': 'date',
                'journal': 'journaltitle',
                'address': 'location'}
    if key not in BIBLATEX:
        return e.get(key, default)
    else:
        return e.get(key, e.get(BIBLATEX[key], default))


def author_or_editor(e, max_num):
    """
    return string flattened list of either authors or editors
    - authors returned in preference to editors
    - if neither found, then '=no author=' is returned
    :e: bibtex entry
    :max_num: maximum number of names to include, other marked by 'et al'
    :returns: string with authors or editors
    """
    authors = myget(e, 'author', None)
    editors = myget(e, 'editor', None)
    if authors:
        return flatten_list(authors, max_num)
    elif editors:
        return flatten_list(editors, max_num)
    else:
        return '=no author='

def author(e, max_num):
    """
    return string flattened list of authors
    - if not found, then '=no author=' is returned
    :e: bibtex entry
    :max_num: maximum number of names to include, other marked by 'et al'
    :returns: string with authors
    """
    authors = myget(e, 'author', ['=no author='])
    return flatten_list(authors, max_num)


def editor(e, max_num):
    """
    return string flattened list of editors
    - if not found, then '=no author=' is returned
    :e: bibtex entry
    :max_num: maximum number of names to include, other marked by 'et al'
    :returns: string with editors
    """
    editors = myget(e, 'editor', ['=no editor='])
    return flatten_list(editors, max_num)

def flatten_list(names, max_num):
    """
    flattens a list of authors or editors and caps it a max number
    :names: list of names
    :num: maximum number of names to include, others marked by 'et al.'
    :returns: string of flattened list
    """
    # sanity check: empty list returns empty string
    if len(names) == 0:
        return ''
    # add first author
    text = names[0]
    # add next authors
    for i in range(1, min(max_num, len(names))):
            text += ' and ' + names[i]
    # add truncated authors
    if len(names) > max_num:
        text += ' et al.'
    return text

def remove_latex_crap(incoming):
    """
    remove funny latex characters and text from incoming string
    - uses list of subs for find and replace
    :returns: string with characters removed
    """
    subs = [('~', ' '),
            ('\\emph{', ''),
            ('}', ''),
            ('{', ''),
            ('\\', ''),
            ('--', '-')]
    text = incoming
    for s in subs:
        text = text.replace(s[0], s[1])
    return text

