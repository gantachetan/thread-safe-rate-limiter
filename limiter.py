import time
import threading
from typing import Dict

class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.buckets: Dict[str, dict] = {}
        self.lock = threading.Lock()

    def _consume(self, client_id: str, tokens: int = 1) -> bool:
        with self.lock:
            now = time.time()
            if client_id not in self.buckets:
                self.buckets[client_id] = {"tokens": self.capacity, "last_updated": now}
            
            bucket = self.buckets[client_id]
            # Calculate how many tokens have naturally accumulated over time
            elapsed = now - bucket["last_updated"]
            refilled = elapsed * self.refill_rate
            
            bucket["tokens"] = min(self.capacity, bucket["tokens"] + refilled)
            bucket["last_updated"] = now
            
            if bucket["tokens"] >= tokens:
                bucket["tokens"] -= tokens
                return True
            return False

    def handle_request(self, client_id: str) -> str:
        if self._consume(client_id):
            return "🟩 HTTP 200: Request processed successfully."
        else:
            return "🟥 HTTP 429: Rate Limit Exceeded. Backing off..."

# --- TEST THE EXECUTION ---
if __name__ == "__main__":
    # Capacity = 3 requests max. Refills 1 token per second.
    limiter = TokenBucketLimiter(capacity=3, refill_rate_per_sec=1.0)
    user = "user_dev_88"

    print("--- Bursting 5 quick requests simultaneously ---")
    for i in range(5):
        print(f"Request {i+1}: {limiter.handle_request(user)}")
        time.sleep(0.1)

    print("\n⏳ Pausing for 2 seconds to let tokens naturally refill...")
    time.sleep(2)

    print("\n--- Sending new request after recovery ---")
    print(f"Request 6: {limiter.handle_request(user)}")