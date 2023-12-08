from __future__ import annotations

from collections import deque
from copy import copy
from dataclasses import MISSING, fields
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum, EnumMeta
from ipaddress import IPv4Address, IPv4Interface, IPv4Network, IPv6Address, IPv6Interface, IPv6Network
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    DefaultDict,
    Deque,
    Dict,
    FrozenSet,
    Hashable,
    Iterable,
    List,
    Literal,
    Mapping,
    MutableMapping,
    MutableSequence,
    OrderedDict,
    Pattern,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
    get_origin,
)
from uuid import UUID

from msgspec import Struct
from msgspec.structs import fields as msgspec_struct_fields
from typing_extensions import NotRequired, Required, Self, get_args

from litestar._openapi.schema_generation.constrained_fields import (
    create_date_constrained_field_schema,
    create_numerical_constrained_field_schema,
    create_string_constrained_field_schema,
)
from litestar._openapi.schema_generation.utils import (
    _get_normalized_schema_key,
    _should_create_enum_schema,
    _should_create_literal_schema,
    _type_or_first_not_none_inner_type,
    get_formatted_examples,
)
from litestar.datastructures import UploadFile
from litestar.exceptions import ImproperlyConfiguredException
from litestar.openapi.spec import Reference
from litestar.openapi.spec.enums import OpenAPIFormat, OpenAPIType
from litestar.openapi.spec.schema import Schema, SchemaDataContainer
from litestar.pagination import ClassicPagination, CursorPagination, OffsetPagination
from litestar.params import BodyKwarg, ParameterKwarg
from litestar.plugins import OpenAPISchemaPlugin
from litestar.types import Empty
from litestar.types.builtin_types import NoneType
from litestar.typing import FieldDefinition
from litestar.utils.helpers import get_name
from litestar.utils.predicates import (
    is_class_and_subclass,
    is_optional_union,
    is_undefined_sentinel,
)
from litestar.utils.typing import (
    get_origin_or_inner_type,
    make_non_optional_union,
)

if TYPE_CHECKING:
    from msgspec.structs import FieldInfo

    from litestar._openapi.datastructures import OpenAPIContext
    from litestar.openapi.spec import Example
    from litestar.plugins import OpenAPISchemaPluginProtocol

KWARG_DEFINITION_ATTRIBUTE_TO_OPENAPI_PROPERTY_MAP: dict[str, str] = {
    "content_encoding": "content_encoding",
    "default": "default",
    "description": "description",
    "enum": "enum",
    "examples": "examples",
    "external_docs": "external_docs",
    "format": "format",
    "ge": "minimum",
    "gt": "exclusive_minimum",
    "le": "maximum",
    "lt": "exclusive_maximum",
    "max_items": "max_items",
    "max_length": "max_length",
    "min_items": "min_items",
    "min_length": "min_length",
    "multiple_of": "multiple_of",
    "pattern": "pattern",
    "title": "title",
    "read_only": "read_only",
}

TYPE_MAP: dict[type[Any] | None | Any, Schema] = {
    Decimal: Schema(type=OpenAPIType.NUMBER),
    DefaultDict: Schema(type=OpenAPIType.OBJECT),
    Deque: Schema(type=OpenAPIType.ARRAY),
    Dict: Schema(type=OpenAPIType.OBJECT),
    FrozenSet: Schema(type=OpenAPIType.ARRAY),
    IPv4Address: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.IPV4),
    IPv4Interface: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.IPV4),
    IPv4Network: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.IPV4),
    IPv6Address: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.IPV6),
    IPv6Interface: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.IPV6),
    IPv6Network: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.IPV6),
    Iterable: Schema(type=OpenAPIType.ARRAY),
    List: Schema(type=OpenAPIType.ARRAY),
    Mapping: Schema(type=OpenAPIType.OBJECT),
    MutableMapping: Schema(type=OpenAPIType.OBJECT),
    MutableSequence: Schema(type=OpenAPIType.ARRAY),
    None: Schema(type=OpenAPIType.NULL),
    NoneType: Schema(type=OpenAPIType.NULL),
    OrderedDict: Schema(type=OpenAPIType.OBJECT),
    Path: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.URI),
    Pattern: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.REGEX),
    Sequence: Schema(type=OpenAPIType.ARRAY),
    Set: Schema(type=OpenAPIType.ARRAY),
    Tuple: Schema(type=OpenAPIType.ARRAY),
    UUID: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.UUID, description="Any UUID string"),
    bool: Schema(type=OpenAPIType.BOOLEAN),
    bytearray: Schema(type=OpenAPIType.STRING),
    bytes: Schema(type=OpenAPIType.STRING),
    date: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.DATE),
    datetime: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.DATE_TIME),
    deque: Schema(type=OpenAPIType.ARRAY),
    dict: Schema(type=OpenAPIType.OBJECT),
    float: Schema(type=OpenAPIType.NUMBER),
    frozenset: Schema(type=OpenAPIType.ARRAY),
    int: Schema(type=OpenAPIType.INTEGER),
    list: Schema(type=OpenAPIType.ARRAY),
    set: Schema(type=OpenAPIType.ARRAY),
    str: Schema(type=OpenAPIType.STRING),
    time: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.DURATION),
    timedelta: Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.DURATION),
    tuple: Schema(type=OpenAPIType.ARRAY),
    UploadFile: Schema(
        type=OpenAPIType.STRING,
        content_media_type="application/octet-stream",
    ),
}


