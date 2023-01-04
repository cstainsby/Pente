from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .database import PenteDatabase
from . import models