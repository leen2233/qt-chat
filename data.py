from chat_types import ChatType, MessageType, StatType

CHAT_LIST = [
    ChatType(
        id=1,
        avatar="https://fastly.picsum.photos/id/689/200/200.jpg?hmac=2KHWG2UlfLNAWC1jiBz-LQ7b-TMOB4bcW-FVvdQ_7a4",
        name="John Doe",
        last_message="Hello!",
        time="3 min ago",
        phone_number="+99361234567",
        username="john244",
        stats=StatType(photos=10, videos=2, files=360, links=231, voices=2),
        messages=[
            MessageType(text="Hi there!", sender="me", time="10:00 AM"),
            MessageType(text="Hello!", sender="another", time="10:03 AM"),
            MessageType(text="How's it going?", sender="me", time="10:05 AM"),
            MessageType(text="Pretty good, you?", sender="another", time="10:06 AM"),
            MessageType(text="Same here!", sender="me", time="10:07 AM"),
            MessageType(
                text="""
                self.nm.finished.connect(self.on_image_loaded)
                url = QUrl(avatar)
                request = QNetworkRequest(url)
                self.nm.get(request)

                # Default placeholder for avatar
                self.set_default_avatar()""",
                sender="another",
                time="10:07 AM",
            ),
        ],
    ),
    ChatType(
        id=2,
        avatar="https://fastly.picsum.photos/id/25/200/200.jpg?hmac=G4ZRBi0qdWfQJQs_yxNQr_LJJlf0V1_Pdj8Tp41xsJU",
        name="Jane Smith",
        last_message="Yeah it's awesome!",
        time="5 hours ago",
        phone_number="+99361234563",
        username="jane_smith",
        stats=StatType(photos=10, videos=2, files=360, links=231, voices=2),
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
        avatar="https://fastly.picsum.photos/id/354/200/200.jpg?hmac=ykMwenrB5tcaT_UHlYwh2ZzAZ4Km48YOmwJTFCiodJ4",
        name="Alice Johnson",
        last_message="Hey!",
        time="just now",
        phone_number="+99361234565",
        username="alice.johnson",
        stats=StatType(photos=10, videos=2, files=360, links=231, voices=2),
        messages=[
            MessageType(text="Hey!", sender="another", time="10:30 AM"),
            MessageType(text="What's up?", sender="me", time="10:31 AM"),
            MessageType(text="Just chilling!", sender="another", time="10:32 AM"),
            MessageType(text="Nice, any plans?", sender="me", time="10:33 AM"),
            MessageType(text="Maybe a movie!", sender="me", time="10:34 AM"),
        ],
    ),
]
