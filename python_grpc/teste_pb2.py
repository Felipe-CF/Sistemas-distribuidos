
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'teste.proto'
)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bteste.proto\x12\x08saudando\"\x19\n\tOiRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1e\n\nOiResposta\x12\x10\n\x08mensagem\x18\x01 \x01(\t2?\n\x07\x44\x61ndoOi\x12\x34\n\x07\x46\x61lando\x12\x13.saudando.OiRequest\x1a\x14.saudando.OiRespostab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'teste_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_OIREQUEST']._serialized_start=25
  _globals['_OIREQUEST']._serialized_end=50
  _globals['_OIRESPOSTA']._serialized_start=52
  _globals['_OIRESPOSTA']._serialized_end=82
  _globals['_DANDOOI']._serialized_start=84
  _globals['_DANDOOI']._serialized_end=147
