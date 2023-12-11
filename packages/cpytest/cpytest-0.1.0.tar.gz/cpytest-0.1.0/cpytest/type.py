"""cpycparser type wrapper classes as an interface between pycparser and cpygen.

The types (CpyType and CpyFunc) wrap typedef and function declarations in order to allow retrieving specific
information from them, and especially to add serialization for C and python stub code.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pycparser import c_ast
from pycparserext import ext_c_parser as c_ext

if TYPE_CHECKING:
    from cpytest.parse import CpyVisitor


def type_error(node: c_ast.Node) -> str:  # pragma: no cover
    return f"unexpected type {type(node)} [{node.coord if isinstance(node, c_ast.Node) else 'none'}]"


class Indent:
    def __init__(self, indent: int = 0) -> None:
        self._indent = indent

    def __add__(self, other: int) -> 'Indent':
        return Indent(self._indent + other)

    def __str__(self) -> str:
        return ' ' * self._indent


class CpyBase:
    @classmethod
    def id_type_str(cls, id_type: c_ast.IdentifierType) -> str:
        assert isinstance(id_type, c_ast.IdentifierType), type_error(id_type)
        return f"{' '.join(id_type.names)}".strip()

    @classmethod
    def type_str(cls, type_decl: c_ast.TypeDecl, indent: Indent, packed: bool = False) -> str:
        assert isinstance(type_decl, c_ast.TypeDecl), type_error(type_decl)
        if isinstance(type_decl.type, c_ast.IdentifierType):
            return cls.id_type_str(type_decl.type)
        if isinstance(type_decl.type, (c_ast.Struct, c_ast.Union)):
            return cls.struct_str(type_decl.type, indent, packed)
        if isinstance(type_decl.type, c_ast.Enum):
            return cls.enum_str(type_decl.type, indent)
        raise NotImplementedError(f"type_decl.type: {type(type_decl.type)} {type_decl.type.coord}")

    @classmethod
    def array_decl_str(cls, array_decl: c_ast.ArrayDecl, name_prefix: str = '') -> str:
        assert isinstance(array_decl, c_ast.ArrayDecl), type_error(array_decl)
        if isinstance(array_decl.type, c_ast.TypeDecl):
            type_str = cls.type_decl_str(array_decl.type, Indent(), name_prefix)
        elif isinstance(array_decl.type, c_ast.PtrDecl):
            type_str = cls.ptr_decl_str(array_decl.type, Indent(), name_prefix)
        else:
            raise NotImplementedError(f"array_decl.type: {type(array_decl.type)} {array_decl.type.coord}")
        dim_str = cls.value_str(array_decl.dim) if array_decl.dim else ""
        array_size_str = f"[{dim_str}]"
        return f"{type_str}{array_size_str}".strip()

    @classmethod
    def ptr_decl_str(cls, ptr_decl: c_ast.PtrDecl, indent: Indent, name_prefix: str = '') -> str:
        assert isinstance(ptr_decl, c_ast.PtrDecl), type_error(ptr_decl)
        if isinstance(ptr_decl.type, c_ast.TypeDecl):
            return cls.type_decl_str(ptr_decl, indent, name_prefix=name_prefix)
        if isinstance(ptr_decl.type, c_ext.FuncDeclExt):
            func_decl: c_ext.FuncDeclExt = ptr_decl.type
            param_str = cls.parameter_str(func_decl)
            if isinstance(func_decl.type, c_ast.TypeDecl):
                declname_str = f"{name_prefix}{func_decl.type.declname}"
                quals_str = ' '.join(set(ptr_decl.quals))
                quals_str = f"{quals_str} " if quals_str else ''
                type_str = cls.type_str(func_decl.type, indent)
            elif isinstance(func_decl.type, c_ast.PtrDecl):
                ptr_type_decl: c_ast.PtrDecl = func_decl.type
                declname_str = f"{name_prefix}{ptr_type_decl.type.declname}"
                type_str = cls.type_sign_str(ptr_type_decl, indent)
                quals_str = ""
            else:
                raise NotImplementedError(f"func_decl.type: {type(func_decl.type)} {func_decl.type.coord}")
            return f"{type_str} (*{quals_str}{declname_str})({param_str})"
        raise NotImplementedError(f"ptr_decl.type: {type(ptr_decl.type)} {ptr_decl.type.coord}")

    @classmethod
    def func_decl_str(cls, func_decl: c_ext.FuncDeclExt, indent: Indent, name_prefix: str = '') -> str:
        assert isinstance(func_decl, c_ext.FuncDeclExt), type_error(func_decl)
        param_str = cls.parameter_str(func_decl)
        if isinstance(func_decl.type, c_ast.TypeDecl):
            declname_str = f"{name_prefix}{func_decl.type.declname}"
            quals_str = ' '.join(set(func_decl.type.quals))
            quals_str = f" {quals_str} " if quals_str else ''
            type_str = cls.type_str(func_decl.type, indent)
        elif isinstance(func_decl.type, c_ast.PtrDecl):
            ptr_type_decl: c_ast.PtrDecl = func_decl.type
            declname_str = f"{name_prefix}{ptr_type_decl.type.declname}"
            type_str = cls.type_sign_str(ptr_type_decl, indent)
            quals_str = ""
        else:
            raise NotImplementedError(f"func_decl.type: {type(func_decl.type)} {func_decl.type.coord}")
        return f"{type_str} ({quals_str}{declname_str})({param_str})".strip()

    @classmethod
    def type_sign_str(cls, decl: c_ast.TypeDecl | c_ast.PtrDecl, indent: Indent, packed: bool = False) -> str:
        assert isinstance(decl, (c_ast.TypeDecl, c_ast.PtrDecl)), type_error(decl)

        if isinstance(decl, c_ast.TypeDecl):
            type_decl = decl
            ptr_str = ""
        elif isinstance(decl, c_ast.PtrDecl):
            ptr_decl: c_ast.PtrDecl = decl
            type_decl = ptr_decl.type
            ptr_quals_str = ' '.join(set(ptr_decl.quals))
            ptr_quals_str = f" {ptr_quals_str}" if ptr_quals_str else ''
            ptr_str = f"*{ptr_quals_str}"

        quals_str = ' '.join(set(type_decl.quals))
        quals_str = f"{quals_str} " if quals_str else ''
        type_str = cls.type_str(type_decl, indent, packed)

        return f"{quals_str}{type_str}{ptr_str}".strip()

    @classmethod
    def type_decl_str(
        cls, decl: c_ast.TypeDecl | c_ast.PtrDecl, indent: Indent, name_prefix: str = '', packed: bool = False
    ) -> str:
        assert isinstance(decl, (c_ast.TypeDecl, c_ast.PtrDecl)), type_error(decl)
        if isinstance(decl, c_ast.TypeDecl):
            type_decl = decl
        elif isinstance(decl, c_ast.PtrDecl):
            type_decl = decl.type

        type_sign_str = cls.type_sign_str(decl, indent, packed)
        declname_str = f" {name_prefix}{type_decl.declname}" if type_decl.declname else ''

        return f"{type_sign_str}{declname_str}".strip()

    @classmethod
    def decl_str(
        cls, decl: c_ast.Decl | c_ast.Typename | c_ext.FuncDeclExt, indent: Indent, name_prefix: str = ''
    ) -> str:
        assert isinstance(decl, (c_ast.Decl, c_ast.Typename, c_ext.FuncDeclExt)), type_error(decl)
        if isinstance(decl.type, c_ast.TypeDecl):
            return cls.type_decl_str(decl.type, indent, name_prefix)
        if isinstance(decl.type, c_ast.PtrDecl):
            return cls.ptr_decl_str(decl.type, indent, name_prefix)
        if isinstance(decl.type, c_ast.ArrayDecl):
            return cls.array_decl_str(decl.type, name_prefix)
        raise NotImplementedError(f"decl.type: {type(decl.type)} {decl.type.coord}")

    @classmethod
    def _is_void_type(cls, decl: c_ast.Decl | c_ast.Typename | c_ext.FuncDeclExt) -> bool:
        assert isinstance(decl, (c_ast.Decl, c_ast.Typename, c_ext.FuncDeclExt)), type_error(decl)
        if isinstance(decl.type, c_ast.TypeDecl):
            return cls.id_type_str(decl.type.type) == "void"
        return False

    @classmethod
    def parameter_str(cls, func_decl: c_ext.FuncDeclExt) -> str:
        param_list: c_ast.ParamList = func_decl.args
        if not param_list:
            return 'void'
        param_str_list = []
        for i, param in enumerate(param_list.params):
            param_name_str = "" if param.name is not None else f" arg{i}"
            if cls._is_void_type(param):
                param_str = "void"
            else:
                param_str = f"{cls.decl_str(param, Indent())}{param_name_str}"
            param_str_list.append(param_str)
        return ", ".join(param_str_list)

    @classmethod
    def storage_str(cls, node: c_ast.Typedef | c_ast.Decl) -> str:
        return ' '.join(node.storage).strip()

    @classmethod
    def value_str(cls, value: None | c_ast.Constant | c_ast.BinaryOp | c_ast.Cast | c_ast.ID) -> str | None:
        if not value:
            return None
        assert isinstance(value, (c_ast.Constant, c_ast.BinaryOp, c_ast.Cast, c_ast.ID)), type_error(value)
        if isinstance(value, c_ast.ID):
            return str(value.name)
        if isinstance(value, c_ast.Constant):
            return str(value.value).strip()
        if isinstance(value, c_ast.BinaryOp):
            binary_op: c_ast.BinaryOp = value
            return f"({cls.value_str(binary_op.left)} {binary_op.op} {cls.value_str(binary_op.right)})".strip()
        if isinstance(value, c_ast.Cast):
            cast: c_ast.Cast = value
            cast_to_str = cls.type_str(cast.to_type.type, Indent())
            expr_str = cls.value_str(cast.expr)
            # Note: casts are not supported in constant expressions by CFFI, so we're removing them and leave the
            #       cast expression as a comment. However, the See `test_enum_cast_initializer`
            # cast_str = f"({cast_to_str})"
            cast_str = f"/*({cast_to_str})*/"
            return f"{cast_str}{expr_str}".strip()
        raise NotImplementedError(f"enum: {type(value)} {value.coord}")

    @classmethod
    def enum_str(cls, enum: c_ast.Enum, indent: Indent) -> str:
        assert isinstance(enum, c_ast.Enum), type_error(enum)
        enum_tag = f" {enum.name}" if enum.name else ''
        enum_str = f"enum{enum_tag} {{\n"
        for enum_ in enum.values.enumerators:
            enum_value = cls.value_str(enum_.value)
            enum_value_str = f" = {enum_value}" if enum_value else ''
            enum_str += f"{indent + 4}{enum_.name}{enum_value_str},\n"
        enum_str += f"{indent}}}"
        return enum_str.strip()

    @classmethod
    def struct_str(cls, struct: c_ast.Struct | c_ast.Union, indent: Indent, packed: bool = False) -> str:
        assert isinstance(struct, (c_ast.Struct, c_ast.Union)), type_error(struct)
        struct_union = "struct" if isinstance(struct, c_ast.Struct) else "union"
        struct_tag = f" {struct.name}" if struct.name else ''
        struct_str = f"{struct_union}{struct_tag}"
        if struct.decls is not None:
            struct_str += " {\n"
            for member in struct.decls:  # type: c_ast.Decl
                member_type_decl_str = cls.decl_str(member, indent + 4)
                bitsize_str = ""
                if member.bitsize is not None:
                    bitsize_str = f" : {cls.value_str(member.bitsize)}"
                struct_str += f"{indent + 4}{member_type_decl_str}{bitsize_str};\n"
            if packed:
                struct_str += f"{indent + 4}...;  // Flexible field layout for packed struct or union\n"
            struct_str += f"{indent}}}"
        return struct_str.strip()

    @classmethod
    def typename_str(cls, decl: c_ast.TypeDecl | c_ast.PtrDecl, indent: Indent) -> str:
        assert isinstance(decl, (c_ast.TypeDecl, c_ast.PtrDecl)), type_error(decl)
        quals_str = ' '.join(set(decl.quals))
        quals_str = f"{quals_str} " if quals_str else ''
        if isinstance(decl, c_ast.PtrDecl):
            typename_str = cls.typename_str(decl.type, indent)
            return f"*{quals_str}{typename_str}"
        assert isinstance(decl, c_ast.TypeDecl), type_error(decl.type)
        assert decl.declname is not None
        return f"{decl.declname}".strip()

    @classmethod
    def add_unique_type_id(cls, id_types: list[c_ast.IdentifierType], id_type: c_ast.IdentifierType) -> None:
        """Helper function to add a type to a list of types, if it is not already in the list."""
        assert isinstance(id_type, c_ast.IdentifierType), type_error(id_type)
        for existing in id_types:
            assert isinstance(existing, c_ast.IdentifierType), type_error(existing)
            if existing.names == id_type.names:
                return
        id_types.append(id_type)


class CpyFunc(CpyBase):
    def __init__(self, decl: c_ast.Decl, types: list['CpyType']) -> None:
        assert isinstance(decl.type, c_ext.FuncDeclExt), type_error(decl.type)
        self._decl = decl
        self.types: list['CpyType'] = types

    @property
    def decl(self) -> c_ast.Decl:
        return self._decl

    def c_signature_str(self, name_prefix: str = '', storage: str = '') -> str:
        storage_str = storage or self.storage_str(self._decl)
        storage_str = f"{storage_str} " if storage_str else ''
        param_str = self.parameter_str(self._decl.type)
        type_decl_str = self.decl_str(self._decl.type, Indent(), name_prefix=name_prefix)
        return f"{storage_str}{type_decl_str}({param_str})"

    @dataclass
    class TypeMap:
        default: str | None
        c_types: list[str]

    py_c_type_map: dict[str, TypeMap] = {
        'bool': TypeMap(
            default="False",
            c_types=[
                '_Bool',
            ],
        ),
        'int': TypeMap(
            default="0",
            c_types=[
                'int',
                'long',
                'long long',
                'unsigned int',
                'unsigned long',
                'unsigned long long',
                'char',
                'unsigned char',
                'signed char',
                'short',
                'unsigned short',
                'unsigned',
            ],
        ),
        'float': TypeMap(
            default="0.0",
            c_types=[
                'float',
                'double',
                'long double',
            ],
        ),
        'None': TypeMap(
            default=None,
            c_types=[
                'void',
            ],
        ),
    }

    def _find_mapped_py_type(self, id_type: c_ast.IdentifierType) -> str | None:
        assert isinstance(id_type, c_ast.IdentifierType), type_error(id_type)
        c_type_name = self.id_type_str(id_type)
        for python_type, type_map in self.py_c_type_map.items():
            if c_type_name in type_map.c_types:
                return python_type
        return None

    def _get_python_type_name(self, id_type: c_ast.IdentifierType) -> str | None:
        """Return the python type for a given C type.

        The function first tries to find a matching python type in the `py_c_type_map`, using the c-type name.
        If no match is found, it tries to find a matching typedef in the ASTs list of types with a matching name.
        For enums and structs, the name of the type is returned. For ID types (typedefs), the function is called
        recursively, trying to determine a python type for the underlying type.
        """
        assert isinstance(id_type, c_ast.IdentifierType), type_error(id_type)

        python_type = self._find_mapped_py_type(id_type)
        if python_type is not None:
            return python_type

        c_type_name = self.id_type_str(id_type)
        for cpy_type in self.types:
            if cpy_type.typedef.name == c_type_name:
                if cpy_type.is_enum() or cpy_type.is_struct():
                    return str(cpy_type.typedef.name)
                if isinstance(cpy_type.typedef.type.type, c_ast.IdentifierType):
                    return self._get_python_type_name(cpy_type.typedef.type.type)
        return None

    def _py_find_default_value(self, id_type: c_ast.IdentifierType) -> str | None:
        """Determine a python value which can be used as a default value for the given C type.

        The search order for a default value for the type is as follows:
        - if a python type is found in the `py_c_type_map`, the default value for the python type is returned
        - otherwise, search for a matching typedef with the same c-type anme in the ASTs list of types
            - if the typedef is an enum, return the default value of that enum
            - if the typedef is a struct, return a new instance of that struct
            - if the typedef is another enum (ID type), call `_py_find_default_value()` recursively
        - return None if nothing is found
        """
        assert isinstance(id_type, c_ast.IdentifierType), type_error(id_type)

        python_type = self._find_mapped_py_type(id_type)
        if python_type is not None:
            return self.py_c_type_map[python_type].default

        c_type_name = self.id_type_str(id_type)
        for cpy_type in self.types:
            if cpy_type.typedef.name == c_type_name:
                if cpy_type.is_enum():
                    return f"lib.{cpy_type.get_enum_default()}"
                if cpy_type.is_struct():
                    return f"ffi.new('{cpy_type.typedef.name} *')[0]"
                if isinstance(cpy_type.typedef.type.type, c_ast.IdentifierType):
                    return self._py_find_default_value(cpy_type.typedef.type.type)
        return None

    def _py_default_type_value(  # pylint: disable=too-many-return-statements
        self, decl: c_ast.TypeDecl | c_ast.PtrDecl | c_ast.ArrayDecl
    ) -> str | None:
        """Determine a python value which can be used as a default value for the given C declarations type.

        The function returns a CFFI null pointer for pointer types, an empty list for array types.
        For type declarations, the default type is determined by calling `_py_find_default_value()`.
        """
        if isinstance(decl, c_ast.PtrDecl):
            return "ffi.NULL"

        if isinstance(decl, c_ast.ArrayDecl):
            return "[]"

        return self._py_find_default_value(decl.type)

    def py_default_return_str(self) -> str | None:
        """Return a python value which can be used as a default return value for this function.

        See `_py_default_type_value()` for details.
        """
        return self._py_default_type_value(self._decl.type.type)

    def _python_type_str(self, decl: c_ast.TypeDecl | c_ast.PtrDecl | c_ast.ArrayDecl) -> str | None:
        assert isinstance(decl, (c_ast.TypeDecl, c_ast.PtrDecl, c_ast.ArrayDecl)), type_error(decl)
        if isinstance(decl, c_ast.PtrDecl):
            return "CData"
        if isinstance(decl, c_ast.ArrayDecl):
            # FIXME: doesn't this need to recurse into _python_type_str()?
            return f"list[{self._get_python_type_name(decl.type.type)}]"
        return self._get_python_type_name(decl.type)

    def py_signature_str(self, name_prefix: str = '') -> str | None:
        name_str = f"{name_prefix}{self._decl.name}"
        param_str_list = []
        if self._decl.type.args is not None:
            for i, param in enumerate(self._decl.type.args.params):
                if not self._is_void_type(param):
                    param_name_str = param.name or f"arg{i}"
                    param_type_str = self._python_type_str(param.type)
                    param_type_str = f": {param_type_str}" if param_type_str else ""
                    param_str_list.append(f"{param_name_str}{param_type_str}")
        param_str = ', '.join(param_str_list)
        func_type = self._python_type_str(self._decl.type.type)
        func_type = f"{func_type}" if func_type else "Any"
        return f"def {name_str}({param_str}) -> {func_type}"

    def py_call_return_str(self, name_prefix: str = '') -> str:
        name_str = f"{name_prefix}{self._decl.name}"
        param_str_list = []
        if self._decl.type.args is not None:
            for i, param in enumerate(self._decl.type.args.params):
                if not self._is_void_type(param):
                    param_name_str = param.name or f"arg{i}"
                    param_str_list.append(param_name_str)
        func_call_str = f"{name_str}({', '.join(param_str_list)})"
        if self._is_void_type(self._decl.type):
            return func_call_str
        return f"return {func_call_str}"

    def py_call_default_str(self, name_prefix: str = '') -> str:
        name_str = f"{name_prefix}{self._decl.name}"
        arg_str_list: list[str] = []
        if self._decl.type.args is not None:
            for param in self._decl.type.args.params:
                if not self._is_void_type(param):
                    arg_str = self._py_default_type_value(param.type)
                    arg_str_list.append(arg_str or 'None')
        return f"{name_str}({', '.join(arg_str_list)})"

    def c_call_str(self, name_prefix: str = '') -> str:
        param_str_list = []
        if self._decl.type.args is not None:
            for i, param in enumerate(self._decl.type.args.params):
                if not self._is_void_type(param):
                    param_name_str = param.name or f"arg{i}"
                    param_str_list.append(param_name_str)
        return_str = "" if self._is_void_type(self._decl.type) else "return "
        return f"{return_str}{name_prefix}{self._decl.name}({', '.join(param_str_list)})"

    def _get_type(self, decl: c_ast.Decl | c_ast.Typename | c_ext.FuncDeclExt) -> c_ast.IdentifierType:
        assert isinstance(decl, (c_ast.Decl, c_ast.Typename, c_ext.FuncDeclExt)), type_error(decl)
        if isinstance(decl.type, c_ast.TypeDecl):
            return decl.type.type
        if isinstance(decl.type, c_ast.PtrDecl):
            return decl.type.type.type
        if isinstance(decl.type, c_ast.ArrayDecl):
            return decl.type.type.type
        raise NotImplementedError(f"decl.type: {type(decl.type)} {decl.type.coord}")

    def get_all_types(self) -> list[c_ast.IdentifierType]:
        """Return a list of all types that are used in the function declaration."""
        types: list[c_ast.IdentifierType] = []
        if self._decl.type.args is not None:
            for param in self._decl.type.args.params:
                if not self._is_void_type(param):
                    self.add_unique_type_id(types, self._get_type(param))
        if not self._is_void_type(self._decl.type):
            self.add_unique_type_id(types, self._get_type(self._decl.type))
        return types


class CpyFuncDef(CpyFunc):
    """Cpytest wrapper class for AST function definitions.

    The wrapper is used to find all external function calls in the function body and transitive external function calls.

    In order to search for external function calls, the wrapper uses a back reference to the visitor (`CpyVisitor`),
    which holds the global AST of all parsed files.
    """

    def __init__(self, func_def: c_ast.FuncDef, types: list['CpyType'], visitor: 'CpyVisitor') -> None:
        assert isinstance(func_def, c_ast.FuncDef), type_error(func_def)
        assert isinstance(func_def.decl, c_ast.Decl), type_error(func_def.decl)
        assert isinstance(func_def.decl.type, c_ext.FuncDeclExt), type_error(func_def.decl.type)
        super().__init__(func_def.decl, types)
        self._func_def = func_def
        self._visitor = visitor

    def get_called_func_decls(self) -> list[CpyFunc]:
        """Return a list of all function calls in the function body."""
        visitor = _ExternalFuncCallVisitor(self._visitor, self)
        visitor.visit(self._func_def)
        return visitor.func_decls


class _ExternalFuncCallVisitor(c_ast.NodeVisitor):  # type: ignore[misc]
    """A parser AST visitor, which recursively collects external function calls.

    The visitor has a reference to the global `parser`, from which it determins whether a found function call has a
    definition in the global AST (local function call), or not (external function call). External function calls are
    collected in a list of function declarations. Local function calls are recursively visited, using the same visitor,
    to search for transitive external function calls.
    """

    def __init__(self, parser: 'CpyVisitor', parent_cpy_func: 'CpyFuncDef') -> None:
        self._cpy_funcs: list[CpyFunc] = []
        self._parser = parser
        self._parent_cpy_func = parent_cpy_func

    @property
    def func_decls(self) -> list[CpyFunc]:
        return self._cpy_funcs

    def _add_func(self, func_decl: c_ast.FuncDecl) -> None:
        for existing in self._cpy_funcs:
            if existing.decl.name == func_decl.name:
                return
        self._cpy_funcs.append(CpyFunc(func_decl, self._parent_cpy_func.types))

    def visit_FuncCall(self, func_call: c_ast.FuncCall) -> None:  # pylint: disable=invalid-name
        func_def = self._parser.find_definition_for_func_name(func_call.name.name)
        if func_def is not None:
            self.visit(func_def)
        else:
            # found no definition for call: add declaration of call to list
            func_decl = self._parser.find_declaration_for_func_name(func_call.name.name)
            if func_decl is not None:
                # found a declaration for call: add to list
                self._add_func(func_decl)
        self.generic_visit(func_call)


class Typeref:
    def __init__(
        self, typedef: c_ast.Typedef, reference: c_ast.Typedef | None = None, pack_level: int | None = None
    ) -> None:
        """A typedef wraps a c_ast.Typedef with a packing level and a reference to another typedef.

        The packing level is the current stack packing level when the typedef was found. It determins whether
        currently packing is active (none-None) or not. That is later used for cffi specific serialization of
        packed structs or unions.

        The reference is the typedef that is referenced by this typedef. A referenced typedef is the original
        typedef, which was already found when this typedef was found. This is the case when multiple aliaes have
        been defined in a single typedef statement, such as "typedef struct {} a, b, c;". For the pycparser AST,
        these are individual typedefs, but in order to serialize them back to C code, they need to know that they
        are derived from a single type declaration. The reference is that single definition. A serialization of the
        above example would then be "typedef struct {} a; typedef a b; typedef a c;".
        """
        assert isinstance(typedef, c_ast.Typedef), type_error(typedef)
        self._typedef = typedef
        self._reference = reference
        self._pack_level = pack_level

    @property
    def typedef(self) -> c_ast.Typedef:
        return self._typedef

    @property
    def reference(self) -> c_ast.Typedef | None:
        return self._reference

    @classmethod
    def get_typedefed_decl(
        cls, typedef: c_ast.Typedef
    ) -> c_ast.Enum | c_ast.Struct | c_ast.Union | c_ast.IdentifierType:
        """Return the declaration which the given typedef is aliasing."""
        assert isinstance(typedef, c_ast.Typedef), type_error(typedef)
        if isinstance(typedef.type, c_ast.TypeDecl):
            return typedef.type.type
        if isinstance(typedef.type, c_ast.PtrDecl):
            return typedef.type.type.type
        if isinstance(typedef.type, c_ast.ArrayDecl):
            return typedef.type.type.type
        if isinstance(typedef.type, c_ext.FuncDeclExt):
            return typedef.type.type
        raise NotImplementedError(f"typedef.type: {type(typedef.type)} {typedef.type.coord}")


class CpyType(CpyBase):
    def __init__(self, typeref: Typeref) -> None:
        assert isinstance(typeref, Typeref), type_error(typeref)
        assert isinstance(
            typeref.typedef.type, (c_ast.TypeDecl, c_ast.PtrDecl, c_ast.ArrayDecl, c_ext.FuncDeclExt)
        ), type_error(typeref.typedef.type)
        self._typeref: Typeref = typeref
        self._typedef: c_ast.Typedef = typeref.typedef
        self._packed: bool = typeref._pack_level is not None

    @property
    def typedef(self) -> c_ast.Typedef:
        return self._typedef

    def is_enum(self) -> bool:
        assert isinstance(self._typedef, c_ast.Typedef), type_error(self._typedef)
        return isinstance(self._typedef.type.type, c_ast.Enum)

    def is_struct(self) -> bool:
        assert isinstance(self._typedef, c_ast.Typedef), type_error(self._typedef)
        return isinstance(self._typedef.type.type, c_ast.Struct)

    def get_enum_default(self) -> str:
        assert self.is_enum(), f"not an enum typedef: {self._typedef.type}"
        assert isinstance(self._typedef.type.type, c_ast.Enum), type_error(self._typedef.type)
        assert isinstance(self._typedef.type.type.values.enumerators[0].name, str)
        return self._typedef.type.type.values.enumerators[0].name

    def to_string(self) -> str:
        storage_str = self.storage_str(self._typedef)
        storage_str = f"{storage_str} " if storage_str else ''

        if self._typeref.reference is not None:
            assert isinstance(self._typeref.reference.type, c_ast.TypeDecl), type_error(self._typeref.reference.type)
            referenced_str = self._typeref.reference.type.declname
            typename_str = self.typename_str(self._typeref.typedef.type, Indent())
            type_decl_str = f"{referenced_str} {typename_str}"
        else:
            if isinstance(self._typedef.type, c_ast.TypeDecl):
                type_decl_str = self.type_decl_str(self._typedef.type, Indent(), packed=self._packed)
            elif isinstance(self._typedef.type, c_ast.PtrDecl):
                type_decl_str = self.ptr_decl_str(self._typedef.type, Indent())
            elif isinstance(self._typedef.type, c_ast.ArrayDecl):
                type_decl_str = self.array_decl_str(self._typedef.type)
            elif isinstance(self._typedef.type, c_ext.FuncDeclExt):
                type_decl_str = self.func_decl_str(self._typedef.type, Indent())
            else:
                raise NotImplementedError(f"self._typedef.type: {type(self._typedef.type)} {self._typedef.type.coord}")
        return f"{storage_str}{type_decl_str}"

    @classmethod
    def add_unique_type(cls, types: list['CpyType'], new_type: 'CpyType') -> None:
        for existing in types:
            if existing.typedef.name == new_type.typedef.name:
                return
        types.append(new_type)
