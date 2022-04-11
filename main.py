from dao.user_dao import UserDao
from dao.request_dao import RequestDao

from sanic.response import text
from sanic.request import Request

from model.queue_model import WorkItem
from server import app
import asyncio


@app.listener('after_server_start')
def create_task_queue(app):
    UserDao().create_table()
    RequestDao().create_table()
    app.ctx.queue_pending = asyncio.PriorityQueue(maxsize=0)
    app.ctx.queue_executing = asyncio.Queue(maxsize=0)


async def limited_function(x: WorkItem):
    await asyncio.sleep(10)
    result = f'OUTPUT OF LIMITED FUNCTION for {x}'
    queue_object = await app.ctx.queue_executing.get()
    RequestDao().set_result_for_request(queue_object.request_id, result)


@app.listener('after_server_start')
async def monitor_queue(app):
    while True:
        if app.ctx.queue_executing.qsize() == 0:
            queue_object = await app.ctx.queue_pending.get()
            x = queue_object[1]
            await app.ctx.queue_executing.put(x)
            await limited_function(queue_object)


@app.route("/limited", methods=['POST'])
async def limited_endpoint(request):
    request_id = RequestDao().get_last_request() + 1
    return text(f"your job is submitted, Your request id is {request_id} "
                f"you can check the result of your request by going to"
                f" /check_status/<request_id>")


@app.route("/check_status/<request_id>")
async def check_status(request, request_id):
    status = RequestDao().get_status_of_request(request_id)
    if status == 'Finished':
        result = RequestDao().get_result_of_completed_request(request_id)
        return text(f'your request status is {status} and the result is {result}')
    return text(f'your request is {status}')


@app.middleware("request")
async def request_middleware(request: Request):
    if request.path == "/limited":
        job = request.json
        user_weight = 2
        user_id = UserDao().add(user_weight)
        request_id = RequestDao().add('Pending', 1)
        x = WorkItem(priority=user_weight, request_id=request_id, user_id=user_id, data=job)
        await queue_handler(user_weight, x)


async def queue_handler(user_weight, x):
    await app.ctx.queue_pending.put((user_weight, x))

