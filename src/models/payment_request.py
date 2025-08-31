from dataclasses import dataclass
from typing import Literal, Optional, List, Dict, Any

@dataclass
class PaymentRequest:
    session_id: str
    amount: float
    method: Literal["CARD", "WALLET", "CASH", "LOYALTY"] = "CARD"
    currency: str = "ILS"
    lines: Optional[List[Dict[str, Any]]] = None
