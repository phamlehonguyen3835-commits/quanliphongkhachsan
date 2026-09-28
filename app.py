import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import json

# =========================================================
# CẤU HÌNH
# =========================================================
st.set_page_config(
    page_title="Hotel Manager",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "hotel_data.json"

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #1f4e79;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #666;
        margin-bottom: 25px;
    }

    .room-card {
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #ddd;
        background-color: #ffffff;
    }

    .status-available {
        color: #198754;
        font-weight: bold;
    }

    .status-occupied {
        color: #dc3545;
        font-weight: bold;
    }

    .status-cleaning {
        color: #fd7e14;
        font-weight: bold;
    }

    .status-maintenance {
        color: #6c757d;
        font-weight: bold;
    }

    .metric-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        border: 1px solid #e1e5ea;
    }

    div[data-testid="stMetricValue"] {
        color: #1f4e79;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# DỮ LIỆU MẶC ĐỊNH
# =========================================================
DEFAULT_ROOMS = [
    {
        "room": "101",
        "type": "Standard",
        "floor": 1,
        "price": 500000,
        "status": "Trống",
        "customer": "",
        "phone": "",
        "checkin": "",
        "checkout": ""
    },
    {
        "room": "102",
        "type": "Standard",
        "floor": 1,
        "price": 500000,
        "status": "Đang ở",
        "customer": "Nguyễn Văn An",
        "phone": "0901234567",
        "checkin": "2026-09-27",
        "checkout": "2026-09-29"
    },
    {
        "room": "103",
        "type": "Deluxe",
        "floor": 1,
        "price": 800000,
        "status": "Trống",
        "customer": "",
        "phone": "",
        "checkin": "",
        "checkout": ""
    },
    {
        "room": "201",
        "type": "Deluxe",
        "floor": 2,
        "price": 800000,
        "status": "Đang vệ sinh",
        "customer": "",
        "phone": "",
        "checkin": "",
        "checkout": ""
    },
    {
        "room": "202",
        "type": "Suite",
        "floor": 2,
        "price": 1200000,
        "status": "Trống",
        "customer": "",
        "phone": "",
        "checkin": "",
        "checkout": ""
    },
    {
        "room": "203",
        "type": "Suite",
        "floor": 2,
        "price": 1200000,
        "status": "Bảo trì",
        "customer": "",
        "phone": "",
        "checkin": "",
        "checkout": ""
    },
    {
        "room": "301",
        "type": "Standard",
        "floor": 3,
        "price": 500000,
        "status": "Trống",
        "customer": "",
        "phone": "",
        "checkin": "",
        "checkout": ""
    },
    {
        "room": "302",
        "type": "Deluxe",
        "floor": 3,
        "price": 800000,
        "status": "Đang ở",
        "customer": "Trần Thị Mai",
        "phone": "0912345678",
        "checkin": "2026-09-26",
        "checkout": "2026-09-30"
    },
]


# =========================================================
# HÀM ĐỌC / LƯU DỮ LIỆU
# =========================================================
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception:
            return DEFAULT_ROOMS.copy()

    return DEFAULT_ROOMS.copy()


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.rooms, f, ensure_ascii=False, indent=4)


if "rooms" not in st.session_state:
    st.session_state.rooms = load_data()


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================
def money(value):
    return f"{value:,.0f} VNĐ"


def get_room(room_number):
    for room in st.session_state.rooms:
        if room["room"] == room_number:
            return room
    return None


def status_icon(status):
    icons = {
        "Trống": "🟢",
        "Đang ở": "🔴",
        "Đang vệ sinh": "🟠",
        "Bảo trì": "⚫"
    }
    return icons.get(status, "⚪")


def status_class(status):
    classes = {
        "Trống": "status-available",
        "Đang ở": "status-occupied",
        "Đang vệ sinh": "status-cleaning",
        "Bảo trì": "status-maintenance"
    }
    return classes.get(status, "")


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("🏨 HOTEL MANAGER")
st.sidebar.caption("Hệ thống quản lý khách sạn")

