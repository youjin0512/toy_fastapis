from typing import Any, List, Optional
from beanie import init_beanie, PydanticObjectId
from models.users import User
from models.toyteam import input_answer,toyteam

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
# 변경 후 코드
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DATABASE_URL: Optional[str] = None
    DATABASE_URL : Optional[str] = None
      # async-await == 네크워크의 속도와 맞추기 위해 넣는 기능(방식은 비동기)
    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[User])
        await init_beanie(database=client.get_default_database(),
                          document_models=[input_answer])
        await init_beanie(database=client.get_default_database(),
                          document_models=[toyteam])
    class Config:
        env_file = ".env"

class Database:
    # model 즉 collection
    def __init__(self, model) -> None:
        self.model = model
        pass
        # 전체 리스트
    async def get_all(self):
        documents = await self.model.find_all().to_list()
        pass
        return documents
    # 상세 보기
    async def get(self, id:PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False
    # 저장
    async def save(self, document) -> None:
        await document.create()
        return None