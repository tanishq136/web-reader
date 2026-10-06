from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl

from .webreader import WebReaderError, answer_question


class QuestionRequest(BaseModel):
    url: HttpUrl
    query: str = Field(min_length=1, max_length=1_000)


app = FastAPI(title="Web Reader API", version="1.0.0")

# The extension does not use cookies, so wildcard origins are safe here and avoid
# the invalid `allow_credentials=True` + `allow_origins=["*"]` combination.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/explain")
def explain(data: QuestionRequest) -> dict[str, str | int]:
    try:
        result = answer_question(str(data.url), data.query)
    except WebReaderError as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error
    return {"output": result.answer, "source_characters": result.source_characters}
