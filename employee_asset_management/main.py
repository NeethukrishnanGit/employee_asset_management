from fastapi import FastAPI
from router.instrument import instrument_app
from router.audit_trial import audit_app

app = FastAPI()
app.include_router(instrument_app)
app.include_router(audit_app)


@app.get("/")
def root():
    return {"message": "Hi welcome to Employee Asset Management"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
