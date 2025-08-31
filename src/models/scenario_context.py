from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal

@dataclass
class ScenarioContext:
    # restrict to only valid methods
    method: Literal["CARD", "WALLET", "CASH", "LOYALTY"] = "CARD"
    session_id: Optional[str] = None
    pump: int = 0

    liters: int = 0
    amount: float = 0.0

    cart: List[Dict[str, Any]] = field(default_factory=list)

    loyalty_points: int = 0

    payment_response: Optional[Dict[str, Any]] = None
