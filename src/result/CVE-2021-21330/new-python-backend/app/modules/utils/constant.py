import json
import os

from aiohttp import web
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine

load_dotenv()

DATABASE_KEY = web.AppKey("database", AsyncEngine)

LIST_CORRECT_ANSWER = json.loads(os.getenv("LIST_CONDITIONS", "[]"))

LIST_CONTEXT = [
    {
        "path": "20-03-2020-airport",
        "label": "Lần đâu tiên vợ Ngáo tiễn tui.",
        "context": "Lần đầu được người yêu nhất của mình tiễn nó sung sướng gì đâu á. Nhìn vợ đáng yêu ghê. "
        "Yêu Yêu. Vợ của ai mà đáng yêu ghê ry ta.",
    },
    {
        "path": "20-09-2020-airport",
        "label": "Cũng là những lần đầu tiên vợ Ngáo tiễn anh.",
        "context": "Trong những lần vợ tiễn anh thì anh nhớ nhất những lần trong năm đầu tiên anh về. "
        "Hông biết tại sao nữa. Chắc là những những lần đầu nên nhớ hơn á vợ Ngáo. "
        "Hồi đó nhìn anh và vợ cưng ghê hì. Đúng là 2 tấm chiếu mới chưa quánh nhau lần nào :)))",
    },
    {
        "path": "26-10-2020",
        "label": "Lần đầu tiên vợ ra thăm anh.",
        "context": "Lần đầu vợ ra thăm anh. Anh vui kinh luôn á. Bất ngờ nữa. Giả làm shipper đồ. "
        "Đồ ngốc nghếch của tui. Nhìn hình ni anh nhớ Hà Nội ghê. Mún đi dạo hồ Tây với vợ.",
    },
    {
        "path": "13-12-2020",
        "label": "Chuyến du lịch nhớ đời của Quắc Tô.",
        "context": "Tưởng đâu về thăm người yêu để ABCXYZ ai ngờ chạy đôn chạy đáo chăm con báo Ngáo. "
        "Nhớ lại lúc ngáo nói mớ anh buồn cười ghê. Thương thương",
    },
    {
        "path": "17-01-2021",
        "label": "Lần du lịch đà lạt đầu tiên của Quắc Tô và Thị Ngáo.",
        "context": "Lần này là lần đầu tiên chúng ta đi du lịch với nhau ấy nhỉ cụ vợ của tui. "
        "Chuyến đi đó thật là vui vợ nhỉ. Lần đầu tiên anh được đi Đà Lạt này, mà lại với vợ nữa nên vui kinh. "
        "Đêm hôm đó vợ ngủ như heo không thèm thức canh sinh nhật luôn. "
        "Lúc gọi vợ dậy nhìn cục vợ mơ mơ màng màng mở quà mà a buồn cười kinh :))",
    },
    {
        "path": "17-01-2021-market",
        "label": "Đêm đi chợ đêm ở Đà Lạt.",
        "context": "Ít giờ trước khi chuyện ấy xảy ra :)). Hôm đó anh thấy thương vợ kinh á. "
        "Biết vì sao hông? Vì mấy hôm trước vợ hay quạu anh. "
        "Tự nhiên hôm đó vợ hiền như mèo, không nhăng miếng nào luôn nên a thấy thương kinh.",
    },
    {
        "path": "30-04-2021-part-1",
        "label": "Lần thứ 2 vợ ra Hà Nội thăm anh.",
        "context": "Lần này là vợ ra Hà Nội để chơi với anh nhân ngày 30/4 1/5. "
        "Lần đó đi vui kinh. Thấy vợ cười típ mắt khi chụp hình với anh. "
        "Sự hạnh phúc của vợ làm anh thấy hạnh phúc kinh luôn. Lại nhớ Hà Nội kinh.",
    },
    {
        "path": "02-05-2021-part-2",
        "label": "Chụp hình ở hồ Gươm này.",
        "context": "Hôm đó chụp hình cười ẻ luôn. Nhớ những lần cầm tay chạy chụp hình buồn cười kinh á. "
        "Trong hình nhìn anh có soái ca không vợ ngáo.",
    },
    {
        "path": "19-06-2021-danang",
        "label": "Lén về thăm cục vợ.",
        "context": "Đồ con nhền nhện của tui. Nhớ tới hôm đó chụp hình cho vợ mà cười ẻ luôn á.",
    },
    {
        "path": "10-10-2021-hanoi",
        "label": "Đặng Trần Côn này.",
        "context": "Lần đó là lần đầu tiên vợ với anh giận nhau hơn 1 tuần. "
        "Hôm đó anh buồn nên đi dạo quanh Hà Nội. "
        "Đi qua hết những nơi mà vợ và anh từng đi qua. Rồi nhớ về vợ Ngáo.",
    },
    {
        "path": "07-11-2021-hanriver",
        "label": "Lần đầu đi cây cầu đi bộ của Đà Nẵng.",
        "context": "Hôm đó là trước khi anh về lại Hà Nội để làm việc. "
        "Anh và vợ mua trà sữa Gông Cha rồi ra cầu ngồi. "
        "Hôm đó ở cầu người đông quá. Vợ lại quạu, anh lại phải dỗ đồ vợ Ngáo. Đồ vợ hư của tui.",
    },
    {
        "path": "15-01-2022-airport",
        "label": "Ngày đó anh trở về với em.",
        "context": "Ngày hôm đó em không biết là anh hồi hộp thế nào đâu. "
        "Trước hôm đó vợ lại quạu anh chuyện chi đó. Nên anh lo không biết vợ có đón anh hay không. "
        "Nên khi thấy vợ anh xúc động kinh luôn. Yêu đồ ngốc của anh nhất.",
    },
    {
        "path": "14-02-2022-valentine",
        "label": "Ngày lễ tình nhân đầu tiên anh ở bên em.",
        "context": "Hôm đó lần đầu tiên được đi ăn valentine với vợ ở Đà Nẵng luôn á. "
        "Thích ghê á vợ ngáo. Tiếc là HongDae nó đóng cửa ở Đà Nẵng rồi. Không là bọn mình đi ăn HongDea rồi hì. "
        "Tới đây chắc vợ thèm đồ nướng lắm chứ chi. Yêu lắm này vợ Ngáo của tui.",
    },
    {
        "path": "26-03-2022-hue",
        "label": "Một ngày trước thảm hoạ xảy ra T.T .",
        "context": "Vợ có nhớ lần đó sao mình lại đi Huế không? "
        "Đợt đó là 1 năm sau khi mình đi resort ở Lăng Cô. Vợ tự nhiên thèm đi chơi. "
        "Mà giá resort ở Lăng Cô nó mắc quá nên bọn mình mới chốt đi Huế này. "
        "Đợt đó mình ở cái khách sạn ở đường Hai Bà Trưng ấy nhỉ. "
        "Haizz thèm bún bò Huế ghê.",
    },
    {
        "path": "12-05-2022-saigon",
        "label": "Chuyến đi Sài Gòn đáng nhớ.",
        "context": "Chuyến đi Sài Gòn đó vui em nhỉ. Lần đầu tiên ăn bánh tráng trộn Sài Gòn này, "
        "lần đầu tiên uống froster này, lần đầu tiên trải nghiệm ngồi qua đêm ở Circle-K Vũng Tàu. "
        'Nhớ cái đêm anh với vợ đi dạo đêm quanh Vũng Tàu, rồi vợ giả tiếng "veeeeee" điếc cả tai luôn. '
        "Đồ con ve ngốc của tui.",
    },
    {
        "path": "18-03-2023",
        "label": "Con chim cánh cụt của tui đây này.",
        "context": "Một chiều thứ 7 nào đó ở coffee house xuất hiện 1 con chim cánh cụt xinhhh đẹp. "
        "Lúc đó mới mua cho vợ cái áo khoác. Vợ Ngáo thích ghê luôn, mang suốt à, mà vợ mang xinh ghê luôn á.",
    },
    {
        "path": "19-03-2023-hoian",
        "label": "Tấm hình cừi ẻ của vợ Ngáo.",
        "context": "Mỗi lần lướt xem ảnh cũ, nhìn thấy tấm hình này anh cười ghê luôn. Đúng là vợ Ngáo nhứt của tui.",
    },
    {
        "path": "30-03-2023",
        "label": "Tấm hình cừi ẻ thứ 2 của vợ Ngáo.",
        "context": "Tự nhiên hôm đó đang chụp lén vợ, tự nhiên vợ kêu anh chụp vợ cái rồi vợ làm cái mặt ngáo ngơ ni. "
        "Vợ hôm đó chắc bị ma Ngáo nhập rồi.",
    },
    {
        "path": "21-04-2023",
        "label": "Mixue nè.",
        "context": "Lần này không biết có phải là lần đầu tiên ăn mixue của Tô và Ngáo hay không nữa. "
        "Nhưng nhìn mặt vợ vui ghê. Chắc là lần đầu tiên rồi.",
    },
    {
        "path": "04-05-2023",
        "label": "Lần đầu đạp xe với vợ.",
        "context": "Hôm đó thích ghê á, lần đầu tiên đạp xe với vợ. Thấy vợ vừa đạp vừa thở dóc anh khoái ghê. "
        "Chắc thấy vợ đau khổ đạp xe nên anh mới khoái dị á. Thích đạp xe với vợ nữa ghê. Đồ vợ lười chảy thây của tui.",
    },
    {
        "path": "07-05-2023-beautiful-day",
        "label": "Ngày đẹp nhứt của chúng mình.",
        "context": "Ngày trọng đại của 2 chúng mình này. Hôm đó vợ xinh ghê luôn. "
        "Thấy vợ thẹn thùng đi theo mẹ ra trước nhà mà cảm xúc anh lẫn lộn."
        "Nữa thấy xúc động vì sự xinh đẹp của vợ vừa thấy cười ẻ vì khuôn mặt thẹn thùng của vợ."
        "Lúc nớ mà không có ai chắc anh cười ha hả rồi. Đùa chứ hôm đó anh vui ghê luôn. "
        "Vì đã gần 1 nữa có được vợ Ngáo của tui rồi này.",
    },
    {
        "path": "27-05-2023",
        "label": "Ngáo và Chuột này.",
        "context": "Tấm hình cuối cùng của anh có con chuột. Nhớ chuột kinh, mới còn tắm cho nó mà giờ đã... "
        "Thương chuột, thương cả Ngáo của tui.",
    },
    {
        "path": "29-07-2023-mangden-travel",
        "label": "Chuyến đi phượt xa đầu tiên của chúng ta.",
        "context": "Cái này phải là chuyến đi healing (chữa rách tâm hồn) đầu tiên của chúng ta mới đúng chứ haha. "
        "Đi mệt mà vui vợ hì. Đúng là lâu lắm anh mới có cảm giác thoải mái như vậy á. Dù là phải di chuyển nhiều, "
        "ngày nào cũng đi hết luôn, mà lần nào cũng đi mấy chục với mấy trăm cây hết. Nhưng mà thích. "
        "Qua tết mình sắp xếp làm chuyến nữa vợ nhỉ.",
    },
    {
        "path": "23-09-2023",
        "label": "Một tấm hình xinh xắn của Thị Ngáo.",
        "context": "Hehe anh lấy tấm này vì đơn giản nó là tấm hình xinh nhất gần nhất trong máy anh thôi hehe "
        "(Ý anh không phải là những tấm khác ko xinh đâu nhaaaa). Tấm hình nào của vợ trong máy anh cũng xinh hết. "
        "Nhưng vợ toàn bảo anh dình vợ thôi nên anh mới lấy tấm ni đó. Bắt bẻ anh đi anh quánh chết). "
        "Lựa 1 tấm xinh để vợ khỏi nói anh đăng ảnh dìm vợ Ngáo hehehehe. ",
    },
    {
        "path": "23-11-2023",
        "label": "Mỹ nhân và méo.",
        "context": "Nhìn vào tấm hình ni anh thấy có tới 2 con mèo luôn. "
        "Một con mèo nhỏ vô hại và một con mèo Ngáo hung dữ thích cào. "
        "Có ngày anh lén nữa đêm dậy cắt hết móng của vợ, cắt xát dô luôn, cho chừa tội láo lếu...",
    },
    {
        "path": "02-12-2023",
        "label": "Một tấm hình dễ thương của vợ.",
        "context": "Hehe nếu không phải là do cái phòng hơi bừa bộn thì anh đã đặt tấm ni làm hình nền điện thoại rồi đó. "
        "Nhìn đáng yêu ghê luôn, cưng nữa á. À ngày hôm đó là ngày trước khi vợ đi thi tiếng Nhật :v",
    },
    {
        "path": "24-12-2023-xmas",
        "label": "Giáng sinh đầu tiên bên vợ.",
        "context": "Lại một tấm hình dễ thương nữa của vợ. Lâu lắm mới thấy lại vợ đàn. "
        "Lúc vợ đàn thấy vợ thật là xinhh luôn đó vợ biết không? "
        "Sau ni có tiền anh sẽ mua cái đàn xịn cho vợ, để vợ tối nào cũng đàn cho anh nghe.",
    },
    {
        "path": "26-12-2023-ngaongo",
        "label": "Thêm 1 tấm dễ thương của vợ này.",
        "context": "Hôm đó có chiện gì ấy nhỉ mà vợ ngáo nhìn hiền kinh. "
        "Hê hê nhìn dễ thương kinh. mất là cái mái bị lệt qua nhìn cưng dễ sợ. "
        "Mún hun cho 1 cái luôn ấy.",
    },
]
