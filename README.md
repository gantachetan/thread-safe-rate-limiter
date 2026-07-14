Thread-Safe Rate Limiter

A high-performance, thread-safe network traffic controller utilizing a mathematical **Token Bucket** algorithm. Implements atomic concurrency guards to prevent race conditions during high-burst API requests.

---

 Architectural Overview

Unprotected backend APIs are highly susceptible to Denial of Service (DoS) attacks and massive cloud billing spikes. This traffic controller acts as a low-latency gateway layer directly in front of resource nodes.


---

 Engineering Principles

Mathematical Refill Architecture: Avoids CPU-heavy background cron-jobs. It calculates token depletion and replenishment passively on the fly using timestamps ($t_{\text{elapsed}} \times \text{Refill Rate}$), keeping CPU usage near zero.
Concurreny & Thread-Locking:Implements python's `threading.Lock` within bucket evaluation layers, securing critical state pathways against race conditions in multi-threaded API servers.
Structured Rate Auditing: Writes client request logs (`ALLOWED` or `BLOCKED`) to an auditable SQLite database, exposing real-time traffic spikes and malicious actors.

---

 Traffic Limit Performance Profile

Simulation running multiple concurrent connections from a single client user:

```text
--- Bursting 5 quick requests simultaneously ---
Request 1: 🟩 HTTP 200: Request processed successfully.
Request 2: 🟩 HTTP 200: Request processed successfully.
Request 3: 🟩 HTTP 200: Request processed successfully.
Request 4: 🟥 HTTP 429: Rate Limit Exceeded. Backing off...
Request 5: 🟥 HTTP 429: Rate Limit Exceeded. Backing off...

⏳ Pausing for 2 seconds to let tokens naturally refill...

--- Sending new request after recovery ---
Request 6: 🟩 HTTP 200: Request processed successfully.
