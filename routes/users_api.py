# * quest
# * 회원 관리
# /routes/users_api.py
# - document class : models.users.py
# - 회원가입(post : /), 로그인(get : /{id}/{pswd}), 회원탈퇴(delete : /{id})
# - option : 회원 수정(put : /{id})


from typing import List

from beanie import PydanticObjectId   # beanie : mongodb 연결 / PydanticObjectId : mongodb의 _id 불러오기
from databases.connections import Database  # databases 폴더에 connections 파일 연결, Database라는 class 불러오기
from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User   # User : models > users.py의 class User 연결(호출)

router = APIRouter(
    tags=["users"]
)

users_database = Database(User)

# 새로운 레코드 추가 (C)
# http://127.0.0.1:8000/events_api/new
# {
#         "creator": "이철수",
#         "title": "도시의 빛",
#         "image": "city_lights.jpg",
#         "description": "밤하늘을 수놓은 도시의 불빛과 번화가",
#         "tags": ["도시", "야경", "번화가", "불빛"],
#         "location": "명동, 서울"
#     }

# 회원가입 : id 생성[Create]
@router.post("/")    # post : 만들어서 전달
async def create_user(body: User) -> dict:
    document = await users_database.save(body)
    return {
        "message": "Users created successfully"
        ,"datas": document
    }

# mongodb에서 한 개의 행(row) 확인[Read]
@router.get("/{id}/{pswd}", response_model=User)  # method : get
async def retrieve_event(id: PydanticObjectId) -> User:
    get_id = await users_database.get(id)
    if not get_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users with supplied ID does not exist"
        )
    return get_id

# 회원탈퇴 : ID에 따른 row 삭제[Delete]
@router.delete("/{id}")     # method : delete
async def delete_event(id: PydanticObjectId) -> dict:
    users = await users_database.get(id)    # 해당 아이디가 맞는지(있는지) 확인
    if not users:   # 똑같은 아이디가 db에 없으면
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found"    # 해당 메시지를 postman에 출력
        )
    users = await users_database.delete(id)  # 똑같은 아이디가 db에 있으면 삭제

    return {
        "message": "Users deleted successfully."
        ,"datas": users
    }

# update(회원수정) with id[Update]
from fastapi import Request
@router.put("/{id}", response_model=User)
async def update_users_withjson(id: PydanticObjectId, request:Request) -> User:
    users = await users_database.get(id)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found"
        )
    body = await request.json()
    updated_users = await users_database.update_withjson(id, body)
    if not updated_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users with supplied ID does not exist"
        )
    return updated_users

# 전체 내용 가져오기
# @router.get("/", response_model=List[Event])
@router.get("/")
# async def retrieve_all_users() -> List[Event]:
async def retrieve_all_users() -> dict:
    users = await users_database.get_all()
    # return users
    return {"total_count":len(users)
            , 'datas':users}