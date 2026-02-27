from passlib.context import CryptContext


myctx = CryptContext(schemes=["argon2"], deprecated="auto")