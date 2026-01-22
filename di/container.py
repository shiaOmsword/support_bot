from dataclasses import dataclass
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from config import settings
from infrastructure.db.uow import UnitOfWork
from infrastructure.db.repo import UserChoiceRepository
from application.services.routing_service import RoutingService

@dataclass(frozen=True)
class Container:
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]
    uow: UnitOfWork
    repo: UserChoiceRepository
    routing: RoutingService

def build_container() -> Container:
    engine = create_async_engine(settings.database_url, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    uow = UnitOfWork(session_factory)
    repo = UserChoiceRepository()

    routing = RoutingService(
        advertiser_url=str(settings.advertiser_chat_url),
        owner_url=str(settings.owner_chat_url),
        uow=uow,
        repo=repo,
    )

    return Container(
        engine=engine,
        session_factory=session_factory,
        uow=uow,
        repo=repo,
        routing=routing,
    )
