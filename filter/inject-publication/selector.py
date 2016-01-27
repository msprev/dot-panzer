from pandocinject import Selector

##########################
#  Dates of publication  #
##########################

class Published(Selector):
    def select(self, e):
        if type(e.get('year', 'x')) is int:
            return True
        return False

class Unpublished(Published):
    def select(self, e):
        return not super(Unpublished, self).select(e)

class Forthcoming(Selector):
    def select(self, e):
        if e.get('year', 'x') == 'forthcoming':
            return True
        return False

class Forthcoming_or_Published(Selector):
    def select(self, e):
        if type(e.get('year', 'x')) is int:
            return True
        elif e.get('year', 'x') == 'forthcoming':
            return True
        return False

class InPreparation(Selector):
    def select(self, e):
        if e.get('year', 'x') == 'in preparation':
            return True
        return False

class UnderReview(Selector):
    def select(self, e):
        if e.get('year', 'x') == 'under review':
            return True
        return False

##########################
#  Types of publication  #
##########################

class Book(Selector):
    def select(self, e):
        if e.get('type', 'x') in ['book']:
            return True
        return False

class Collection(Selector):
    def select(self, e):
        if e.get('type', 'x') in ['collection', 'special issue']:
            return True
        return False

class Article(Selector):
    def select(self, e):
        if e.get('type', 'x') in ['article']:
            return True
        return False

class BookReview(Selector):
    def select(self, e):
        if e.get('type', 'x') in ['bookreview']:
            return True
        return False

class InCollection(Selector):
    def select(self, e):
        if e.get('type', 'x') in ['incollection']:
            return True
        return False

class Misc(Selector):
    def select(self, e):
        if e.get('type', 'x') in ['misc']:
            return True
        return False

class Article_or_Chapter(Selector):
    def select(self, e):
        if e.get('type', 'x') in ['article', 'incollection']:
            return True
        return False

class Review_or_Misc(Selector):
    def select(self, e):
        if e.get('type', 'x') in ['bookreview', 'misc']:
            return True
        return False


################
#  Authorship  #
################

class SingleAuthor(Selector):
    def select(self, e):
        if 'coauthor' in e or 'coeditor' in e:
            return False
        return True

class JointAuthor(SingleAuthor):
    def select(self, e):
        return not super(JointAuthor, self).select(e)