def _types_in_list(lst: list[Any]) -> list[OpenAPIType] | OpenAPIType:
    """Extract unique OpenAPITypes present in the values of a list.

    Args:
        lst: A list of values

    Returns:
        OpenAPIType in the given list. If more then one exists, return
        a list of OpenAPITypes.
    """
    schema_types: list[OpenAPIType] = []
    for item in lst:
        schema_type = TYPE_MAP[type(item)].type
        if isinstance(schema_type, OpenAPIType):
            schema_types.append(schema_type)
        elif schema_type is None:
            raise RuntimeError("Item in TYPE_MAP must have a type that is not None")
        else:
            schema_types.extend(schema_type)
    schema_types = list(set(schema_types))
    return schema_types[0] if len(schema_types) == 1 else schema_types


def _get_type_schema_name(field_definition: FieldDefinition) -> str:
    """Extract the schema name from a data container.

    Args:
        field_definition: A field definition instance.

    Returns:
        A string
    """

    if name := getattr(field_definition.annotation, "__schema_name__", None):
        return cast("str", name)

    name = get_name(field_definition.annotation)
    if field_definition.inner_types:
        inner_parts = ", ".join(_get_type_schema_name(t) for t in field_definition.inner_types)
        return f"{name}[{inner_parts}]"

    return name


def create_enum_schema(annotation: EnumMeta, include_null: bool = False) -> Schema:
    """Create a schema instance for an enum.

    Args:
        annotation: An enum.
        include_null: Whether to include null as a possible value.

    Returns:
        A schema instance.
    """
    enum_values: list[str | int | None] = [v.value for v in annotation]  # type: ignore
    if include_null and None not in enum_values:
        enum_values.append(None)
    return Schema(type=_types_in_list(enum_values), enum=enum_values)


def _iter_flat_literal_args(annotation: Any) -> Iterable[Any]:
    """Iterate over the flattened arguments of a Literal.

    Args:
        annotation: An Literal annotation.

    Yields:
        The flattened arguments of the Literal.
    """
    for arg in get_args(annotation):
        if get_origin_or_inner_type(arg) is Literal:
            yield from _iter_flat_literal_args(arg)
        else:
            yield arg.value if isinstance(arg, Enum) else arg


def create_literal_schema(annotation: Any, include_null: bool = False) -> Schema:
    """Create a schema instance for a Literal.

    Args:
        annotation: An Literal annotation.
        include_null: Whether to include null as a possible value.

    Returns:
        A schema instance.
    """
    args = list(_iter_flat_literal_args(annotation))
    if include_null and None not in args:
        args.append(None)
    schema = Schema(type=_types_in_list(args))
    if len(args) > 1:
        schema.enum = args
    else:
        schema.const = args[0]
    return schema


def create_schema_for_annotation(annotation: Any) -> Schema:
    """Get a schema from the type mapping - if possible.

    Args:
        annotation: A type annotation.

    Returns:
        A schema instance or None.
    """

    return copy(TYPE_MAP[annotation]) if annotation in TYPE_MAP else Schema()


