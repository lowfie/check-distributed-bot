import asyncio

from celery.app.task import Task as Task


class AsyncTask(Task):
    async def run_async(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_async(*args, **kwargs))
