from pandocinject import Formatter

class Base(Formatter):

    def sort_entries(self, entries):
        def custom_sort(e):
            r = [0, 0]
            # 1. sort by date
            # - 'in preparation' comes first
            # - 'under review' comes first
            # - 'forthcoming' comes next
            if type(e['year']) is str:
                if e['year'] == 'in preparation':
                    r[0] = 5000
                if e['year'] == 'under review':
                    r[0] = 4000
                if e['year'] == 'forthcoming':
                    r[0] = 3000
            # then normal dates come after
            if type(e['year']) is int:
                r[0] = e['year']
            # 2. sort by type
            ordering = ['book', 'collection', 'specialissue', 'article', 'incollection', 'bookreview']
            if e['type'] in ordering:
                r[1] = len(ordering) - ordering.index(e['type'])
            else:
                # put at the bottom if not known in ordering
                r[1] = -1
            # 3. sort by title
            a = str()
            if 'title' in e:
                a = e['title']
            elif 'description' in e:
                a = e['description']
            return tuple(r) + tuple(a)
        return sorted(entries, key=lambda x: custom_sort(x), reverse=True)

class EdinburghCV(Base):

    def add_entry(self, e):
        from style import edinburghcv
        f = getattr(edinburghcv, e['type'], edinburghcv.default)
        return f(e)

class Homepage(Base):

    def add_entry(self, e):
        from style import homepage
        f = getattr(homepage, e['type'], homepage.default)
        return f(e)

