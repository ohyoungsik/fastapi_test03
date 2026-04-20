# main.py

from unittest import result
from urllib import request

from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db


app = FastAPI()

# jinja2 템플릿 객체 생성 (templates 파일들이 어디에 있는지 알려야함)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"forturnToday": "동쪽으로가면 귀인을 만나요."})


# get 방식 /post 요청 처리
@app.get("/post", response_class=HTMLResponse)
def getPosts(request: Request, db:Session = Depends(get_db)):
    # DB 에서 글목록을 가져오기 위한 sql 문 준비
    query = text("""
        SELECT num, writer, title, content, created_at
        FROM post
        ORDER BY num DESC
    """)
    # 글 목록을 얻어와서
    result = db.execute(query).fetchall()
    print('글목록:  ', result)
    # 응답하기
    return templates.TemplateResponse(
        request=request,
        name="post/list.html", # templates/post/list.html jinja2 를 해석한 결과를 응답
        context={
            "posts":result
        }
    )
    
@app.get("/post/new", response_class=HTMLResponse)
def postNewForm(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="post/new-form.html"
    )
    
@app.post("/post/new", response_class=HTMLResponse)
def postNew(request: Request, writer: str = Form(...), title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    query = text("""
                 
                 INSERT INTO post(writer, title, content)
                 VALUES (:writer, :title, :content)
    """)
    
    db.execute(query, {"writer": writer, "title": title, "content": content})
    db.commit()

    return RedirectResponse(url="/post", status_code=303)