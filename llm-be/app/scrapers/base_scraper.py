from playwright.async_api import async_playwright


def playwright(func):
    async def inner(*args, **kwargs):
        async with async_playwright() as playwright:
            return await func(playwright=playwright, *args, **kwargs)

    return inner
