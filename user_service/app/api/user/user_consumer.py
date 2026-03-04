from faststream import AckPolicy
from faststream.kafka import KafkaMessage, KafkaRouter
from dishka.integrations.faststream import FromDishka, inject
from .user_events import UserCreateEvent
from .user_service import UserService

router = KafkaRouter()


@router.subscriber(
    "user-create",
    ack_policy=AckPolicy.MANUAL,
    auto_offset_reset="latest",
    group_id="user-create-group",
)
@inject
async def user_create(
    payload: UserCreateEvent,
    msg: KafkaMessage,
    user_service: FromDishka[UserService],
):
    await user_service.create(payload=payload.model_dump())
    await msg.ack()
