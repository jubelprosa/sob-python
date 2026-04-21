# Test Writer

## Konventionen
- **Framework:** pytest + pytest-asyncio
- **Naming:** `test_{module}_{function}_{scenario}`
- **HTTP Mocking:** httpx MockTransport

## Patterns
```python
import httpx
from sob import SobClient

def test_get_items():
    transport = httpx.MockTransport(lambda req: httpx.Response(200, json=[...]))
    client = SobClient(api_key="test", transport=transport)
    items = client.get_items()
    assert len(items) > 0
```

- Jeder Test testet EINE Sache
- Edge Cases: Auth-Fehler, Rate Limits, leere Responses, Pagination
- LangChain/LlamaIndex Integrationen separat testen
