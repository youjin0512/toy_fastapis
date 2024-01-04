from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request


router = APIRouter()

templates = Jinja2Templates(directory="templates/")

# 회원 가입 form    /users/form
@router.post("/form", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    await request.form()
    print(dict(await request.form()))
    return templates.TemplateResponse(name="users/inserts.html"
                                      , context={'request':request
                                                , 'first':5, 'second':6})

@router.get("/form", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    print(dict(request._query_params))
    return templates.TemplateResponse(name="users/inserts.html"
                                      , context={'request':request
                                                , 'first':5, 'second':6})

@router.post("/login", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    print(dict_form_data)
    return templates.TemplateResponse(name="users/login.html"
                                      , context={'request':request
                                                 , 'form_data' : dict_form_data
                                                 , 'first' : 'text'})

@router.get("/login", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    print(dict(request._query_params))
    return templates.TemplateResponse(name="users/login.html", context={'request':request})

# 회원 가입 /users/insert -> users/login.html
@router.get("/insert") # 펑션 호출 방식
async def insert(request:Request):
    print(dict(request._query_params))
    return templates.TemplateResponse(name="users/login.html", context={'request':request})

# 회원 리스트 /users/list -> users/list.html
@router.post("/list") # 펑션 호출 방식
async def list(request:Request):
    await request.form()
    print(dict(await request.form()))
    return templates.TemplateResponse(name="users/list.html", context={'request':request})

@router.get("/list") # 펑션 호출 방식
async def list(request:Request):
    print(dict(request._query_params))
    user_list = [
        {"id": 1, "name": "김철수", "email": "cheolsu@example.com"},
        {"id": 2, "name": "이영희", "email": "younghi@example.com"},
        {"id": 3, "name": "박지성", "email": "jiseong@example.com"},
        {"id": 4, "name": "김미나", "email": "mina@example.com"},
        {"id": 5, "name": "장현우", "email": "hyeonwoo@example.com"}
]
    # return templates.TemplateResponse(name="users/list.html"
    return templates.TemplateResponse(name="users/list_jinja.html"
                                      , context={'request':request
                                                 , 'users' : user_list })

# 회원 상세정보 /users/read -> users/reads.html
# Path parameters : /users/read/id or /users/read/uniqe_name
@router.get("/read/{object_id}") # 펑션 호출 방식
async def reads(request:Request, object_id):
    print(dict(request._query_params))
    return templates.TemplateResponse(name="users/reads.html", context={'request':request})

@router.post("/read/{object_id}") # 펑션 호출 방식
async def reads(request:Request, object_id):
    await request.form()
    print(dict(await request.form()))
    return templates.TemplateResponse(name="users/reads.html", context={'request':request})

# form_datas = await request.form()
    # dict(form_datas)

'''
[GET 방식에서 딕셔너리 형식으로 파라미터를 뽑아오는 과정]
    request._query_params
    # QueryParams('name=jisu&email=ohjisu320%40gmail.com')
    request._query_params._dict
    # {'name': 'jisu', 'email': 'ohjisu320@gmail.com'}
    dict(request._query_params)
    # {'name': 'jisu', 'email': 'ohjisu320@gmail.com'}
[POST 방식에서 딕셔너리 형식으로 formdata를 뽑아오는 과정]
    request._query_params
    # post 방식은 parameter에 정보를 불러오지 않기에 작동되지 않음
    # QueryParams('')
    await request.form()
    # FormData([('name', 'jisu'), ('email', 'ohjisu320@gmail.com')])
    dict(await request.form())
    # {'name': 'jisu', 'email': 'ohjisu320@gmail.com'}
'''