menu = st.sidebar.radio(
    "MENU",
    [
        "📊 Tổng quan",
        "🛏️ Quản lý phòng",
        "📋 Đặt phòng / Check-in",
        "🚪 Check-out",
        "👤 Khách hàng",
        "💰 Doanh thu"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "💡 Dữ liệu được lưu tự động vào file "
    "`hotel_data.json`."
)


# =========================================================
# TRANG TỔNG QUAN
# =========================================================
if menu == "📊 Tổng quan":

    st.markdown(
        '<div class="main-title">📊 Tổng quan khách sạn</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Theo dõi tình trạng phòng và hoạt động khách sạn</div>',
        unsafe_allow_html=True
    )

    rooms = st.session_state.rooms

    total = len(rooms)
    available = len([r for r in rooms if r["status"] == "Trống"])
    occupied = len([r for r in rooms if r["status"] == "Đang ở"])
    cleaning = len([r for r in rooms if r["status"] == "Đang vệ sinh"])
    maintenance = len([r for r in rooms if r["status"] == "Bảo trì"])

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🏨 Tổng phòng", total)
    c2.metric("🟢 Phòng trống", available)
    c3.metric("🔴 Đang ở", occupied)
    c4.metric("🧹 Vệ sinh", cleaning)
    c5.metric("🔧 Bảo trì", maintenance)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Tỷ lệ sử dụng phòng")

        if total > 0:
            occupancy = occupied / total * 100
        else:
            occupancy = 0

        st.progress(int(occupancy))
        st.write(f"**{occupancy:.1f}%** phòng đang được sử dụng.")

    with col2:
        st.subheader("💵 Doanh thu dự kiến")

        revenue = sum(
            r["price"]
            for r in rooms
            if r["status"] == "Đang ở"
        )

        st.metric(
            "Doanh thu phòng hiện tại",
            money(revenue)
        )

    st.divider()

    st.subheader("🛏️ Tình trạng phòng")

    df = pd.DataFrame(rooms)

    if not df.empty:
        display_df = df[
            [
                "room",
                "type",
                "floor",
                "price",
                "status",
                "customer",
                "checkin",
                "checkout"
            ]
        ].copy()

        display_df.columns = [
            "Phòng",
            "Loại phòng",
            "Tầng",
            "Giá/đêm",
            "Trạng thái",
            "Khách hàng",
            "Check-in",
            "Check-out"
        ]

        display_df["Giá/đêm"] = display_df["Giá/đêm"].apply(money)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# QUẢN LÝ PHÒNG
# =========================================================
elif menu == "🛏️ Quản lý phòng":

    st.markdown(
        '<div class="main-title">🛏️ Quản lý phòng</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Theo dõi và cập nhật trạng thái phòng</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input(
            "🔍 Tìm phòng",
            placeholder="Ví dụ: 101"
        )

    with col2:
        status_filter = st.selectbox(
            "Trạng thái",
            ["Tất cả", "Trống", "Đang ở", "Đang vệ sinh", "Bảo trì"]
        )

    with col3:
        type_filter = st.selectbox(
            "Loại phòng",
            ["Tất cả"] +
            sorted(list(set(r["type"] for r in st.session_state.rooms)))
        )

    filtered_rooms = st.session_state.rooms.copy()

    if search:
        filtered_rooms = [
            r for r in filtered_rooms
            if search.lower() in r["room"].lower()
        ]

    if status_filter != "Tất cả":
        filtered_rooms = [
            r for r in filtered_rooms
            if r["status"] == status_filter
        ]

    if type_filter != "Tất cả":
        filtered_rooms = [
            r for r in filtered_rooms
            if r["type"] == type_filter
        ]

    st.divider()

    # Hiển thị phòng dạng card
    cols = st.columns(3)

    for index, room in enumerate(filtered_rooms):

        with cols[index % 3]:

            st.markdown(
                f"""
                <div class="room-card">
                    <h3>🚪 Phòng {room['room']}</h3>
                    <p>🏷️ Loại: <b>{room['type']}</b></p>
                    <p>🏢 Tầng: <b>{room['floor']}</b></p>
                    <p>💰 Giá: <b>{money(room['price'])}/đêm</b></p>
                    <p class="{status_class(room['status'])}">
                        {status_icon(room['status'])}
                        {room['status']}
                    </p>
                    <p>👤 {room['customer'] if room['customer'] else 'Chưa có khách'}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            new_status = st.selectbox(
                f"Cập nhật phòng {room['room']}",
                ["Trống", "Đang ở", "Đang vệ sinh", "Bảo trì"],
                index=[
                    "Trống",
                    "Đang ở",
                    "Đang vệ sinh",
                    "Bảo trì"
                ].index(room["status"]),
                key=f"status_{room['room']}"
            )

            if new_status != room["status"]:

                room["status"] = new_status

                if new_status != "Đang ở":
                    room["customer"] = ""
                    room["phone"] = ""
                    room["checkin"] = ""
                    room["checkout"] = ""

                save_data()
                st.rerun()


# =========================================================
# CHECK-IN
# =========================================================
elif menu == "📋 Đặt phòng / Check-in":

    st.markdown(
        '<div class="main-title">📋 Đặt phòng / Check-in</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Tạo thông tin lưu trú cho khách hàng</div>',
        unsafe_allow_html=True
    )

    available_rooms = [
        r for r in st.session_state.rooms
        if r["status"] == "Trống"
    ]

    if not available_rooms:
        st.warning("⚠️ Hiện không có phòng trống.")
    else:

        with st.form("checkin_form"):

            col1, col2 = st.columns(2)

            with col1:

                room_number = st.selectbox(
                    "🛏️ Chọn phòng",
                    [r["room"] for r in available_rooms]
                )

                customer_name = st.text_input(
                    "👤 Họ và tên khách *"
                )

                phone = st.text_input(
                    "📞 Số điện thoại *"
                )

                identity = st.text_input(
                    "🪪 CCCD / Passport"
                )

            with col2:

                checkin = st.date_input(
                    "📅 Ngày check-in",
                    value=date.today()
                )

                checkout = st.date_input(
                    "📅 Ngày check-out",
                    value=date.today()
                )

                adults = st.number_input(
                    "👨‍👩‍👧 Người lớn",
                    min_value=1,
                    value=1
                )

                note = st.text_area(
                    "📝 Ghi chú"
                )

            submitted = st.form_submit_button(
                "✅ Xác nhận Check-in",
                use_container_width=True
            )

            if submitted:

                if not customer_name.strip():
                    st.error("Vui lòng nhập họ tên khách hàng.")

                elif not phone.strip():
                    st.error("Vui lòng nhập số điện thoại.")

                elif checkout <= checkin:
                    st.error(
                        "Ngày check-out phải sau ngày check-in."
                    )

                else:

                    room = get_room(room_number)

                    room["status"] = "Đang ở"
                    room["customer"] = customer_name
                    room["phone"] = phone
                    room["checkin"] = str(checkin)
                    room["checkout"] = str(checkout)

                    save_data()

                    st.success(
                        f"✅ Check-in thành công cho "
                        f"{customer_name} - Phòng {room_number}"
                    )

                    st.rerun()


# =========================================================
# CHECK-OUT
# =========================================================
elif menu == "🚪 Check-out":

    st.markdown(
        '<div class="main-title">🚪 Check-out</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Thanh toán và trả phòng cho khách</div>',
        unsafe_allow_html=True
    )

    occupied_rooms = [
        r for r in st.session_state.rooms
        if r["status"] == "Đang ở"
    ]

    if not occupied_rooms:

        st.info("Hiện không có khách đang lưu trú.")

    else:

        room_number = st.selectbox(
            "🛏️ Chọn phòng cần check-out",
            [r["room"] for r in occupied_rooms]
        )

        room = get_room(room_number)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("👤 Thông tin khách")

            st.write(f"**Họ tên:** {room['customer']}")
            st.write(f"**Điện thoại:** {room['phone']}")
            st.write(f"**Check-in:** {room['checkin']}")
            st.write(f"**Check-out dự kiến:** {room['checkout']}")

        with col2:

            checkin_date = datetime.strptime(
                room["checkin"],
                "%Y-%m-%d"
            ).date()

            checkout_date = date.today()

            nights = (
                checkout_date - checkin_date
            ).days

            if nights < 1:
                nights = 1

            room_total = nights * room["price"]

            extra_charge = st.number_input(
                "💵 Phụ thu",
                min_value=0,
                value=0,
                step=50000
            )

            discount = st.number_input(
                "🎫 Giảm giá",
                min_value=0,
                value=0,
                step=50000
            )

            total = room_total + extra_charge - discount

            st.metric(
                "💰 Tổng thanh toán",
                money(total)
            )

        st.divider()

        payment_method = st.selectbox(
            "💳 Phương thức thanh toán",
            [
                "Tiền mặt",
                "Chuyển khoản",
                "Thẻ ngân hàng",
                "Ví điện tử"
            ]
        )

        if st.button(
            "✅ Xác nhận Check-out",
            type="primary",
            use_container_width=True
        ):

            room["status"] = "Đang vệ sinh"

            room["customer"] = ""
            room["phone"] = ""
            room["checkin"] = ""
            room["checkout"] = ""

            save_data()

            st.success(
                f"Check-out thành công. "
                f"Đã thu {money(total)} bằng {payment_method}."
            )

            st.rerun()


# =========================================================
# KHÁCH HÀNG
# =========================================================
elif menu == "👤 Khách hàng":

    st.markdown(
        '<div class="main-title">👤 Khách hàng</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Danh sách khách đang lưu trú</div>',
        unsafe_allow_html=True
    )

    customers = [
        r for r in st.session_state.rooms
        if r["status"] == "Đang ở"
    ]

    if not customers:

        st.info("Chưa có khách đang lưu trú.")

    else:

        data = []

        for r in customers:

            data.append({
                "Phòng": r["room"],
                "Họ tên": r["customer"],
                "Số điện thoại": r["phone"],
                "Loại phòng": r["type"],
                "Check-in": r["checkin"],
                "Check-out": r["checkout"],
                "Giá phòng": money(r["price"])
            })

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# DOANH THU
# =========================================================
elif menu == "💰 Doanh thu":

    st.markdown(
        '<div class="main-title">💰 Doanh thu</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Theo dõi doanh thu phòng</div>',
        unsafe_allow_html=True
    )

    rooms = st.session_state.rooms

    total_rooms = len(rooms)

    occupied_rooms = [
        r for r in rooms
        if r["status"] == "Đang ở"
    ]

    available_rooms = [
        r for r in rooms
        if r["status"] == "Trống"
    ]

    revenue = sum(
        r["price"]
        for r in occupied_rooms
    )

    average_price = (
        sum(r["price"] for r in rooms) / total_rooms
        if total_rooms
        else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 Doanh thu đang ghi nhận",
        money(revenue)
    )

    c2.metric(
        "🛏️ Giá phòng trung bình",
        money(average_price)
    )

    c3.metric(
        "👥 Phòng đang có khách",
        len(occupied_rooms)
    )

    st.divider()

    st.subheader("📊 Doanh thu theo loại phòng")

    revenue_by_type = {}

    for room in occupied_rooms:

        room_type = room["type"]

        if room_type not in revenue_by_type:
            revenue_by_type[room_type] = 0

        revenue_by_type[room_type] += room["price"]

    if revenue_by_type:

        chart_df = pd.DataFrame(
            list(revenue_by_type.items()),
            columns=["Loại phòng", "Doanh thu"]
        )

        chart_df = chart_df.set_index("Loại phòng")

        st.bar_chart(chart_df)

    else:

        st.info(
            "Chưa có dữ liệu doanh thu để hiển thị."
        )

    st.divider()

    st.subheader("📋 Chi tiết phòng đang tạo doanh thu")

    if occupied_rooms:

        revenue_data = []

        for r in occupied_rooms:

            revenue_data.append({
                "Phòng": r["room"],
                "Loại": r["type"],
                "Khách hàng": r["customer"],
                "Giá/đêm": money(r["price"]),
                "Check-in": r["checkin"],
                "Check-out": r["checkout"]
            })

        st.dataframe(
            pd.DataFrame(revenue_data),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Chưa có phòng đang tạo doanh thu.")


# =========================================================
# FOOTER
# =========================================================
st.sidebar.divider()
st.sidebar.caption(
    "Hotel Manager v1.0 • Streamlit"
)
