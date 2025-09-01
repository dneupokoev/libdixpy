import asyncio
from libdixpy import uuid_gen

def test_sync_generation():
    uid = uuid_gen.generate(_sync=True)
    assert isinstance(uid, int)
    assert len(str(uid)) == 18

async def test_async_generation():
    uid = await uuid_gen.generate()
    assert isinstance(uid, int)
    assert len(str(uid)) == 18