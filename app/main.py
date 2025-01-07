from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers

from app.modassembly.authentication.login_api import router
app.include_router(router)
from app.feature_flags.get_user_feature_flags import router
app.include_router(router)
from app.feature_flags.update_user_feature_flag import router
app.include_router(router)
from app.feature_flags.create_feature_flag import router
app.include_router(router)
from app.users.get_users import router
app.include_router(router)
from app.users.create_user import router
app.include_router(router)

# Database

from app.modassembly.database.sql.get_sql_session import Base, engine
Base.metadata.create_all(engine)
