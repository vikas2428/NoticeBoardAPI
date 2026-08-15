import asyncio


async def process_notice(notice):
    """
    Simulate asynchronous processing of a notice.
    """

    await asyncio.sleep(0)

    return {
        "id": notice["id"],
        "title": notice["title"],
        "status": notice["status"],
        "processed": True
    }


async def process_notices_async(notices):
    """
    Process multiple notices concurrently using asyncio.
    """

    tasks = [
        process_notice(notice)
        for notice in notices
    ]

    return await asyncio.gather(*tasks)