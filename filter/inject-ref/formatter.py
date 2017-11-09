from pandocinject import Formatter

#####################################
#  block formatters for <div> tags  #
#####################################

class Base(Formatter):

    def sort_entries(self, entries):
        return entries
        # return sorted(entries, key=lambda x: custom_sort(x), reverse=True)

class APA_block(Base):

    def format_entry(self, e):
        import sys
        from pandocinject.pandocinject import log
        log('INFO', '  - ' + e.get('title', 'No title!'))
        # return(e.get('title', 'No title!'))
        from style import apalike
        f = getattr(apalike, e['ENTRYTYPE'], apalike.default)
        return f(e)

    def format_block(self, entries, starred):
        """
        format a block containing entries
        """
        out = str()
        for e in entries:
            # add each entry in loose numbered list
            out += '1.  '
            # star start of item
            if e in starred:
                out += '\* '
            out += self.format_entry(e)
            out += '\n'
        return out


class APA_inline(APA_block):

    def format_block(self, entries, starred):
        """
        format a block containing entries
        """
        out = str()
        for i, e in enumerate(entries):
            if e in starred:
                out += '\* '
            out += self.format_entry(e)
            if i < len(entries)-1 and len(entries) > 1:
                out += '; '
        return out

