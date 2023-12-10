from simpleworkspace.__lazyimporter__ import __LazyImporter__
if(__LazyImporter__.TYPE_CHECKING):
    from . import observables as _observables
observables: '_observables' = __LazyImporter__(__package__, '.observables')