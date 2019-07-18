from clld.web.assets import environment
from clldutils.path import Path

import ldh


environment.append_path(
    Path(ldh.__file__).parent.joinpath('static').as_posix(),
    url='/ldh:static/')
environment.load_path = list(reversed(environment.load_path))
