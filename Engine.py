import re

class ChatEngine:

    def __init__(self):

        self.menu = {
            "geprek original": 15000,
            "geprek keju": 18000,
            "geprek mozarella": 22000,
            "nasi": 5000,
            "es teh": 4000
        }

    def get_menu(self):

        text = "📋 DAFTAR MENU\n\n"

        for item, price in self.menu.items():
            text += f"• {item.title()} - Rp{price:,}\n"

        return text

    def get_promo(self):

        return """
🎉 PROMO HARI INI

Beli 2 Geprek Original
Gratis 1 Es Teh
"""

    def get_location(self):

        return """
📍 AYAM GEPREK NUSANTARA

Jl. Raya Mugassari No.10
Semarang
"""

    def get_opening_hours(self):

        return """
🕒 JAM OPERASIONAL

09.00 - 22.00 WIB
"""

    def recommendation(self):

        return """
🔥 MENU TERLARIS

1. Geprek Keju
2. Geprek Mozarella
3. Geprek Original

Rekomendasi:
🍗 Geprek Keju + 🥤 Es Teh
"""

    def contact(self):

        return """
☎️ KONTAK

WhatsApp:
0812-3456-7890

Instagram:
@ayamgepreknusantara
"""

    def help(self):

        return """
📚 DAFTAR PERINTAH

help
menu
promo
rekomendasi
lokasi
jam buka
kontak
status
keranjang
bayar

Contoh:

pesan 2 geprek keju
pesan 3 es teh
"""

    def parse_order(self, text):

        pattern = r'(\d+)\s+(geprek original|geprek keju|geprek mozarella|nasi|es teh)'

        matches = re.findall(
            pattern,
            text.lower()
        )

        orders = []

        for qty, item in matches:

            orders.append({
                "item": item,
                "qty": int(qty)
            })

        return orders

    def calculate_total(self, cart):

        total = 0

        for order in cart:

            total += (
                order["qty"]
                * self.menu[order["item"]]
            )

        return total
