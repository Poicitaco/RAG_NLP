# SafeRAG Pharma - Frontend

Đây là giao diện của ứng dụng SafeRAG Pharma, được xây dựng bằng Next.js (App Router) và TailwindCSS.

## Hướng dẫn chạy thử (Local)

1. Cài đặt thư viện: `npm install`
2. Chạy môi trường dev: `npm run dev`
3. Mở [http://localhost:3000](http://localhost:3000)

*Lưu ý: Bạn cần chạy Backend FastAPI ở cổng `8000` trước khi sử dụng.*

## Hướng dẫn Deploy lên Vercel

1. Đẩy thư mục `frontend-next` này lên một Repository trên GitHub.
2. Đăng nhập vào [Vercel](https://vercel.com/) và tạo project mới từ Repository đó.
3. Trong phần cấu hình **Environment Variables** của Vercel, hãy thêm biến sau:
   - `NEXT_PUBLIC_API_URL`: Điền địa chỉ IP/Domain public của con Backend (Ví dụ: `https://api.saferag.com/api/v1`).
   
*(Lưu ý: Nếu không cấu hình biến này, ứng dụng sẽ mặc định trỏ về `http://localhost:8000/api/v1` và sẽ không hoạt động với người dùng bên ngoài Internet).*
