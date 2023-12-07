# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

@dataclass_json
@dataclass
class Forge:
    id: str
    label: str
    features: list[str] = field(default_factory=list)
    based_on: list[str] = field(default_factory=list)
    proprietary: bool = False
