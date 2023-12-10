# Explicit namespace package, required by maturin.
# Compatible with implicit namespaces, see PEP 420.
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
