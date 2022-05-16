import asyncio
from concurrent.futures.thread import ThreadPoolExecutor

from .bankinter import login as bankinter_login
from .business import login as business_login
from .n26 import login as n26_login


def run(args):

    executor = ThreadPoolExecutor(10)

    loop = asyncio.get_event_loop()

    if args.bankinter:
        loop.run_in_executor(executor, bankinter_login)
    if args.business:
        loop.run_in_executor(executor, business_login)
    if args.n26:
        loop.run_in_executor(executor, n26_login)

    loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop)))

    input("Logged in 🔓")
    loop.close()
    executor.shutdown()
