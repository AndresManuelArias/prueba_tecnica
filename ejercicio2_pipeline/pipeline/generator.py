import time
import random
from datetime import datetime, timezone
from typing import Generator, Dict, Any

def data_stream_generator(total_records: int = 100_000) -> Generator[Dict[str, Any], None, None]:

    event_types = ["click", "view", "purchase", "heartbeat", "error"]
    
    for i in range(total_records):

        timestamp = datetime.now(timezone.utc)
        
        event = {
            "id": i + 1,
            "event_type": random.choice(event_types),
            "value": round(random.uniform(10.0, 500.0), 2),
            "timestamp": timestamp,
            "metadata": {
                "environment": "production",
                "processed": False
            }
        }
        
        yield event
        