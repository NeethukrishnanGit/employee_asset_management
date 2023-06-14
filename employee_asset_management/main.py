from fastapi import FastAPI
from router.instrument import instrument_app
from router.audit_trial import audit_app
from router.user_info import user_app

app = FastAPI(title="Asset Management System")
app.include_router(instrument_app, tags=["instruments"], prefix="/instruments")
app.include_router(user_app, tags=["user_data"], prefix="/user_data")
app.include_router(audit_app, tags=["audit_trail_data"], prefix="/audit_trail_data")


@app.get("/")
def root():
    return {"message": "Hi welcome to Employee Asset Management"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
