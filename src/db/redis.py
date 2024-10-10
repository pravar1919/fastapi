import aioredis
from src.config import Config

JTI_EXPIRY = 3600

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

# here we are storing jti in the redis

async def add_jti_to_blocklist(jti: str)->None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )

async def token_in_blocklist(jti: str)->bool:
    return token_blocklist.get(
        name=jti
    )

