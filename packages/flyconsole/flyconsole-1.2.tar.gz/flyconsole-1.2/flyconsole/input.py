from dataclasses import dataclass
from console import Console, Color

@dataclass
class MenuItem:
    master: any
    title: str
    _id: int

@dataclass
class KeyConfiguration:
    up: tuple = (72, 1)
    down: tuple = (80, 1)
    select: tuple = (13, 0)
    escape: tuple = (27, 0)
    cancel: tuple = (3, 0)

class ListMenu:
    def __init__(self, y:int=0, can_cancel:bool=1, can_escape:bool=1, key_configuration:KeyConfiguration=KeyConfiguration()) -> None:
        self._items = []
        self._menu_index = 0
        self._y = y
        self._key_configuration = key_configuration
        self._running = 0
        self._can_cancel = can_cancel
        self._can_escape = can_escape
    
    def add_item(self, title) -> None:
        if self._running: return
        self._items.append(MenuItem(self, title, len(self._items)))
    
    def _render(self) -> None:
        for i in range(len(self._items)):
            item = self._items[i]
            Console.Cursor.go_to(self._y+i, 0)
            Console.set_color(Color.BLACK, Color.LIGHT_BLUE if self.get_active() == item else Color.WHITE)
            Console.write(item.title + ' '*(Console.get_width() - len(item.title)))
        Console.reset_color()
    
    def get_active(self) -> None:
        return self._items[self._menu_index]

    def enable(self) -> None:
        if len(self._items) <= 0: return
        self._running = 1
        Console.Cursor.Private.hide()
        while self._running:
            self._render()
            k = Console.getch()
            if self._can_cancel and k == self._key_configuration.cancel: break
            if self._can_escape and k == self._key_configuration.escape: break
            if k == self._key_configuration.select:
                self.result = self.get_active()
                break
            if k == self._key_configuration.down and self._menu_index < len(self._items)-1: self._menu_index += 1
            if k == self._key_configuration.up and self._menu_index > 0: self._menu_index -= 1
        Console.Cursor.Private.show()
        self._running = 0