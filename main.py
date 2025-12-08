from fastapi import FastAPI 
from db.database import Base , engine
from router.user_router import router as user_router
from router.booking_router import router as booking_router
from router.location_router import router as location_router
from router.payment_router import router as payment_router
from router.service_router import router as service_router 


Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(booking_router)
app.include_router(payment_router)
app.include_router(service_router)
app.include_router(location_router)