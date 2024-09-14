from .db_config import AsyncSessionLocal


async def get_async_session():
    """
    Asynchronous generator function that returns an async session.
    Create a new async session for each request and close it after the request is finished.

    Yields:
        async_session: An async session object.

    Example Usage:
        ```
        async with get_async_session() as async_session:
            # Do something with async session
            pass
        ```
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
