from dataclasses import dataclass
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from config import settings
from infrastructure.db.uow import UnitOfWork
from infrastructure.db.repo import UserChoiceRepository
from infrastructure.db.state_repo import UserStateRepository, BotStateRepository
from application.services.routing_service import RoutingService

@dataclass(frozen=True)
class Container:
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]
    uow: UnitOfWork
    repo: UserChoiceRepository
    routing: RoutingService
    user_state_repo: UserStateRepository
    bot_state_repo: BotStateRepository

def build_container() -> Container:
    engine = create_async_engine(settings.database_url, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    uow = UnitOfWork(session_factory)
    repo = UserChoiceRepository()
    user_state_repo = UserStateRepository()
    bot_state_repo = BotStateRepository()
    
    routing = RoutingService(
        owner_deliver_chat_id=settings.owner_deliver_chat_id,
        owner_open_url=str(settings.owner_open_url),
        owner_thread_id=settings.owner_thread_id,

        adv_new_deliver_chat_id=settings.adv_new_deliver_chat_id,
        adv_new_open_url=str(settings.adv_new_open_url),
        adv_new_thread_id=settings.adv_new_thread_id,

        adv_existing_deliver_chat_id=settings.adv_existing_deliver_chat_id,
        adv_existing_open_url=str(settings.adv_existing_open_url),
        adv_existing_thread_id=settings.adv_existing_thread_id,
        owner_accounting_open_url=str(settings.owner_accounting_open_url),
        support_open_url= str(settings.support_open_url),
    )

    return Container(
        engine=engine,
        session_factory=session_factory,
        uow=uow,
        repo=repo,
        routing=routing,
        user_state_repo=user_state_repo,
        bot_state_repo=bot_state_repo,
    )
