from pandocinject import Formatter

#####################################
#  block formatters for <div> tags  #
#####################################

class Base(Formatter):

    def sort_entries(self, entries):
        def custom_sort(e):
            r = [0, 0]
            # 1. sort by status
            # - 'in preparation' comes first
            # - 'under review' comes first
            # - 'forthcoming' comes next
            if e['status'] == 'proposed':
                r[0] = 6
            elif e['status'] == 'in preparation':
                r[0] = 5
            elif e['status'] == 'under review':
                r[0] = 4
            elif e['status'] == 'forthcoming':
                r[0] = 3
            elif e['status'] == 'published':
                r[0] = 2
            # 2. sort by date_updated
            r[1] = e['date_updated']
            # 3. sort by title/description
            a = str()
            if 'title' in e:
                a = e['title']
            elif 'description' in e:
                a = e['description']
            return tuple(r) + tuple(a)
        return sorted(entries, key=lambda x: custom_sort(x), reverse=True)

class EdinburghCV(Base):

    def format_entry(self, e):
        import sys
        from pandocinject.pandocinject import log
        log('INFO', '  - ' + e.get('title', 'No title!'))
        from style import edinburghcv
        if 'published' in e:
            n = e['published']['type']
        else:
            n = 'default'
        f = getattr(edinburghcv, n, edinburghcv.default)
        return f(e)

class Quick(Base):

    def format_entry(self, e):
        import sys
        from pandocinject.pandocinject import log
        log('INFO', '  - ' + e.get('title', 'No title!'))
        from style import quick
        if 'published' in e:
            n = e['published']['type']
        else:
            n = 'default'
        f = getattr(quick, n, quick.default)
        return f(e)
