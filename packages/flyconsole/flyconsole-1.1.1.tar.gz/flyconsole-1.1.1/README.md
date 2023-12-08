# Fly Console

---

Fly Console is build to easy manipulate the terminal xonsole in multiple aspects It is possible to change the color, clear the terminal or manipulate the position and visibility of the cursor.

With that all said, lets get into the documentations `:D`

## Documenation

Welcome to the documentation about the fly console package c:

With this package it is possible to change the foreground and background color of the text in the terminal, write with or without line breaks, set the cursor position with different modes, show and hide the cursor or clear the console on specific parts.

Lets get right into it!

---

### Writing to the Terminal

The most important part is writing to the terminal. This can done in two ways. Write a line without a break or write a line with a break at the end.

We can write with a break like this

```py
from flyconsole import Console
Console.writeln('This is a test!')
Console.writeln('This is another test!')
```

The output will look like this

```
This is a test!
This is another test!
```

To write without a break we use

```py
from flyconsole import Console
Console.write('This is a test!')
Console.write('This is another test!')
```

With the following output

```
This is a test!This is another test!
```

As we can see, there is no line break betweeen

---

### Colors

First of all there are two ways to use colors It is possible to use just integers from 0 to 255. There are also predefined constants for the first 16 colors (0 - 15).

They can be imported as following

```py
from flyconsole import Color
```

Now lets make the console colorful!
To set the foreground color of the text you can just simply run

```py
from flyconsole import Console, Color
Console.set_color(Color.RED)
```

But you are not limited to the foreground color. You can also only set the background color

```py
from flyconsole import Console, Color
Console.set_color(background=Color.CYAN)
```

And as if that wasn't enough, you can combine these into one line

```py
from flyconsole import Console, Color
Console.set_color(Color.RED, Color.CYAN)
```

This line will do the same as the two lines before.

At some point you may want to remove all Color effects. For this the following code does the job

```py
from flyconsole import Console
Console.reset_color()
```

Pretty self-explanatory.

Lets hop on to the next part!

---

### Cursor Maniplation

Before we can start there is one thing to say.
The cursor module is a submodule of the console. You dont have to import it, you can just use it right away like this

```py
from flyconsole import Console
Console.Cursor # Thats the Cursor sub module
```

There a nine methods for manipulation of the cursor
The first is the simplest. To jump to a specific line and column just write the follwing

```py
from flyconsole import Console
Console.Cursor.go_to(line, column)
```

If u want to go to the cursors home instead, you can write

```py
from flyconsole import Console
Console.Cursor.go_home()
```

There are 4 methods to go relative amounts in different directions

```py
from flyconsole import Console

# The Cursor will go one line up
Console.Cursor.go_up() 
# The Cursor will go n lines up
Console.Cursor.go_up(n)

# The Cursor will go one line down
Console.Cursor.go_down()
# The Cursor will go n lines down
Console.Cursor.go_down(n)

# The Cursor will go one column to the right
Console.Cursor.go_right()
# The Cursor will go n columns to the right
Console.Cursor.go_right(n)

# The Cursor will go one column to the left
Console.Cursor.go_left()
# The Cursor will go n columns to the left
Console.Cursor.go_left(n)
```

As you can see, the variable n is predefined with the value 1 so you dont have to write it again and again

You can also move the cursor down n lines and then go automatically to the beginning of that line with the following code

```py
from flyconsole import Console

# n is predifned with 1
Console.Cursor.go_down_beginning(n)
```

The same also for going up

```py
from flyconsole import Console

# n is predifned with 1
Console.Cursor.go_up_beginning(n)
```

Last but not least, you can go to a specific column via

```py
from flyconsole import Console

# n is predifned with 1
Console.Cursor.go_to_column(column)
```

This can be usefull when u go up a line and want to be on another column

##### Private Modes

Private modes are some console sequences that may not work on every Terminal. To manipulate the visibility of the cursor we need private modes.

The visibility can be modified with

```py
from flyconsole import Console

Console.Cursor.Private.hide()
Console.Cursor.Private.show()
```

Its obvious which method does what

---

### Clearing the Terminal

There are six methods to clear the terminal or specific parts of it.

The first one and the most common one is there to clear the whole terminal

```py
from flyconsole import Console
Console.Clear.clear()
```

To clear from the cursor to the end of the terminal you can use the next snippet

```py
from flyconsole import Console
Console.Clear.cursor_to_end()
```

To clear from the cursor to the beginning of the terminal you can use this

```py
from flyconsole import Console
Console.Clear.cursor_to_start()
```

You can also clear from the cursor to the end or start of the current line with

```py
from flyconsole import Console
Console.Clear.cursor_to_end_line()
Console.Clear.cursor_to_start_line()
```

And you can also clear the whole current line with the following

```py
from flyconsole import Console
Console.Clear.current_line()
```