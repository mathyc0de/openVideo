from .transform import Transform

class Plugins:
    def __init__(self, result) -> None:
        self.result = result

    def reverse(self): self.result = Transform.reverse(self.result)

    def cut(self): self.result = Transform.cut(self.result) 