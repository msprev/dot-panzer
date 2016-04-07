from pandocinject import Selector

##########################
#  Status of publication #
##########################

class Proposed(Selector):
    def select(self, e):
        if e.get('status', 'x') == 'proposed':
            return True
        return False

class InPreparation(Selector):
    def select(self, e):
        if e.get('status', 'x') == 'in preparation':
            return True
        return False

class UnderReview(Selector):
    def select(self, e):
        if e.get('status', 'x') == 'under review':
            return True
        return False

class Forthcoming(Selector):
    def select(self, e):
        if e.get('status', 'x') == 'forthcoming':
            return True
        return False

class Published(Selector):
    def select(self, e):
        if e.get('status', 'x') == 'published':
            return True
        return False

##########################
#  Types of publication  #
##########################

class Monograph(Selector):
    def select(self, e):
        if 'published' in e \
        and e['published'].get('type', 'x') in ['monograph']:
            return True
        return False

class EditedCollection(Selector):
    def select(self, e):
        if 'published' in e \
        and e['published'].get('type', 'x') in ['editedcollection']:
            return True
        return False

class SpecialIssue(Selector):
    def select(self, e):
        if 'published' in e \
        and e['published'].get('type', 'x') in ['specialissue']:
            return True
        return False

class Article(Selector):
    def select(self, e):
        if 'published' in e \
        and e['published'].get('type', 'x') in ['article']:
            return True
        return False

class BookReview(Selector):
    def select(self, e):
        if 'published' in e \
        and e['published'].get('type', 'x') in ['bookreview']:
            return True
        return False

class InCollection(Selector):
    def select(self, e):
        if 'published' in e \
        and e['published'].get('type', 'x') in ['incollection']:
            return True
        return False

class Misc(Selector):
    def select(self, e):
        if 'published' in e \
        and e['published'].get('type', 'x') in ['misc']:
            return True
        return False

################
#  Authorship  #
################

class SingleAuthor(Selector):
    def select(self, e):
        if len(e.get('author', ['x'])) == 1:
            return True
        return False

