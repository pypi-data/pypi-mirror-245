# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pairlist']
install_requires = \
['numpy>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'pairlist',
    'version': '0.5.1.2',
    'description': 'Generate neighbor list for the particles in a periodic boundary cell.',
    'long_description': '# pairlist\nGenerates the pair list of atoms that are closer to each other than the\ngiven threshold under the periodic boundary conditions.\n\nversion 0.5.1.1\n\n## Usage\n\nSee `pairlist.h` for the function definition and `pairlist-test.c` for usage.\n\nPython API is served in pairlist.py. The API document is [here](https://vitroid.github.io/PairList/pairlist.html).\n\nTo find the neighbors in a face-centered cubic lattice of size 10x10x10 on a MacBook Air 2021 (Apple Silicon),\n\n```shell\n$ python benchmark.py\nINFO crude: Neighboring pair list by a crude double loop.\nINFO crude: 18024 ms\nINFO crude: end.\n24000 pairs\nINFO numpyish: Neighboring pair list by numpy fancy array.\nINFO numpyish: 741 ms\nINFO numpyish: end.\n24000.0 pairs\nINFO pairlist_py: Neighboring pair list by pairlist in pure python.\nINFO pairlist_py: 125 ms\nINFO pairlist_py: end.\n24000 pairs\nINFO pairlist_c: Neighboring pair list by pairlist in c.\nINFO pairlist_c: end.\nINFO pairlist_c: 16 ms\n24000 pairs\n```\n\n```python\nimport pairlist as pl\nfrom fcc import FaceCenteredCubic\nfrom logging import getLogger, basicConfig, INFO, DEBUG\nfrom decorator import timeit, banner\nimport numpy as np\nfrom pairlist import pairs_py, pairs2_py\n\n\nbasicConfig(level=INFO, format="%(levelname)s %(message)s")\nlogger = getLogger()\nlogger.debug("Debug mode.")\n\n\n@banner\n@timeit\ndef crude(lattice, cell, rc=1.1):\n    "Neighboring pair list by a crude double loop."\n    rc2 = rc**2\n    count = 0\n    for i in range(len(lattice)):\n        for j in range(i):\n            d = lattice[i] - lattice[j]\n            d -= np.floor(d + 0.5)\n            d = d @ cell\n            if d @ d < rc2:\n                count += 1\n    return count\n\n\n@banner\n@timeit\ndef numpyish(lattice, cell, rc=1.1):\n    "Neighboring pair list by numpy fancy array."\n    # cross-differences\n    M = lattice[:, None, :] - lattice[None, :, :]\n    # wrap\n    M -= np.floor(M + 0.5)\n    # in absolute coordinate\n    M = M @ cell\n    d = (M * M).sum(2)\n    return d[(d < rc**2) & (0 < d)].shape[0] / 2\n\n\n@banner\n@timeit\ndef pairlist_py(lattice, cell, rc=1.1):\n    "Neighboring pair list by pairlist in pure python."\n    count = 0\n    for i, j, d in pl.pairs_iter(\n        lattice, maxdist=rc, cell=cell, _engine=(pairs_py, pairs2_py)\n    ):\n        count += 1\n    return count\n\n\n@timeit\n@banner\ndef pairlist_c(lattice, cell, rc=1.1):\n    "Neighboring pair list by pairlist in c."\n    count = 0\n    for i, j, d in pl.pairs_iter(lattice, maxdist=rc, cell=cell):\n        count += 1\n    return count\n\n\nlattice, cell = FaceCenteredCubic(10)\n\nprint(crude(lattice, cell), "pairs")\nprint(numpyish(lattice, cell), "pairs")\nprint(pairlist_py(lattice, cell), "pairs")\nprint(pairlist_c(lattice, cell), "pairs")\n\n```\n\n![benchmark](https://github.com/vitroid/PairList/raw/master/benchmark/benchmark.png)\n\n## Algorithm\n\nA simple cell division algorithm is implemented.\n\n## Demo\n\nIt requires [GenIce](https://github.com/vitroid/GenIce) to make the test data.\n\n```shell\n% make test\n```\n\n## Requirements\n\n* python\n* numpy\n\n\n## Bugs\n\n',
    'author': 'vitroid',
    'author_email': 'vitroid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
