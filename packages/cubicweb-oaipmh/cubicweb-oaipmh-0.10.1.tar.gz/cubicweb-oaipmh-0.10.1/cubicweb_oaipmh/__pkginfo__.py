# pylint: disable=W0622
"""cubicweb-oaipmh application packaging information"""


modname = "cubicweb_oaipmh"
distname = "cubicweb-oaipmh"

numversion = (0, 10, 1)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "OAI-PMH server for CubicWeb"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname

__depends__ = {
    "cubicweb": ">= 3.38.0, < 3.39.0",
    "python-dateutil": None,
    "isodate": None,
    "pytz": None,
    "lxml": None,
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
