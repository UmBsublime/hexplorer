from inspect import signature
from typing import get_type_hints

from textual.app import App
from textual.widgets import Label


class Dummy:
    def func1(self, x: int, y: list[str]) -> list[bool]:
        ...


typing_1 = get_type_hints(Dummy.func1)
#typing_2 = get_type_hints(Dummy.func2)
inspect_1 = signature(Dummy.func1)
#inspect_2 = signature(Dummy.func2)

typing_test = f"typing:  {typing_1}"
inspect_test = f"inspect: {inspect_1}"


class TestApp(App):
    def compose(self):
        yield Label(typing_test)
        yield Label(inspect_test)


app = TestApp()
app.run()
print(typing_test)
print(inspect_test)