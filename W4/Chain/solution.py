class EventGet:
    def __init__(self, kind):
        self.kind = kind
        #print(self.kind)
        
        
class EventSet:
    def __init__(self, value):
        self.value = value
        

class NullHandler:
    
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, obj, event):
        if self.successor is not None:
            self.successor.handle(obj, event)

            
class StrHandler(NullHandler):
    def handle(self, obj, event):
        if type(event) == EventSet:
            if type(event.value) == str:
                obj.string_field = event.value
            else:
                if self.successor is not None:
                    self.successor.handle(obj, event)
        elif type(event) == EventGet:
            #print(event.kind)
            if event.kind == str:
                return obj.string_field
            else:
                if self.successor is not None:
                    return self.successor.handle(obj, event)
        else:
            if self.successor is not None:
                self.successor.handle(obj, event)
            
            
class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if type(event) == EventSet:
            if type(event.value) == float:
                obj.float_field = event.value
            else:
                if self.successor is not None:
                    self.successor.handle(obj, event)
        elif type(event) == EventGet:
            if event.kind == float:
                return obj.float_field
            else:
                if self.successor is not None:
                    return self.successor.handle(obj, event)
        else:
            if self.successor is not None:
                self.successor.handle(obj, event)
            
            
class IntHandler(NullHandler):
    def handle(self, obj, event):
        if type(event) == EventSet:
            if type(event.value) == int:
                obj.integer_field = event.value
            else:
                if self.successor is not None:
                    self.successor.handle(obj, event)
        elif type(event) == EventGet:
            if event.kind == int:
                return obj.integer_field
            else:
                if self.successor is not None:
                    return self.successor.handle(obj, event)
        else:
            if self.successor is not None:
                self.successor.handle(obj, event)