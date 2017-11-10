# EBNF.md

## Syntax

expression = [ "+" | "-" ] term { ("+" | "-") term };
digit = "0" .. "9";
number = digit { digit };
term = roll_expression | number;
roll_expression = number "d" number [ roll_modifier ];
roll_modifier = roll_modifier_operand number;
roll_modifier_operand = "h" | "l";

## See

http://www.icosaedro.it/bnf_chk/
