# %%
class Dictoat:
    def __init__(self,dictt = {}):
        for item in dictt:
            if type(dictt[item]) is dict:
                setattr(self, str(item)+'_', Dictoat(dictt[item])) # the undersquare avoids coinciding with reserved keywords
            else:
                setattr(self, str(item)+'_', dictt[item])
# %%
