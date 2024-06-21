from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
import os
import uvicorn
from openai import OpenAI

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
api_key = os.getenv('OPENAI_API_KEY')

cred = credentials.Certificate("firebase_credential.json")
firebase_admin.initialize_app(cred)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)



class RecipeRequest(BaseModel):
    ingredients: list[str]
    tools: list[str]

class RecipeResponse(BaseModel):
    recipe: str

@app.get("/")
def read_root():
    return {"Status": "200 OK", "Purpose": "OS19", "Author": "Chanwoo"}

@app.post("/getrecipe")
async def getRecipeByGPT(request: RecipeRequest):
    prompt = f"""
    식재료: {', '.join(request.ingredients)}
    조리도구: {', '.join(request.tools)}
    위 식재료와 조리도구에 맞는 레시피를 다음 형식에 맞게 추천해줘. 형식을 반드시 지켜주세요:
    요리 이름: 까르보나라 스파게티
    요리 시간: 30분
    요리 난이도: 중간
    예상되는 재료비: 12,000원
    단계별 레시피:
    1. 스파게티를 삶습니다.
    2. 베이컨을 볶습니다.
    3. 계란과 치즈를 섞습니다.
    4. 모든 재료를 섞어 완성합니다.

    다음 형식을 꼭 따르세요:
    요리 이름: 
    요리 시간: 
    요리 난이도: 
    예상되는 재료비: 
    단계별 레시피:
    """

    try:
        response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-3.5-turbo",
            )
        recipe = response.choices[0].message.content.strip()
        return RecipeResponse(recipe=recipe)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8000 if PORT not set
    uvicorn.run(app, host="0.0.0.0", port=port)