import asyncio
from playwright.async_api import async_playwright
import time
import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

async def kiem_thu_ui():
    danh_sach_cau_hoi = [
        "Bé nhà em 3 tuổi bị sốt 38.5 độ, em cho uống Paracetamol được không? Liều lượng bao nhiêu?",
        "Tôi bị cao huyết áp, đang nghẹt mũi quá định mua Decolgen uống cho đỡ, có sao không?",
        "Tôi đang dùng thuốc tiểu đường Metformin, hôm nay nhức đầu quá uống thêm Panadol được không?",
        "Cho em hỏi thuốc dạ dày Omeprazol thì uống trước ăn hay sau ăn ạ?",
        "Bạn có thể tóm tắt cho tôi bộ phim Avengers mới nhất được không?"
    ]

    ket_qua = []
    print("Bắt đầu kiểm thử giao diện bằng Playwright...")

    async with async_playwright() as p:
        trinh_duyet = await p.chromium.launch(headless=True)
        trang = await trinh_duyet.new_page()

        print("Đang mở http://localhost:3000/ ...")
        await trang.goto("http://localhost:3000/")
        await trang.wait_for_selector("input[type='text']")

        for i, cau_hoi in enumerate(danh_sach_cau_hoi):
            print(f"\n[{i+1}/{len(danh_sach_cau_hoi)}] Gửi câu hỏi: {cau_hoi}")
            
            # Nhập câu hỏi và nhấn Enter
            await trang.fill("input[type='text']", cau_hoi)
            
            # Khởi tạo watcher cho network response trước khi nhấn Enter
            async with trang.expect_response(lambda response: "/api/v1/chat/" in response.url and response.request.method == "POST", timeout=60000) as response_info:
                await trang.press("input[type='text']", "Enter")
            
            print("Đang đợi API trả về...")
            response = await response_info.value
            json_data = await response.json()
            noi_dung_tra_loi = json_data.get("message", "")
            canh_bao = json_data.get("warnings", [])
            
            print(f"Bot trả lời: {noi_dung_tra_loi[:150]}...")
            if canh_bao:
                print(f"Cảnh báo: {canh_bao}")
            
            ket_qua.append({
                "cau_hoi": cau_hoi,
                "tra_loi": noi_dung_tra_loi,
                "canh_bao": canh_bao
            })
            
            await trang.wait_for_timeout(2000)

        await trinh_duyet.close()

    print("\n=== TỔNG KẾT KẾT QUẢ KIỂM THỬ ===")
    with open("ket_qua_kiem_thu.json", "w", encoding="utf-8") as f:
        json.dump(ket_qua, f, ensure_ascii=False, indent=2)
    print("Đã lưu kết quả vào ket_qua_kiem_thu.json")

if __name__ == "__main__":
    asyncio.run(kiem_thu_ui())
