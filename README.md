# Описание языка

С левой части нашего правила располагается нетерминал -- язык, который мы описываем

С правой части нашего правила располагается выражение, состоящее из последовательности терминалов и нетерминалов вместе со следующими операторами:

* Повторение (0 или больше повторений аргумента): `*`
* Опциональный оператор (0 или 1 вхождение аргумента): `[]`
* Конкатенация (2 аргумента): `+`
* Альтернатива (2 аргумента): `|`
* Скобки для группировки: `()`

**Все операторы правоассоциативны**

Приоритеты операторов: 1) Скобки; 2) Повторение, опциональный оператор; 3) Конкатенация; 4) Альтернатива


Левая часть от правой отделяется с помощью `=`. После операторов аргументы идут после пробельных символов.

Комментарии начинаются с `%`

Идентификаторы -- любая комбинация символов, не начинающаяся с `_` и цифр, состоящее из букв латинского алфавита и цифр. Чтобы пометить идентификатор как стартовый нетерминал, необходимо написать `START = ` название нетерминала

Литералы -- символ из алфавита, заключенные в одинарные ковычки. Символы `%`, `'`, `\` необходимо экранировать с помощью `\`. Перенос строки -- `\n`

**Пример** 

Язык, состоящий из слов, заданных с помощью регулярного выражения: `a*(b|ba)*`

```
START = Lang
Lang = A + ('b' | ('b' + 'a'))*
A = 'a'*
```

## Грамматика

```
Program : Rule
Rule : ID = EXPR
EXPR : SYMB
     | ID
     | LBRACKET EXPR RBRACKET
     | EXPR MULT
     | LSQ EXPR RSQ
     | EXPR PLUS EXPR
     | EXPR ALT EXPR
```
## Запуск парсера

Для запуска нужна библиотека для отображения графов - graphviz
``` bash
sudo apt install graphviz
```
## Запуск подсветки синтаксиса

Необходимо переместить файл ebnf.sublime-syntax в Packages/User в директории с Sublime

После этого в Sublime можно будет в правом нижнем углу выбрать подсветку синтаксиса под названием ebnf, которая будет подсвечивать синтаксис нашего языка в файлах с форматом .txt