class SchemaCreator:
    __slots__ = ("generate_examples", "plugins", "schemas", "prefer_alias", "dto_for")

    def __init__(
        self,
        generate_examples: bool = False,
        plugins: Iterable[OpenAPISchemaPluginProtocol] | None = None,
        schemas: dict[str, Schema] | None = None,
        prefer_alias: bool = True,
    ) -> None:
        """Instantiate a SchemaCreator.

        Args:
            generate_examples: Whether to generate examples if none are given.
            plugins: A list of plugins.
            schemas: A mapping of namespaces to schemas - this mapping is used in the OA components section.
            prefer_alias: Whether to prefer the alias name for the schema.
        """
        self.generate_examples = generate_examples
        self.plugins = plugins if plugins is not None else []
        self.schemas = schemas if schemas is not None else {}
        self.prefer_alias = prefer_alias

    @classmethod
    def from_openapi_context(cls, context: OpenAPIContext, prefer_alias: bool = True, **kwargs: Any) -> Self:
        kwargs.setdefault("generate_examples", context.openapi_config.create_examples)
        kwargs.setdefault("plugins", context.plugins)
        kwargs.setdefault("schemas", context.schemas)
        return cls(**kwargs, prefer_alias=prefer_alias)

    @property
    def not_generating_examples(self) -> SchemaCreator:
        """Return a SchemaCreator with generate_examples set to False."""
        if not self.generate_examples:
            return self
        return type(self)(generate_examples=False, plugins=self.plugins, schemas=self.schemas, prefer_alias=False)

    def get_plugin_for(self, field_definition: FieldDefinition) -> OpenAPISchemaPluginProtocol | None:
        return next(
            (plugin for plugin in self.plugins if plugin.is_plugin_supported_type(field_definition.annotation)), None
        )

    def is_constrained_field(self, field_definition: FieldDefinition) -> bool:
        """Return if the field is constrained, taking into account constraints defined by plugins"""
        return (
            isinstance(field_definition.kwarg_definition, (ParameterKwarg, BodyKwarg))
            and field_definition.kwarg_definition.is_constrained
        ) or any(
            p.is_constrained_field(field_definition)
            for p in self.plugins
            if isinstance(p, OpenAPISchemaPlugin) and p.is_plugin_supported_type(field_definition.annotation)
        )

    def is_undefined(self, value: Any) -> bool:
        """Return if the field is undefined, taking into account undefined types defined by plugins"""
        return is_undefined_sentinel(value) or any(
            p.is_undefined_sentinel(value) for p in self.plugins if isinstance(p, OpenAPISchemaPlugin)
        )

    def for_field_definition(self, field_definition: FieldDefinition) -> Schema | Reference:
        """Create a Schema for a given FieldDefinition.

        Args:
            field_definition: A signature field instance.

        Returns:
            A schema instance.
        """

        result: Schema | Reference

        if plugin_for_annotation := self.get_plugin_for(field_definition):
            result = self.for_plugin(field_definition, plugin_for_annotation)
        elif _should_create_enum_schema(field_definition):
            annotation = _type_or_first_not_none_inner_type(field_definition)
            result = create_enum_schema(annotation, include_null=field_definition.is_optional)
        elif _should_create_literal_schema(field_definition):
            annotation = (
                make_non_optional_union(field_definition.annotation)
                if field_definition.is_optional
                else field_definition.annotation
            )
            result = create_literal_schema(annotation, include_null=field_definition.is_optional)
        elif field_definition.is_optional:
            result = self.for_optional_field(field_definition)
        elif field_definition.is_union:
            result = self.for_union_field(field_definition)
        elif field_definition.origin in (CursorPagination, OffsetPagination, ClassicPagination):
            # NOTE: The check for whether the field_definition.annotation is a Pagination type
            # has to come before the `is_dataclass_check` since the Pagination classes are dataclasses,
            # but we want to handle them differently from how dataclasses are normally handled.
            result = self.for_builtin_generics(field_definition)
        elif field_definition.is_type_var:
            result = self.for_typevar()
        elif field_definition.is_subclass_of(Struct):
            result = self.for_struct_class(field_definition)
        elif field_definition.is_dataclass_type:
            result = self.for_dataclass(field_definition)
        elif field_definition.is_typeddict_type:
            result = self.for_typed_dict(field_definition)
        elif self.is_constrained_field(field_definition):
            result = self.for_constrained_field(field_definition)
        elif field_definition.inner_types and not field_definition.is_generic:
            result = self.for_object_type(field_definition)
        else:
            result = create_schema_for_annotation(field_definition.annotation)

        return self.process_schema_result(field_definition, result) if isinstance(result, Schema) else result

    def for_typevar(self) -> Schema:
        """Create a schema for a TypeVar.

        Returns:
            A schema instance.
        """

        return Schema(type=OpenAPIType.OBJECT)

    def for_optional_field(self, field_definition: FieldDefinition) -> Schema:
        """Create a Schema for an optional FieldDefinition.

        Args:
            field_definition: A signature field instance.

        Returns:
            A schema instance.
        """
        schema_or_reference = self.for_field_definition(
            FieldDefinition.from_kwarg(
                annotation=make_non_optional_union(field_definition.annotation),
                name=field_definition.name,
                default=field_definition.default,
            )
        )
        if isinstance(schema_or_reference, Schema) and isinstance(schema_or_reference.one_of, list):
            result = schema_or_reference.one_of
        else:
            result = [schema_or_reference]

        return Schema(one_of=[Schema(type=OpenAPIType.NULL), *result])

    def for_union_field(self, field_definition: FieldDefinition) -> Schema:
        """Create a Schema for a union FieldDefinition.

        Args:
            field_definition: A signature field instance.

        Returns:
            A schema instance.
        """
        inner_types = (f for f in (field_definition.inner_types or []) if not self.is_undefined(f.annotation))
        values = list(map(self.for_field_definition, inner_types))
        return Schema(one_of=values)

    def for_object_type(self, field_definition: FieldDefinition) -> Schema:
        """Create schema for object types (dict, Mapping, list, Sequence etc.) types.

        Args:
            field_definition: A signature field instance.

        Returns:
            A schema instance.
        """
        if field_definition.is_mapping:
            return Schema(
                type=OpenAPIType.OBJECT,
                additional_properties=(
                    self.for_field_definition(field_definition.inner_types[1])
                    if field_definition.inner_types and len(field_definition.inner_types) == 2
                    else None
                ),
            )

        if field_definition.is_non_string_sequence or field_definition.is_non_string_iterable:
            # filters out ellipsis from tuple[int, ...] type annotations
            inner_types = (f for f in field_definition.inner_types if f.annotation is not Ellipsis)
            items = list(map(self.for_field_definition, inner_types or ()))
            return Schema(
                type=OpenAPIType.ARRAY,
                items=Schema(one_of=items) if len(items) > 1 else items[0],
            )

        raise ImproperlyConfiguredException(
            f"Parameter '{field_definition.name}' with type '{field_definition.annotation}' could not be mapped to an Open API type. "
            f"This can occur if a user-defined generic type is resolved as a parameter. If '{field_definition.name}' should "
            "not be documented as a parameter, annotate it using the `Dependency` function, e.g., "
            f"`{field_definition.name}: ... = Dependency(...)`."
        )

    def for_builtin_generics(self, field_definition: FieldDefinition) -> Schema:
        """Handle builtin generic types.

        Args:
            field_definition: A signature field instance.

        Returns:
            A schema instance.
        """
        if field_definition.origin is ClassicPagination:
            return Schema(
                type=OpenAPIType.OBJECT,
                properties={
                    "items": Schema(
                        type=OpenAPIType.ARRAY,
                        items=self.for_field_definition(field_definition.inner_types[0]),
                    ),
                    "page_size": Schema(type=OpenAPIType.INTEGER, description="Number of items per page."),
                    "current_page": Schema(type=OpenAPIType.INTEGER, description="Current page number."),
                    "total_pages": Schema(type=OpenAPIType.INTEGER, description="Total number of pages."),
                },
            )

        if field_definition.origin is OffsetPagination:
            return Schema(
                type=OpenAPIType.OBJECT,
                properties={
                    "items": Schema(
                        type=OpenAPIType.ARRAY,
                        items=self.for_field_definition(field_definition.inner_types[0]),
                    ),
                    "limit": Schema(type=OpenAPIType.INTEGER, description="Maximal number of items to send."),
                    "offset": Schema(type=OpenAPIType.INTEGER, description="Offset from the beginning of the query."),
                    "total": Schema(type=OpenAPIType.INTEGER, description="Total number of items."),
                },
            )

        cursor_schema = self.not_generating_examples.for_field_definition(field_definition.inner_types[0])
        cursor_schema.description = "Unique ID, designating the last identifier in the given data set. This value can be used to request the 'next' batch of records."

        return Schema(
            type=OpenAPIType.OBJECT,
            properties={
                "items": Schema(
                    type=OpenAPIType.ARRAY,
                    items=self.for_field_definition(field_definition=field_definition.inner_types[1]),
                ),
                "cursor": cursor_schema,
                "results_per_page": Schema(type=OpenAPIType.INTEGER, description="Maximal number of items to send."),
            },
        )

    def for_plugin(self, field_definition: FieldDefinition, plugin: OpenAPISchemaPluginProtocol) -> Schema | Reference:
        """Create a schema using a plugin.

        Args:
            field_definition: A signature field instance.
            plugin: A plugin for the field type.

        Returns:
            A schema instance.
        """
        schema = plugin.to_openapi_schema(field_definition=field_definition, schema_creator=self)
        if isinstance(schema, SchemaDataContainer):
            return self.for_field_definition(
                FieldDefinition.from_kwarg(
                    annotation=schema.data_container,
                    name=field_definition.name,
                    default=field_definition.default,
                    extra=field_definition.extra,
                    kwarg_definition=field_definition.kwarg_definition,
                )
            )
        return schema  # pragma: no cover

    def for_struct_class(self, field_definition: FieldDefinition) -> Schema:
        """Create a schema object for a msgspec.Struct class.

        Args:
            field_definition: A field definition instance.

        Returns:
            A schema instance.
        """

        def _is_field_required(field: FieldInfo) -> bool:
            return field.required or field.default_factory is Empty

        unwrapped_annotation = field_definition.origin or field_definition.annotation
        type_hints = field_definition.get_type_hints(include_extras=True, resolve_generics=True)
        fields = msgspec_struct_fields(unwrapped_annotation)

        return Schema(
            required=sorted(
                [
                    field.encode_name
                    for field in fields
                    if _is_field_required(field=field) and not is_optional_union(type_hints[field.name])
                ]
            ),
            properties={
                field.encode_name: self.for_field_definition(
                    FieldDefinition.from_kwarg(type_hints[field.name], field.encode_name)
                )
                for field in fields
            },
            type=OpenAPIType.OBJECT,
            title=_get_type_schema_name(field_definition),
        )

    # noinspection PyDataclass
    def for_dataclass(self, field_definition: FieldDefinition) -> Schema:
        """Create a schema object for a dataclass class.

        Args:
            field_definition: A field definition instance.

        Returns:
            A schema instance.
        """

        unwrapped_annotation = field_definition.origin or field_definition.annotation
        type_hints = field_definition.get_type_hints(include_extras=True, resolve_generics=True)
        return Schema(
            required=sorted(
                [
                    field.name
                    for field in fields(unwrapped_annotation)
                    if (
                        field.default is MISSING
                        and field.default_factory is MISSING
                        and not is_optional_union(type_hints[field.name])
                    )
                ]
            ),
            properties={k: self.for_field_definition(FieldDefinition.from_kwarg(v, k)) for k, v in type_hints.items()},
            type=OpenAPIType.OBJECT,
            title=_get_type_schema_name(field_definition),
        )

    # noinspection PyTypedDict
    def for_typed_dict(self, field_definition: FieldDefinition) -> Schema:
        """Create a schema object for a typeddict.

        Args:
            field_definition: A field definition instance.

        Returns:
            A schema instance.
        """

        unwrapped_annotation = field_definition.origin or field_definition.annotation
        type_hints = field_definition.get_type_hints(include_extras=True, resolve_generics=True)

        return Schema(
            required=sorted(getattr(unwrapped_annotation, "__required_keys__", [])),
            properties={
                k: self.for_field_definition(FieldDefinition.from_kwarg(v, k))
                for k, v in {
                    k: get_args(v)[0] if get_origin(v) in (Required, NotRequired) else v for k, v in type_hints.items()
                }.items()
            },
            type=OpenAPIType.OBJECT,
            title=_get_type_schema_name(field_definition),
        )

    def for_constrained_field(self, field: FieldDefinition) -> Schema:
        """Create Schema for Pydantic Constrained fields (created using constr(), conint() and so forth, or by subclassing
        Constrained*)

        Args:
            field: A signature field instance.

        Returns:
            A schema instance.
        """
        kwarg_definition = cast(Union[ParameterKwarg, BodyKwarg], field.kwarg_definition)
        if any(is_class_and_subclass(field.annotation, t) for t in (int, float, Decimal)):
            return create_numerical_constrained_field_schema(field.annotation, kwarg_definition)
        if any(is_class_and_subclass(field.annotation, t) for t in (str, bytes)):  # type: ignore[arg-type]
            return create_string_constrained_field_schema(field.annotation, kwarg_definition)
        if any(is_class_and_subclass(field.annotation, t) for t in (date, datetime)):
            return create_date_constrained_field_schema(field.annotation, kwarg_definition)
        return self.for_collection_constrained_field(field)

    def for_collection_constrained_field(self, field_definition: FieldDefinition) -> Schema:
        """Create Schema from Constrained List/Set field.

        Args:
            field_definition: A signature field instance.

        Returns:
            A schema instance.
        """
        schema = Schema(type=OpenAPIType.ARRAY)
        kwarg_definition = cast(Union[ParameterKwarg, BodyKwarg], field_definition.kwarg_definition)
        if kwarg_definition.min_items:
            schema.min_items = kwarg_definition.min_items
        if kwarg_definition.max_items:
            schema.max_items = kwarg_definition.max_items
        if any(is_class_and_subclass(field_definition.annotation, t) for t in (set, frozenset)):  # type: ignore[arg-type]
            schema.unique_items = True

        item_creator = self.not_generating_examples
        if field_definition.inner_types:
            items = list(map(item_creator.for_field_definition, field_definition.inner_types))
            schema.items = Schema(one_of=items) if len(items) > 1 else items[0]
        else:
            schema.items = item_creator.for_field_definition(
                FieldDefinition.from_kwarg(
                    field_definition.annotation.item_type, f"{field_definition.annotation.__name__}Field"
                )
            )
        return schema

    def process_schema_result(self, field: FieldDefinition, schema: Schema) -> Schema | Reference:
        if field.kwarg_definition and field.is_const and field.has_default and schema.const is None:
            schema.const = field.default

        if field.kwarg_definition:
            for kwarg_definition_key, schema_key in KWARG_DEFINITION_ATTRIBUTE_TO_OPENAPI_PROPERTY_MAP.items():
                if (value := getattr(field.kwarg_definition, kwarg_definition_key, Empty)) and (
                    not isinstance(value, Hashable) or not self.is_undefined(value)
                ):
                    if schema_key == "examples":
                        value = get_formatted_examples(field, cast("list[Example]", value))

                    # we only want to transfer values from the `KwargDefinition` to `Schema` if the schema object
                    # doesn't already have a value for that property. For example, if a field is a constrained date,
                    # by this point, we have already set the `exclusive_minimum` and/or `exclusive_maximum` fields
                    # to floating point timestamp values on the schema object. However, the original `date` objects
                    # that define those constraints on `KwargDefinition` are still `date` objects. We don't want to
                    # overwrite them here.
                    if getattr(schema, schema_key, None) is None:
                        setattr(schema, schema_key, value)

        if not schema.examples and self.generate_examples:
            from litestar._openapi.schema_generation.examples import create_examples_for_field

            schema.examples = get_formatted_examples(field, create_examples_for_field(field))

        if schema.title and schema.type in (OpenAPIType.OBJECT, OpenAPIType.ARRAY):
            class_name = _get_normalized_schema_key(str(field.annotation))

            if class_name in self.schemas:
                return Reference(ref=f"#/components/schemas/{class_name}", description=schema.description)

            self.schemas[class_name] = schema
            return Reference(ref=f"#/components/schemas/{class_name}")
        return schema
