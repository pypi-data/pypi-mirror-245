from .atlas import Atlas
from .hamburg import FTSDCAtlas, FTSAvrgAtlas
from .sss import SSSAtlas


def atlas_factory(name: str, lower_limit, upper_limit, conversion=1) -> Atlas:
    if name.lower() in ['fts', 'hhdc']:
        ref = FTSDCAtlas(lower_limit * conversion, upper_limit * conversion).load()
    elif name.lower() in ['hhavrg']:
        ref = FTSAvrgAtlas(lower_limit * conversion, upper_limit * conversion).load()
    elif name.lower() == 'sss':
        ref = SSSAtlas(lower_limit * conversion, upper_limit * conversion).load()
    else:
        raise NotImplementedError(f'Atlas {name} not known/implemented.')
    ref.convert_wl(1 / conversion)
    return ref
