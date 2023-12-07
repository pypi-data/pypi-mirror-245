from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from decimal import Decimal as PyDecimal
from decimal import InvalidOperation
from typing import (Any, NotRequired, Required, Self, get_args, get_origin,
                    is_typeddict)

from .ast import Node, ScalarNode
from .errors import KyssSchemaError, SourceLocation


class Schema:
    '''Base class for all schema builders. You can implement your own schema builder by subclassing ``Schema`` and overriding the ``validate`` method.'''

    def validate(self, node: Node) -> Any:
        '''Validates its argument. If the argument is accepted, returns the value that should represent the data.
        If the argument is not accepted, raises :py:exc:`KyssSchemaError`.'''

        raise NotImplementedError

    def __or__(self, other: 'Schema') -> 'Alternatives':
        return Alternatives([*self._get_alternatives(), *other._get_alternatives()])

    def _get_alternatives(self) -> Iterator['Schema']:
        yield self

    def wrap_in(self, fn: Callable[[Any], Any], expected: str | None = None) -> 'Wrapper':
        r'''Wrap a schema in a callable.

        >>> parse_string('6', Int().wrap_in(lambda x: x * 7))
        42
        >>> parse_string('- one\n- seven\n- thirteen', List(Str().wrap_in(len)))
        [3, 5, 8]
        '''

        return Wrapper(self, fn, expected)

@dataclass
class Wrapper(Schema):
    schema: Schema
    fn: Callable[[Any], Any]
    expected: str | None = None

    def validate(self, node: Node) -> Any:
        try:
            return self.fn(self.schema.validate(node))
        except (TypeError, ValueError) as e:
            raise node.error(self.expected or str(self.fn)) from e

@dataclass
class Alternatives(Schema):
    '''``schema_1 | schema_2 | ... | schema_n`` <=> ``Alternatives([schema_1, schema_2, ..., schema_n])``

    This tries to validate the parsed value with each schema given. The first schema that accepts the value is used.
    Only fails if none of the alternatives accept it.'''

    alternatives: list[Schema]

    def validate(self, node: Node) -> Any:
        exp = {}
        for alternative in self.alternatives:
            try:
                return alternative.validate(node)
            except KyssSchemaError as e:
                exp |= e.expected
        raise KyssSchemaError(node.location, exp)

    def _get_alternatives(self) -> Iterator[Schema]:
        yield from self.alternatives

@dataclass
class Str(Schema):
    'Accepts any scalar and produces it unchanged.'

    def validate(self, node: Node) -> Any:
        node.require_scalar()
        return node.value

@dataclass
class Bool(Schema):
    "Accepts scalars that case-insensitively equal to 'true' or 'false'. Produces a ``bool``."

    def validate(self, node: Node) -> Any:
        if node.kind == 'scalar':
            v = node.value.lower()
            if v == 'true':
                return True
            elif v == 'false':
                return False
        raise node.error('true or false')

@dataclass
class Int(Schema):
    'Accepts scalars that Python can interpret as integers. Produces an ``int``.'

    def validate(self, node: Node) -> Any:
        if node.kind == 'scalar':
            try:
                return int(node.value)
            except ValueError:
                pass
        raise node.error('integer')

@dataclass
class Float(Schema):
    'Accepts scalars that Python can interpret as floating point numbers. Produces a ``float``.'

    def validate(self, node: Node) -> Any:
        if node.kind == 'scalar':
            try:
                return float(node.value)
            except ValueError:
                pass
        raise node.error('floating point number')


@dataclass
class Decimal(Schema):
    'Accepts scalars that Python can interpret as a decimal number. Produces a ``decimal.Decimal``.'

    def validate(self, node: Node) -> Any:
        if node.kind == 'scalar':
            try:
                return PyDecimal(node.value)
            except InvalidOperation:
                pass
        raise node.error('decimal number')

@dataclass
class List(Schema):
    'Accepts sequences where each item is accepted by the ``item`` schema. Produces a ``list``.'

    item: Schema

    def validate(self, node: Node) -> Any:
        node.require_sequence()
        return [self.item.validate(item) for item in node.children]

@dataclass
class Dict(Schema):
    '''Accepts mappings. Produces a ``dict``.

    :param required: maps required keys to the schemas for their respective values.
    :param values: the schema used for values whose keys are not specified in either required or optional. If ``None``, rejects mappings with unspecified keys.
    :param optional: maps optional keys to the schemas for their respective values.'''

    required: dict[str, Schema]
    values: Schema | None = None
    optional: dict[str, Schema] | None = field(default=None, kw_only=True)

    def validate(self, node: Node) -> Any:
        node.require_mapping()
        v = node.children
        if missing_keys := self.required.keys() - v.keys():
            raise node.error(f'a mapping that has the keys {sorted(self.required)}')
        unspecified_keys = v.keys() - self.required.keys()
        if self.optional is not None:
            unspecified_keys -= self.optional.keys()
        if unspecified_keys and self.values is None:
            keys = sorted([*self.required, *(self.optional or ())])
            raise node.error(f'a mapping that only has the keys {keys}')
        specified = {key: schema.validate(v[key]) for key, schema in self.required.items()}
        if self.optional is not None:
            specified |= {key: schema.validate(v[key]) for key, schema in self.optional.items() if key in v}
        if unspecified_keys and self.values is not None:
            return specified | {key: self.values.validate(v[key]) for key in unspecified_keys}
        return specified

@dataclass
class ListOrSingle(Schema):
    '''Accepts either a sequence where each item is accepted by ``item`` or a non-sequence value that is accepted by ``item``. Always produces a ``list``, regardless.

    :param item: the schema used for either the sequence items or the non-sequence value.'''

    item: Schema

    def validate(self, node: Node) -> Any:
        if node.kind == 'sequence':
            return [self.item.validate(item) for item in node.children]
        return [self.item.validate(node)]

@dataclass
class CommaSeparated(Schema):
    '''Accepts a scalar, splits it on commas. Produces a ``list``.

    :param item: schema that should accept a scalar for the substrings.
    '''

    item: Schema

    def validate(self, node: Node) -> Any:
        node.require_scalar()
        return [self.item.validate(ScalarNode(node.location, item)) for item in node.value.split(',')]

@dataclass
class Accept(Schema):
    '''Accepts any value and produces it unchanged.'''

    def validate(self, node: Node) -> Any:
        if node.kind == 'scalar':
            return node.value
        elif node.kind == 'sequence':
            return [self.validate(item) for item in node.children]
        elif node.kind == 'mapping':
            return {key: self.validate(value) for key, value in node.children.items()}
        assert False  # unreachable
