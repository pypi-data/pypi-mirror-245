from dataclasses import dataclass
from typing import Any, Optional, Union

from bgpy.enums import ASGroups, Plane, Outcomes
from bgpy.caida_collector.graph.base_as import AS


@dataclass(frozen=True, slots=True)
class MetricKey:
    """Key for storing data within each metric"""

    plane: Plane
    as_group: ASGroups
    outcome: Outcomes
    ASCls: Union[Optional[type[AS]], Any] = None
