class Event(list):
    """
    something like C# event.
    Call all delegates inside when triggered.
    """
    def on(self, **dictArgs):
        for dele in self:
            dele(**dictArgs)