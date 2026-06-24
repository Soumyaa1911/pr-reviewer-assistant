from app.ingestion.classifier import classify_chunk_complexity

samples = [
    ("simple function", "def greet(name):\n    return f'Hello {name}'"),
    ("complex class", """class AsyncHTMLSession(BaseSession):
    def __init__(self, loop=None, workers=None, mock_browser=True):
        super().__init__(*args, **kwargs)
        self.loop = loop or asyncio.get_event_loop()
        self.thread_pool = ThreadPoolExecutor(workers)
    
    async def run(self, *coros):
        tasks = [asyncio.ensure_future(coro()) for coro in coros]
        return await asyncio.gather(*tasks)
"""),
]

for name, code in samples:
    result = classify_chunk_complexity(code)
    print(f"{name}: {result}")