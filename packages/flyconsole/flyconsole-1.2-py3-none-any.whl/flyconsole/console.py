import sys
import os
if os.name == 'nt': # Windows
    import msvcrt
else: # Unix
    import tty

class Color:
    # NOTE: Colors range from 0 - 255
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PINK = 5
    CYAN = 6
    LIGHT_GRAY = 7
    DARK_GRAY = 8
    LIGHT_RED = 9
    LIGHT_GREEN = 10
    LIGHT_YELLOW = 11
    LIGHT_BLUE = 12
    LIGHT_PINK = 13
    LIGHT_CYAN = 14
    WHITE = 15

class _Console:
    @staticmethod
    def escape(data:str) -> None:
        Console.write(f'\033[{data}')

class Console:
    @staticmethod
    def write(data:str) -> None:
        sys.stdout.write(data)
        sys.stdout.flush()
    
    @staticmethod
    def writeln(data:str) -> None:
        Console.write(f'{data}\n')
    
    @staticmethod
    def set_color(foreground:Color=None, background:Color=None) -> None:
        if foreground: _Console.escape(f'38;5;{foreground}m')
        if background: _Console.escape(f'48;5;{background}m')
    
    @staticmethod
    def reset_color() -> None:
        _Console.escape(f'0m')
    
    @staticmethod
    def get_width() -> int:
        return os.get_terminal_size().columns
    
    @staticmethod
    def get_height() -> int:
        return os.get_terminal_size().lines
    
    @staticmethod
    def get_dimensions() -> tuple[int, int]:
        return Console.get_height(), Console.get_width()
    
    @staticmethod
    def getch() -> int:
        if os.name == 'nt':
            char = msvcrt.getch()
            if char == b'\xe0':
                arrow_key = msvcrt.getch()
                return ord(arrow_key), 1
            else:
                return ord(char), 0
        else:
            fd = sys.stdin.fileno()
            old_settings = tty.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                char = sys.stdin.read(1)
                if char == '\x1b':
                    special_key = sys.stdin.read(2)
                    return ord(special_key[-1]), 1
                else:
                    return ord(char), 0
            finally:
                tty.tcsetattr(fd, tty.TCSADRAIN, old_settings)
    
    class Cursor:
        @staticmethod
        def go_to(line:int, column:int) -> None:
            _Console.escape(f'{line+1};{column+1}f')
        
        @staticmethod
        def go_home() -> None:
            _Console.escape('H')
        
        @staticmethod
        def go_up(lines:int=1) -> None:
            _Console.escape(f'{lines}A')
        
        @staticmethod
        def go_down(lines:int=1) -> None:
            _Console.escape(f'{lines}B')
        
        @staticmethod
        def go_right(columns:int=1) -> None:
            _Console.escape(f'{columns}C')
        
        @staticmethod
        def go_left(columns:int=1) -> None:
            _Console.escape(f'{columns}D')
        
        @staticmethod
        def go_down_beginning(lines:int=1) -> None:
            _Console.escape(f'{lines}E')
        
        @staticmethod
        def go_up_beginning(lines:int=1) -> None:
            _Console.escape(f'{lines}F')
        
        @staticmethod
        def go_to_column(column:int) -> None:
            _Console.escape(f'{column+1}G')
        
        class Private:
            @staticmethod
            def hide() -> None:
                _Console.escape('?25l')

            @staticmethod
            def show() -> None:
                _Console.escape('?25h')
    
    class Clear:
        @staticmethod
        def cursor_to_end() -> None:
            _Console.escape('0J')

        @staticmethod
        def cursor_to_start() -> None:
            _Console.escape('1J')

        @staticmethod
        def clear(weird_2J_method:bool=0) -> None:
            if weird_2J_method: _Console.escape('2J')
            else: os.system('cls' if os.name == 'nt' else 'clear')

        @staticmethod
        def cursor_to_end_line() -> None:
            _Console.escape('0K')

        @staticmethod
        def cursor_to_start_line() -> None:
            _Console.escape('1K')

        @staticmethod
        def current_line() -> None:
            _Console.escape('2K')