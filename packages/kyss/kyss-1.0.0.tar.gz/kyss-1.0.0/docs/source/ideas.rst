Ideas for future improvement
============================

Here are some ideas that I may want to implement:

.. module:: kyss
   :no-index:

- Giving :exc:`SchemaError` and :exc:`ParsingFailure` a shared superclass in
  order to make handling errors a more smooth experience for client code. **Done**
- Integrating schema validation more tightly into the parser, especially adding
  the same detailed context to :exc:`SchemaError` as is given to
  :exc:`ParsingFailure`. **Done**
- Adding ``EnumKey`` and ``EnumValue`` schema builders for recognising
  :class:`enum.Enum`\s by their keys or values respectively.
- Catching :exc:`TypeError` and :exc:`ValueError` raised by wrapper
  functions and convert them to :exc:`SchemaError`\s, which would make it
  easier to add functionality that currently requires users to subclass
  :exc:`Schema`. **Done**
- Allowing user schema builders to register types, so they can extend typed
  schemas. **Done**
- Adding some sort of annotation so :meth:`Schema.wrap_in` is supported by
  typed schemas.
