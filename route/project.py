from fastapi_utils.inferring_router import InferringRouter

# from tortoise.query_utils import Q
from fastapi.exceptions import HTTPException
from fastapi_utils.cbv import cbv
from fastapi import Request
from model import Project

from os import urandom

# from app.ratelimit import global_limiter

router = InferringRouter()


@cbv(router)
class Project:
    @router.post("/project")
    async def new_project(self, request: Request):
        data = await request.json()

        await Project.create(
            id=urandom(15).hex(), name=data.name, description=data.description
        )
        return {"data": {"name": data.name, "description": data.description}}

    #router.get("/project/{project_id}")

    @router.get("/project/{project_id}")
    async def get_project(self, project_id: str):
        if not Project.exists(id=project_id):
            return HTTPException(status_code=404, detail="project not found")
        source = await Project.get(id=project_id)
        return {
            "data": {
                "name": source.name,
                "description": source.description,
                "author": source.author.name,
                "author_id": source.author.id,
                "project_type": source.project_type,
                "created_at": source.timestamp,
                "reactions": source.reactions,
            }
        }

    @router.get("/project/search/{keyword}")
    async def search_project(self, keyword: str):
        results = (
            await Project.filter(
                Q(name__icontains=keyword, description__icontains=keyword)
            )
            .order_by("timestamp")
            .all()
        )
        return {"data": results}


# await Project.create(id='', name='', ...) #이거 save같은건 안해도 되나요 네 틀린거 있으면 제가 중간중간 수정해드릴게요
# await Project.get(id='')
# await Project.exist(id='') -> 'return bool'
# # 작품 검색
# keyword = 'tst'
# results = await Project.filter(Q(name__icontains=keyword, description__icontains=keyword)).order_by("timestamp").all()
