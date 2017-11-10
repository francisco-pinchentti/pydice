README.md
=========

## Description

A simple python dice rolling library, including a cli for quick tests.
Supports parsing of simple expressions found in board games or rpgs involving
different types of dices and operations like addition and substraction.

## Running

Launch the cli with an expression like this:

```bash
python dice_cli.py 8d6+24
```

It also supports a few arguments for multiple rolls, average result, etc

```bash
python dice_cli.py "2d6+6+1d6" -n "2h axe of shock" -c 10 -avg
python dice_cli.py "4d4+4" --name "Magic Missile IV" -c 4 -avg
python dice_cli.py "6d4l1+1" 
```

Additionally, a few dice roll modifiers where introduced:

* Append "h" and a number "n" to take the highest n dices
* Append "l" and a number "n" to take the lowest n dices

## Known issues

* Asking to take the n highest or lowest on an expression where n > total ammount of dices, such as 3d6h4
* Asking to take the n highest or lowest on an expression where n == 0, such as 2d4l0

Calling the cli with a leading **-** on the expression may cause the argument parser to fail:

```bash
python dice_cli.py "-1d4"
```

As a workaround you can add a **0** at the beggining of the expression:

```bash
python dice_cli.py "0-1d4"
```
