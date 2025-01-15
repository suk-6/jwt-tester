import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from uuid import uuid4
from datetime import datetime, timedelta, timezone

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def makeJWT(second, data):
    return {
        "access": jwt.encode(
            data
            | {
                "type": "access",
                "exp": datetime.now(timezone.utc) + timedelta(seconds=second),
            },
            "secret",
            algorithm="HS256",
        ),
        "refresh": jwt.encode(
            data
            | {
                "type": "refresh",
                "exp": datetime.now(timezone.utc) + timedelta(days=365),
            },
            "secret",
            algorithm="HS256",
        ),
    }


@app.get("/token")
async def get_token(second: int = 20):
    return makeJWT(
        second,
        {
            "id": str(uuid4()),
            "name": "ㅎㅇ요",
            "age": "20",
            "job": "개발자",
            "region": "서울",
        },
    )


@app.get("/refresh")
async def refresh_token(refreshToken: str, second: int = 20):
    try:
        data = jwt.decode(refreshToken, "secret", algorithms=["HS256"])
        if data["type"] == "refresh":
            return makeJWT(
                second,
                {
                    "id": data["id"],
                    "name": data["name"],
                    "age": data["age"],
                    "job": data["job"],
                    "region": data["region"],
                },
            )
        else:
            raise Exception("Invalid token")
    except Exception as e:
        return {"error": str(e)}


@app.get("/info")
async def get_info(accessToken: str, key: str = "id"):
    """key: id, name, age, job, region"""
    try:
        data = jwt.decode(accessToken, "secret", algorithms=["HS256"])
        if data["type"] == "access":
            return {key: data[key]}
        else:
            raise Exception("Invalid token")
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
