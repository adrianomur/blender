import builtins
import typing
import inspect

class _MISSING_TYPE:
    pass
MISSING = _MISSING_TYPE()

def _set_qualname(cls, value):
    # Ensure that the functions returned from _create_fn uses the proper
    # __qualname__ (the class they belong to).
    if inspect.isfunction(value):
        value.__qualname__ = f"{cls.__qualname__}.{value.__name__}"
    return value

def set_new_attribute(cls, name, value):
    # Never overwrites an existing attribute.  Returns True if the
    # attribute already exists.
    if name in cls.__dict__:
        return True
    _set_qualname(cls, value)
    setattr(cls, name, value)
    return False

def create_function(name: str, args: list[str], body: list[str], *, globals=None, locals=None,
               return_type=MISSING):
    # Note that we mutate locals when exec() is called.  Caller
    # beware!  The only callers are internal to this module, so no
    # worries about external callers.
    if locals is None:
        locals = {}
    if 'BUILTINS' not in locals:
        locals['BUILTINS'] = builtins
    return_annotation = ''
    if return_type is not MISSING:
        locals['_return_type'] = return_type
        return_annotation = '->_return_type'
    args = ','.join(args)
    body = '\n'.join(f'  {b}' for b in body)

    # Compute the text of the entire function.
    txt = f' def {name}({args}){return_annotation}:\n{body}'

    local_vars = ', '.join(locals.keys())
    txt = f"def __create_fn__({local_vars}):\n{txt}\n return {name}"
    ns = {}
    exec(txt, globals, ns)
    return ns['__create_fn__'](**locals)

def create_init():

    init_params = [
        'number: float',
        'name: str'
    ]

    body_lines = [
        'self.number = number',
        'self.name = name'
    ] 

    return create_function(
        name='__init__',
        args = ['self'] + init_params,
        body = body_lines,
        return_type=None)