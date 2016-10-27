from pandocinject import Selector

class Primary(Selector):
    def select(self, e):
        if e.get('kind', '-1') == 'primary':
            return True
        return False

class Secondary(Selector):
    def select(self, e):
        if e.get('kind', '-1') == 'secondary':
            return True
        return False

class Current(Selector):
    def select(self, e):
        if not e['degree'].get('completed', False):
            return True
        return False

class Past(Selector):
    def select(self, e):
        if not e['degree'].get('completed', False):
            return False
        return True

