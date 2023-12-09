from typeable import Object, field, JsonSchema
from typeable.typing import Union, Literal, Any

#
# OpenRPC v1.2.6
#

version = '1.2.6'


class Contact(Object):
    name: str
    url: str
    email: str


class License(Object):
    name: str = field(required=True)
    url: str


class Info(Object):
    title: str = field(required=True)
    description: str
    termsOfService: str
    contact: Contact
    license: License
    version: str = field(required=True)


class RuntimeExpression(Object):
    pass


class ServerVariable(Object):
    enum: list[str]
    default: str = field(required=True)
    description: str


class Server(Object):
    name: str = field(required=True)
    url: RuntimeExpression = field(required=True)
    summary: str
    description: str
    variables: dict[str, ServerVariable]


class ExternalDocs(Object):
    description: str
    url: str = field(required=True)


class Tag(Object):
    name: str
    sumary: str
    description: str
    externalDocs: ExternalDocs


class Reference(Object):
    ref: str = field(key='$ref', required=True)


class ContentDescriptor(Object):
    name: str = field(required=True)
    summary: str
    description: str
    required: bool = False
    schema: Union[JsonSchema, Reference] = field(required=True)
    deprecated: bool = False


class Error(Object):
    code: int = field(required=True)
    message: str = field(required=True)
    data: Any


class Link(Object):
    name: str
    description: str
    summary: str
    method: str
    params: dict[str, Union[RuntimeExpression, Any]]
    server: Server


class Example(Object):
    name: str
    summary: str
    description: str
    value: Any
    externalValue: str


class ExamplePairing(Object):
    name: str
    description: str
    summary: str
    params: list[Union[Example, Reference]]
    result: Union[Example, Reference]


class Method(Object):
    name: str = field(required=True)
    tags: list[Union[Tag, Reference]]
    summary: str
    description: str
    externalDocs: ExternalDocs
    params: list[Union[ContentDescriptor, Reference]] = field(required=True)
    result: Union[ContentDescriptor, Reference] = field(required=True)
    deprecated: bool = False
    servers: list[Server]
    errors: list[Union[Error, Reference]]
    links: list[Union[Link, Reference]]
    paramStructure: Literal['by-name', 'by-position', 'either']
    examples: list[ExamplePairing]


class Components(Object):
    contentDescriptors: dict[str, ContentDescriptor]
    schemas: dict[str, Union[JsonSchema, Reference]]
    examples: dict[str, Example]
    links: dict[str, Link]
    errors: dict[str, Error]
    examplePairingObjects: dict[str, ExamplePairing]
    tags: dict[str, Tag]


class Document(Object, jsonschema='https://raw.githubusercontent.com/open-rpc/meta-schema/master/schema.json'):
    openrpc: str = field(required=True)
    info: Info = field(required=True)
    servers: list[Server]  # TODO: default server
    methods: list[Union[Method, Reference]] = field(required=True)
    components: Components
    externalDocs: ExternalDocs
