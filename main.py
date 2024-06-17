from auth import auth
import schema.models as models
from auth import owner
import uvicorn
from schema.database import engine
from routers import shows, admin
from routers import users, test
from MW.midware import app
from MW.utils import args

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(owner.router)
app.include_router(admin.router)
app.include_router(shows.router)
app.include_router(users.router)
app.include_router(test.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(args.port))
