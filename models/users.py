from typing import Optional, List

from beanie import Document, Link   # beanie : 몽고db 연결하기 위한 패키지 모음, Document : 몽고db의 row
from pydantic import BaseModel, EmailStr

# 개발자 실수로 들어가는 field 제한
class User(Document):    # 아래 변수들은 init이 생략되어있음(실제로는 들어감)
    name: Optional[str] = None       # Optional : 넣어도 그만 안넣어도 그만
    email: Optional[EmailStr] = None # EmailStr : @와 . 안넣고 넣으면 안들어감
    pswd: Optional[str] = None
    manager: Optional[str] = None
    sellist1 : Optional[str] = None
    text : Optional[str] = None
    # class 만드는 이유 : 값이 들어갈 때 값의 원천적인 데이터 형태를 구분할 수 있게 하기 위해 만들어준다.        
    # Optional없이 str만 사용하면, 오류일 때 값을 뱉어낸다.
    class Settings:
        name = "users"
  