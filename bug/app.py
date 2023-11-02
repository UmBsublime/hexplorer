from inspect import signature
from typing import get_type_hints

from textual.app import App
from textual.widgets import Label


class Dummy:
    def func(self, x: int, y: list[str]) -> list[bool]:
        ...

class TestApp(App):
    def compose(self):
        yield Label(typing_test)
        yield Label(inspect_test, markup=False)

typing_test = f"typing:  {get_type_hints(Dummy.func)}"
inspect_test = f"inspect: {signature(Dummy.func)}"

app = TestApp()
app.run()
print(typing_test)
print(inspect_test)



# Output in the terminal:
# typing:  {'x': <class 'int'>, 'y': list[str], 'return': list[bool]}
# inspect: (self, x: int, y: list[str]) -> list[bool]

# Output in the textual app:
# typing:  {'x': <class 'int'>, 'y': list, 'return': list}
# inspect: (self, x: int, y: list) -> list