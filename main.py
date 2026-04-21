import discord
from discord import Webhook
import aiohttp
import asyncio
from datetime import datetime

# --- CẤU HÌNH ---
WEBHOOK_URL = ''
API_URL = "https://test-hub.kys.gay/api/stock"
LOGO_URL = "http://googleusercontent.com/image_collection/image_retrieval/78615118789308201_0"
SUPPORT_URL = "https://discord.gg/Zg2XkS5hq9"
POLL_INTERVAL = 60  # giây, kiểm tra API mỗi 60s

def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def stock_signature(stock_list: list) -> frozenset:
    """Fingerprint kho hàng bằng tập tên fruit — thay đổi = reset."""
    return frozenset(item.get('name', '') for item in stock_list)

def format_stock(stock_list: list) -> str:
    if not stock_list:
        return "Hiện tại không có stock."
    lines = []
    for item in stock_list:
        name = item.get('name', 'Unknown')
        price = f"{item.get('price_beli', 0):,}"
        lines.append(f"• **{name}** — `{price} Beli`")
    return "\n".join(lines)

async def send_webhook(
    session: aiohttp.ClientSession,
    json_data: dict,
    data: dict,
    timers: dict,
    mirage_reset: bool,
    normal_reset: bool,
    is_startup: bool = False
):
    all_items = data.get('mirage_stock', []) + data.get('normal_stock', [])
    top_fruit = max(all_items, key=lambda x: x.get('price_beli', 0), default=None)
    thumbnail_url = top_fruit.get('image_url', LOGO_URL) if top_fruit else LOGO_URL
    top_name = top_fruit.get('name', 'N/A') if top_fruit else 'N/A'
    top_price = f"{top_fruit.get('price_beli', 0):,}" if top_fruit else 'N/A'

    # --- Tiêu đề sự kiện ---
    if is_startup:
        event_label = "🟢 Bot khởi động — Stock hiện tại"
    elif mirage_reset and normal_reset:
        event_label = "🔄 Cả 2 kho vừa **RESET**!"
    elif mirage_reset:
        event_label = "🏝️ **Mirage Island** vừa RESET!"
    else:
        event_label = "🛒 **Normal Shop** vừa RESET!"

    webhook = Webhook.from_url(WEBHOOK_URL, session=session)
    view = discord.ui.LayoutView()
    container = discord.ui.Container(accent_colour=discord.Colour.green())

    # --- Header ---
    header_section = discord.ui.Section(
        discord.ui.TextDisplay(content=f"# 🍎 BLOXFRUIT LIVE STOCK"),
        discord.ui.TextDisplay(
            content=(
                f"{event_label}\n"
                f"Cập nhật từ hệ thống **{json_data.get('provider', 'BloxFruit')}**\n"
                f"-# 👑 Fruit đắt nhất: **{top_name}** — `{top_price} Beli`"
            )
        ),
        accessory=discord.ui.Thumbnail(media=thumbnail_url)
    )
    container.add_item(header_section)
    container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

    # --- Mirage Stock ---
    container.add_item(
        discord.ui.TextDisplay(
            content=f"### 🏝️ Mirage Island Stock\n{format_stock(data.get('mirage_stock', []))}"
        )
    )
    container.add_item(discord.ui.Separator())

    # --- Normal Stock ---
    container.add_item(
        discord.ui.TextDisplay(
            content=f"### 🛒 Normal Shop Stock\n{format_stock(data.get('normal_stock', []))}"
        )
    )
    container.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

    # --- Timers ---
    reset_text = (
        f"### ⏰ Trình thời gian\n"
        f"⏳ Mirage Reset: `{timers.get('mirage_reset_in', 'N/A')}`\n"
        f"🛒 Normal Reset: `{timers.get('normal_reset_in', 'N/A')}`"
    )
    container.add_item(discord.ui.TextDisplay(content=reset_text))
    container.add_item(discord.ui.Separator())

    # --- Button Support ---
    support_button = discord.ui.Button(
        style=discord.ButtonStyle.link,
        label="💬 Support Server",
        url=SUPPORT_URL
    )
    container.add_item(discord.ui.ActionRow(support_button))
    container.add_item(discord.ui.Separator())

    # --- Footer ---
    container.add_item(
        discord.ui.TextDisplay(content="-# BloxFruit Stock Notifier • Tự động cập nhật")
    )

    view.add_item(container)

    await webhook.send(
        view=view,
        username="BloxFruit Bot",
        avatar_url=LOGO_URL
    )

async def fetch_stock(session: aiohttp.ClientSession):
    """Fetch API, trả về (json_data, data, timers) hoặc None nếu lỗi."""
    try:
        async with session.get(API_URL, timeout=aiohttp.ClientTimeout(total=15)) as response:
            if response.status == 200:
                json_data = await response.json()
                return json_data, json_data.get('data', {}), json_data.get('timers', {})
            else:
                log(f"❌ Lỗi API: HTTP {response.status}")
    except asyncio.TimeoutError:
        log("❌ Timeout khi gọi API.")
    except Exception as e:
        log(f"❌ Lỗi kết nối: {e}")
    return None

async def main():
    log("🚀 BloxFruit Stock Notifier khởi động — chạy 24/7")

    prev_mirage_sig: frozenset | None = None
    prev_normal_sig: frozenset | None = None
    is_startup = True

    async with aiohttp.ClientSession() as session:
        while True:
            result = await fetch_stock(session)

            if result:
                json_data, data, timers = result
                mirage_stock = data.get('mirage_stock', [])
                normal_stock = data.get('normal_stock', [])

                cur_mirage_sig = stock_signature(mirage_stock)
                cur_normal_sig = stock_signature(normal_stock)

                mirage_reset = not is_startup and cur_mirage_sig != prev_mirage_sig
                normal_reset = not is_startup and cur_normal_sig != prev_normal_sig

                should_send = is_startup or mirage_reset or normal_reset

                if should_send:
                    try:
                        await send_webhook(
                            session, json_data, data, timers,
                            mirage_reset=mirage_reset,
                            normal_reset=normal_reset,
                            is_startup=is_startup
                        )
                        if is_startup:
                            log("✅ Gửi stock khởi động thành công.")
                        else:
                            events = []
                            if mirage_reset:
                                events.append("Mirage reset")
                            if normal_reset:
                                events.append("Normal reset")
                            log(f"✅ Phát hiện {' + '.join(events)} — đã gửi webhook!")
                    except Exception as e:
                        log(f"❌ Lỗi gửi webhook: {e}")

                prev_mirage_sig = cur_mirage_sig
                prev_normal_sig = cur_normal_sig
                is_startup = False
            else:
                log("⚠️  Bỏ qua lần poll này do lỗi API.")

            await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
