# made by yohan except 문제리스트

from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from database.connections import Database
from models.toyteam import toyteam,input_answer
from beanie import PydanticObjectId

router = APIRouter()

templates = Jinja2Templates(directory="templates/")

collection_toyteam = Database(toyteam)
collection_input_answer = Database(input_answer)

# 문제 리스트
@router.get("/question_list", response_class=HTMLResponse) # 펑션 호출 방식
async def forms(request:Request):
    return templates.TemplateResponse(name="toyteam/question_list.html", context={'request':request})

@router.post("/question_list", response_class=HTMLResponse) # 펑션 호출 방식
async def forms(request:Request):
    return templates.TemplateResponse(name="toyteam/question_list.html", context={'request':request})


# 응시 결과
@router.get("/data_list", response_class=HTMLResponse) # 펑션 호출 방식
async def forms(request:Request):
    dict(request._query_params)
    
    answer_list = await collection_input_answer.get_all()
    answer_list = [answer.__dict__ for answer in answer_list]
    try:
        for answer in answer_list:
            answer.pop('id', None)
            answer.pop('revision_id', None)
        count=len(answer_list[0])-3
    except:
        answer_list=[
            {
                'name': None,
                'question1':None,
                'question2':None,
                'question3':None,
                'question4':None,
                'question5':None,
                'count':None,
                'score':None
            }
        ]
        count = None
        pass
    return templates.TemplateResponse(name="toyteam/data_list.html", context={'request':request,'answers':answer_list, 'question_counts':count})

@router.post("/data_list", response_class=HTMLResponse) # 펑션 호출 방식
async def forms(request:Request):
    form_data = await request.form()
    answer_dict = dict(form_data)


    quest_list = await collection_toyteam.get_all()
    quests_list = [answer.dict() for answer in quest_list]


   
    correct = 0
    score = 0
    answer_dict['count'] = correct
    answer_dict['score'] = score
    try:
        for j in range(len(answer_dict)-3):
            if int(answer_dict[f'question{j+1}']) == dict(quest_list[j])['answer']:
                correct +=1
                score += dict(quest_list[j])['score']
                pass
            answer_dict['count'] = correct
            answer_dict['score'] = score
        pass
    except:
        pass
    pass
    answer = input_answer(**answer_dict)
    await collection_input_answer.save(answer)

    answer_list = await collection_input_answer.get_all()
    answer_list = [answer.__dict__ for answer in answer_list]
    try:
        for answer in answer_list:
            answer.pop('id', None)
            answer.pop('revision_id', None)
        count=len(answer_list[0])-3
    except:
        answer_list=[
            {
                'name': None,
                'question1':None,
                'question2':None,
                'question3':None,
                'question4':None,
                'question5':None,
                'count':None,
                'score':None
            }
        ]
        count = None
        pass
    return templates.TemplateResponse(name="toyteam/data_list.html", context={'request':request,'answers':answer_list,'questions':quests_list, 'question_counts':count})


# 문제 풀기
@router.get("/exam_test", response_class=HTMLResponse) # 펑션 호출 방식
async def forms(request:Request):
    dict(request._query_params)
    
    question_list = await collection_toyteam.get_all()
    return templates.TemplateResponse(name="toyteam/exam_test.html", context={'request':request,'questions' : question_list})

@router.post("/exam_test", response_class=HTMLResponse) # 펑션 호출 방식
async def forms(request:Request):
    form_data = await request.form()
    question_dict = dict(form_data)

    # question_list = question(**question_dict)
    # await collection_user.save(user)

    question_list = await collection_toyteam.get_all()
    return templates.TemplateResponse(name="toyteam/exam_test.html", context={'request':request,'form_data':question_list})
