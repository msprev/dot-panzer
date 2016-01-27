from pandocinject import Formatter
import datetime

class EdinburghCV(Formatter):
    """
    1.  Mario Villalobos, 23 September 2014 (Scholarship from Comisión Nacional de Investigación Científica y Tecnológica CONICYT, Chile)
        -   ‘The biological roots of cognition and the social origins of mind’
        -   Passed without corrections
        -   Winner of J Warren Macalpine Prize
        -   First employment: Lecturer in philosophy and cognitive science, Universidad de Tarapacá, Chile

    2.  David Des Roches-Dueck, 6 March 2014
        -   ‘Diamonds and corkscrews: A hybrid account of realization’
        -   Passed with minor corrections
        -   Did not seek academic employment

    3.  Richard Stöckle-Schobel, 2 December 2013
        -   ‘Concept learning challenged’
        -   Passed without corrections
        -   First employment: 3-year Research Assistant in
            Ludwig-Maximilians-Universität München (LMU)
    """

    def format_entry(self, e):
        """
        format single entry
        """

        def date(e):
            if e['degree']['completed']:
                if e['degree']['kind'] in ['PhD', 'MPhil by research']:
                    return uk_date(e['degree']['date']['exam'])
                elif e['degree']['kind'] in ['UG', 'MSc']:
                    o = str()
                    o += str(e['degree']['date']['start'])
                    o += '--'
                    o += str(e['degree']['date']['end'])[2:]
                    return o
            else:
                return year(e['degree']['date']['start']) + '--'

        o = str()
        o += e['name']['first'] + ' ' + e['name']['last']
        o += ', '
        o += date(e)
        if e.get('school', False):
            o += ' '
            o += '(%s)' % e['school']
        if e['degree'].get('note', False):
            o += ' '
            o += '(%s)' % e['degree']['note']
        if e['degree'].get('scholarship', False):
            o += ' '
            o += '(%s)' % e['degree']['scholarship']
        if e['degree'].get('title', False):
            o += '\n'
            o += '    - '
            o += "'%s'" % e['degree']['title']
        if e['degree'].get('outcome', False):
            o += '\n'
            o += '    - '
            o += e['degree']['outcome']
        if e.get('prizes', False):
            for p in e['prizes']:
                o += '\n'
                o += '    - '
                o += p
        if e['degree'].get('after', False):
            o += '\n'
            o += '    - '
            o += e['degree']['after']
        return o

    def sort_entries(self, entries):
        """
        sort order:
            completed > exam date > end date > start date
        """
        def custom_sort(e):
            r = [0, 0, 0, 0]
            if e['degree']['completed'] == False:
                r[0] = 1
            if e['degree']['date'].get('exam', False):
                r[1] = str(e['degree']['date']['exam'])
            if e['degree']['date'].get('end', False):
                r[2] = str(e['degree']['date']['end'])
            if e['degree']['date'].get('start', False):
                r[2] = str(e['degree']['date']['start'])
            return tuple(r)
        return sorted(entries, key=lambda x: custom_sort(x), reverse=True)


class EdinburghCV_Digest_PhD(Formatter):
    """
    1.  Research students supervised (current): 9
        -   As primary supervisor: 4
        -   As secondary supervisor: 5

    2.  Research students supervised (total): 18
        -   As primary supervisor: 9
        -   As secondary supervisor: 9

    3.  Completed theses in past 5 years: 9
        -   As primary supervisor: 5
        -   As secondary supervisor: 4
    """

    def format_block(self, entries, starred):
        # current
        current = [e for e in entries
                   if e['degree'].get('completed', False) == False]
        current_sum = len(current)
        current_primary = len([e for e in current if e.get('kind', '-1') == 'primary'])
        current_secondary = len([e for e in current if e.get('kind', '-1') == 'secondary'])
        # total
        total = entries
        total_sum = len(entries)
        total_primary = len([e for e in total if e.get('kind', '-1') == 'primary'])
        total_secondary = len([e for e in total if e.get('kind', '-1') == 'secondary'])
        # past 5 years
        current_year = datetime.date.today().year
        completed = [e for e in entries
                     if e['degree'].get('completed', False) == True and
                     current_year - int(year(e['degree']['date']['exam'])) <= 5]
        completed_sum = len(completed)
        completed_primary = len([e for e in completed if e.get('kind', '-1') == 'primary'])
        completed_secondary = len([e for e in completed if e.get('kind', '-1') == 'secondary'])
        out = '''
1.  Research students supervised (current): %d
    -   As primary supervisor: %d
    -   As secondary supervisor: %d

2.  Research students supervised (total): %d
    -   As primary supervisor: %d
    -   As secondary supervisor: %d

3.  Completed theses in past 5 years: %d
    -   As primary supervisor: %d
    -   As secondary supervisor: %d
''' % (current_sum, current_primary, current_secondary,
    total_sum, total_primary, total_secondary,
    completed_sum, completed_primary, completed_secondary)
        return out

class EdinburghCV_Digest_MSc(Formatter):
    """
    Taught MSc students supervised: 11
    """

    def format_block(self, entries, starred):
        # total
        total = entries
        total_sum = len(entries)
        out = 'Taught MSc students supervised: %d' % total_sum
        return out


######################
#  helper functions  #
######################

def year(iso_date):
    """
    return year from iso date
    """
    d = datetime.datetime.strptime(str(iso_date), "%Y-%m-%d")
    return str(d.year)

def uk_date(iso_date):
    """
    return 4 March 2015 from 2015-03-04
    """
    d = datetime.datetime.strptime(str(iso_date), "%Y-%m-%d")
    return d.strftime('%-d %B %Y')

