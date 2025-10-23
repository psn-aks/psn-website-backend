# import asyncio
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlmodel import select

# from src.db.session import engine
# from src.auth.models import User, UserRole
# from src.core.security import PWDHashing
# from src.core.config import Config

# pwd_hashing = PWDHashing()


# async def create_admin():
#     async with AsyncSession(engine) as session:
#         result = await session.exec(
#             select(User).where(User.role == UserRole.ADMIN)
#         )
#         if not result.first():
#             admin = User(
#                 email=Config.ADMIN_EMAIL,
#                 full_name="Super Admin",
#                 role=UserRole.ADMIN,
#                 hashed_password=pwd_hashing.generate_password_hash(
#                     Config.ADMIN_PASSWORD
#                 )
#             )
#             session.add(admin)
#             await session.commit()
#             await session.refresh(admin)
#             print("✅ Admin created")
#         else:
#             print("Admin already exists")

# if __name__ == "__main__":
#     asyncio.run(create_admin())
