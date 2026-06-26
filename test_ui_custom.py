import asyncio
from playwright.async_api import async_playwright
import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

async def kiem_thu_ui_custom():
    danh_sach_cau_hoi = [
        "Trẻ 5 tuổi bị ho có đờm thì nên uống thuốc gì?",
        "Tôi đang uống thuốc dạ dày Nexium, có uống kèm với thuốc cảm Tiffy được không?",
        "Liều dùng Paracetamol 500mg cho người lớn là như thế nào?",
        "Phụ nữ có thai 3 tháng đầu bị đau đầu có uống được Panadol không?",
        "Thời tiết hôm nay ở Hà Nội thế nào?",
        "Uống thuốc kháng sinh Amoxicillin có bị đau dạ dày không?",
        "Người bị suy thận có dùng được thuốc Ibuprofen không?",
        "Chỉ định và chống chỉ định của thuốc Aspirin là gì?"
    ]

    ket_qua = []
    print("Bắt đầu kiểm thử giao diện bằng Playwright với các câu hỏi tự tạo...")

    async with async_playwright() as p:
        trinh_duyet = await p.chromium.launch(headless=True)
        trang = await trinh_duyet.new_page()

        print("Đang mở http://localhost:3000/ ...")
        await trang.goto("http://localhost:3000/")
        
        # Use a more specific locator by placeholder
        input_locator = trang.get_by_placeholder("Bạn muốn hỏi về thuốc gì?")
        await input_locator.wait_for()

        for i, cau_hoi in enumerate(danh_sach_cau_hoi):
            print(f"\n[{i+1}/{len(danh_sach_cau_hoi)}] Gửi câu hỏi: {cau_hoi}")
            
            # Fill the input using press_sequentially
            await input_locator.fill("")
            await input_locator.press_sequentially(cau_hoi, delay=10)
            
            await trang.wait_for_timeout(500)
            
            async with trang.expect_response(lambda response: "/api/v1/chat" in response.url and response.request.method == "POST", timeout=60000) as response_info:
                # Sometimes clicking the button explicitly is safer
                await trang.locator("button[type='submit']").click()
            
            print("Đang đợi API trả về...")
            response = await response_info.value
            try:
                json_data = await response.json()
            except Exception as e:
                print(f"Lỗi phân tích JSON: {e}")
                json_data = {}
                
            noi_dung_tra_loi = json_data.get("message", "")
            canh_bao = json_data.get("warnings", [])
            
            print(f"Bot trả lời: {noi_dung_tra_loi[:200]}...")
            if canh_bao:
                print(f"Cảnh báo: {canh_bao}")
            
            ket_qua.append({
                "cau_hoi": cau_hoi,
                "tra_loi": noi_dung_tra_loi,
                "canh_bao": canh_bao
            })
            
            await trang.wait_for_timeout(2000)

        await trinh_duyet.close()

    print("\n=== TỔNG KẾT KẾT QUẢ KIỂM THỬ TÙY CHỈNH ===")
    with open("ket_qua_kiem_thu_custom.json", "w", encoding="utf-8") as f:
        json.dump(ket_qua, f, ensure_ascii=False, indent=2)
    print("Đã lưu kết quả vào ket_qua_kiem_thu_custom.json")

if __name__ == "__main__":
    asyncio.run(kiem_thu_ui_custom())
