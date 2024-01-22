from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId   # beanie : DB 초기화
from models.users import User
from models.events import Event
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
# 변경 후 코드
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    
    async def initialize_database(self):   # async 사용 이유 : 네트워크 속도(sync : 동기화되어 움직임)
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),   # await : 기다림
                          document_models=[User, Event])
    class Config:
        env_file = ".env"

import json
class Database:
    # model은 즉, collection
    def __init__(self, model) -> None:
        self.model = model
        pass
    
    # 전체 리스트
    async def get_all(self) :
        documents = await self.model.find_all().to_list()   # find({})와 동일
        pass
        return documents
    
    # 상세 보기
    async def get(self, id: PydanticObjectId) -> Any:       # PydanticObjectId : mongoDB에서만 사용
        doc = await self.model.get(id)
        if doc:
            return doc
        return False
    # 값을 가져왔는데 그 값이 있으면 return, 없으면 false이라는 신호 보냄

    # 저장
    async def save(self, document) -> None:
        doc = await document.create()
        return doc
    
    async def delete(self, id: PydanticObjectId):
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
    
    # column 값으로 여러 Documents 가져오기
    async def getsbyconditions(self, conditions:dict) -> [Any]:
        documents = await self.model.find(conditions).to_list()  # find({})
        if documents:
            return documents
        return False

    # update with params json (U)
    async def update_withjson(self, id: PydanticObjectId, body: json):
        doc_id = id

        # des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {**body}}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc