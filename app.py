import streamlit as st
from Engine import ChatEngine
from FSM import State

st.set_page_config(
    page_title="Ayam Geprek Bot",
    page_icon="🍗",
    layout="wide"
)

engine = ChatEngine()

# SESSION

if "messages" not in st.session_state:
    st.session_state.messages = []

if "cart" not in st.session_state:
    st.session_state.cart = []

if "state" not in st.session_state:
    st.session_state.state = State.IDLE

if "order_id" not in st.session_state:
    st.session_state.order_id = 1

if "last_order" not in st.session_state:
    st.session_state.last_order = None

# SIDEBAR

with st.sidebar:

    st.title("🍗 Ayam Geprek")

    st.subheader("Menu")

    for item, price in engine.menu.items():
        st.write(
            f"• {item.title()} - Rp{price:,}"
        )

# HEADER

st.title("🍗 Chatbot Ayam Geprek Nusantara")

if len(st.session_state.messages) == 0:

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": """
Halo 👋

Selamat datang di Ayam Geprek Nusantara.

Ketik help untuk bantuan.
"""
        }
    )

# TAMPILKAN CHAT

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# INPUT

if prompt := st.chat_input("Ketik pesan..."):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    pesan = prompt.lower().strip()

    if st.session_state.state == State.CONFIRM_PAYMENT:

        if pesan == "ya":

            total = engine.calculate_total(
                st.session_state.cart
            )

            nomor = (
                f"GPK{st.session_state.order_id:03d}"
            )

            st.session_state.order_id += 1
            st.session_state.last_order = nomor

            jawaban = f"""
🎉 PESANAN BERHASIL

Nomor:
{nomor}

Total:
Rp{total:,}

Status:
Sedang Diproses
"""

            st.session_state.cart = []
            st.session_state.state = State.IDLE

        else:

            jawaban = """
❌ Pembayaran dibatalkan.
"""

            st.session_state.state = State.IDLE

    elif pesan == "help":

        jawaban = engine.help()

    elif pesan == "menu":

        jawaban = engine.get_menu()

    elif pesan == "promo":

        jawaban = engine.get_promo()

    elif pesan == "rekomendasi":

        jawaban = engine.recommendation()

    elif pesan == "lokasi":

        jawaban = engine.get_location()

    elif pesan == "jam buka":

        jawaban = engine.get_opening_hours()

    elif pesan == "kontak":

        jawaban = engine.contact()

    elif pesan == "status":

        if st.session_state.last_order:

            jawaban = f"""
📦 STATUS PESANAN

Nomor:
{st.session_state.last_order}

Status:
Sedang Diproses
"""
        else:
            jawaban = "Belum ada pesanan."

    elif "pedas" in pesan:

        jawaban = """
🌶 LEVEL PEDAS

Level 1
Level 2
Level 3
Level 4
Level 5
"""

    elif pesan.startswith("pesan"):

        orders = engine.parse_order(
            pesan
        )

        if len(orders) == 0:

            jawaban = """
Contoh:

pesan 2 geprek keju
pesan 1 nasi
pesan 3 es teh
"""

        else:

            for order in orders:
                st.session_state.cart.append(
                    order
                )

            jawaban = "✅ Pesanan ditambahkan."

    elif pesan == "keranjang":

        if len(st.session_state.cart) == 0:

            jawaban = "🛒 Keranjang kosong."

        else:

            total = 0

            text = "🛒 KERANJANG\n\n"

            for order in st.session_state.cart:

                subtotal = (
                    order["qty"]
                    * engine.menu[
                        order["item"]
                    ]
                )

                total += subtotal

                text += (
                    f"{order['qty']}x "
                    f"{order['item'].title()} "
                    f"= Rp{subtotal:,}\n"
                )

            text += (
                f"\n💰 Total Rp{total:,}"
            )

            jawaban = text

    elif pesan == "bayar":

        if len(st.session_state.cart) == 0:

            jawaban = "🛒 Keranjang kosong."

        else:

            st.session_state.state = (
                State.CONFIRM_PAYMENT
            )

            jawaban = """
Apakah pesanan sudah benar?

Ketik:
ya
atau
tidak
"""

    else:

        jawaban = """
Perintah tidak dikenali.

Ketik:
help
"""

    with st.chat_message("assistant"):
        st.write(jawaban)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": jawaban
        }
    )
