from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

class toyteam(Document):
    question: Optional[str] = None
    options: Optional[list] = None
    answer: Optional[int] = None
    score: Optional[int] = None
  
    class toyteam_Settings:
        name = "toyteam"


class input_answer(Document):
    name:Optional[str] = None
    question1:Optional[int] = None
    question2:Optional[int] = None
    question3:Optional[int] = None
    question4:Optional[int] = None
    question5:Optional[int] = None
    count:Optional[int] = None
    score:Optional[int] = None


    class input_answer_Settings:
        name = 'input_answer'