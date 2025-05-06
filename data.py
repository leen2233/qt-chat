from chat_types import ChatType, MessageType

CHAT_LIST = [
    ChatType(
        id=1,
        name="John Doe",
        last_message="Hello!",
        time="3 min ago",
        messages=[
            MessageType(text="Hi there!", sender="me", time="10:00 AM"),
            MessageType(text="Hello!", sender="another", time="10:03 AM"),
            MessageType(text="How's it going?", sender="me", time="10:05 AM"),
            MessageType(text="Pretty good, you?", sender="another", time="10:06 AM"),
            MessageType(text="Same here!", sender="me", time="10:07 AM"),
        ],
    ),
    ChatType(
        id=2,
        name="Jane Smith",
        last_message="Yeah it's awesome!",
        time="5 hours ago",
        messages=[
            MessageType(text="Check this out!", sender="me", time="2:00 AM"),
            MessageType(text="Yeah it's awesome!", sender="another", time="2:05 AM"),
            MessageType(text="Got more to share?", sender="me", time="2:10 AM"),
            MessageType(text="Totally, later!", sender="another", time="2:15 AM"),
            MessageType(text="Can't wait!", sender="me", time="2:20 AM"),
        ],
    ),
    ChatType(
        id=3,
        name="Alice Johnson",
        last_message="Hey!",
        time="just now",
        messages=[
            MessageType(text="Hey!", sender="another", time="10:30 AM"),
            MessageType(text="What's up?", sender="me", time="10:31 AM"),
            MessageType(text="Just chilling!", sender="another", time="10:32 AM"),
            MessageType(text="Nice, any plans?", sender="me", time="10:33 AM"),
            MessageType(text="Maybe a movie!", sender="me", time="10:34 AM"),
        ],
    ),
]
