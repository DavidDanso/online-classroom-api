from fastapi import FastAPI
from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware
from .routers import courses, users, auth, course_enrollment, lessons, assignments

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Define a list of allowed origins, indicated by "*",
# which means any origin is permitted to access this application.
origins = ["*"]

# Add CORS (Cross-Origin Resource Sharing) middleware to the application.
# This middleware allows specified origins to access resources on this server.
# - allow_origins: List of origins allowed to access the server, in this case, any origin ("*").
# - allow_credentials: Indicates whether credentials like cookies can be sent in CORS requests (True).
# - allow_methods: List of HTTP methods allowed in CORS requests, here, any method ("*") is allowed.
# - allow_headers: List of HTTP headers allowed in CORS requests, here, any header ("*") is allowed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###################### INCLUDE ROUTERS * #####################
# These routers handle different endpoints and functionalities of the Online Classroom API
app.include_router(courses.router)             # Router for managing courses
app.include_router(users.router)               # Router for user-related operations
app.include_router(auth.router)                # Router for authentication and authorization
app.include_router(course_enrollment.router)   # Router for course enrollment
app.include_router(lessons.router)             # Router for managing lessons within courses
app.include_router(assignments.router)         # Router for handling assignments
###################### END ROUTERS #####################

@app.get("/")
def read_root():
    # This endpoint provides a simple response when accessing the root URL of the API
    return {"api_response": "Online Classroom API"}


