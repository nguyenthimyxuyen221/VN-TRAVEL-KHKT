# 🇻🇳 Bản đồ Du lịch Việt Nam - 34 Tỉnh Thành

> **Bản đồ tương tác hiển thị 34 tỉnh/thành phố Việt Nam sau sáp nhập theo Nghị quyết 202/2025/QH15, kèm theo 136 địa điểm du lịch tiêu biểu.**

![React](https://img.shields.io/badge/React-19.1.0-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-6.3.5-646CFF?logo=vite)
![D3.js](https://img.shields.io/badge/D3.js-7.9-F9A03C?logo=d3.js)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.1-06B6D4?logo=tailwindcss)

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Demo](#-demo)
- [Cài đặt](#-cài-đặt)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [Dữ liệu](#-dữ-liệu)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Tùy chỉnh](#-tùy-chỉnh)
- [Đóng góp](#-đóng-góp)

---

## 🎯 Giới thiệu

Dự án **Bản đồ Du lịch Việt Nam** là một ứng dụng web tương tác được xây dựng bằng React và D3.js, cho phép người dùng:

- Khám phá bản đồ hành chính Việt Nam với **34 tỉnh/thành phố** sau sáp nhập
- Xem thông tin chi tiết về từng tỉnh: diện tích, dân số, mật độ, danh sách xã/phường
- Khám phá **136 địa điểm du lịch tiêu biểu** trên khắp cả nước
- Tìm kiếm nhanh tỉnh/thành phố theo tên

### Bối cảnh

Theo **Nghị quyết 202/2025/QH15** của Quốc hội, Việt Nam thực hiện sáp nhập các đơn vị hành chính, giảm từ 63 tỉnh/thành xuống còn **34 tỉnh/thành phố** với tổng cộng **3.321 xã/phường/đặc khu**.

---

## ✨ Tính năng

### 🗺️ Bản đồ tương tác
- **Zoom & Pan**: Phóng to, thu nhỏ và di chuyển bản đồ mượt mà
- **Hover effect**: Hiệu ứng khi di chuột qua các tỉnh
- **Click để xem chi tiết**: Nhấn vào tỉnh để xem thông tin đầy đủ

### 📍 Địa điểm du lịch
- **136 điểm du lịch** được đánh dấu trên bản đồ bằng marker đỏ
- **Thông tin chi tiết**: Tên, mô tả, loại hình du lịch
- **Link Google Maps**: Dẫn đường trực tiếp đến địa điểm
- **Bật/tắt hiển thị**: Toggle để ẩn/hiện các điểm du lịch

### 🔍 Tìm kiếm
- Tìm kiếm tỉnh/thành phố theo tên (hỗ trợ tiếng Việt không dấu)
- Kết quả hiển thị realtime

### 📱 Responsive
- Giao diện tối ưu cho cả desktop và mobile
- Panel thông tin tự động điều chỉnh vị trí

### 📊 Thông tin tỉnh/thành
- Tên tỉnh/thành phố
- Loại hình (Tỉnh / Thành phố trực thuộc TƯ)
- Thông tin sáp nhập từ các tỉnh cũ
- Diện tích (km²)
- Dân số (người)
- Mật độ dân số (người/km²)
- **Danh sách đầy đủ các xã/phường**

---

## 🖥️ Demo

### Giao diện chính
```
┌─────────────────────────────────────────────────────────────┐
│  ┌──────────────┐                                           │
│  │ DANH SÁCH    │         🗺️ BẢN ĐỒ VIỆT NAM              │
│  │ 34 TỈNH      │                                           │
│  │              │         ● Điểm du lịch                    │
│  │ 🔍 Tìm kiếm  │         ○ Tỉnh/Thành phố                  │
│  │              │                                           │
│  │ □ An Giang   │              ┌─────────────┐              │
│  │ □ Bắc Ninh   │              │ THÔNG TIN   │              │
│  │ □ Cà Mau     │              │ TỈNH/ĐỊA    │              │
│  │ □ ...        │              │ ĐIỂM        │              │
│  │              │              └─────────────┘              │
│  └──────────────┘                                           │
│                              [+][-][Toàn VN]                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Cài đặt

### Yêu cầu hệ thống
- **Node.js** >= 18.x
- **npm** >= 9.x hoặc **yarn** >= 1.22

### Các bước cài đặt

```bash
# 1. Clone repository
git clone <repository-url>
cd "VN Travel"

# 2. Di chuyển vào thư mục dự án
cd vietnam-map

# 3. Cài đặt dependencies
npm install

# 4. Chạy development server
npm run dev

# 5. Mở trình duyệt tại
# http://localhost:5173
```

### Build production

```bash
# Build ứng dụng
npm run build

# Preview bản build
npm run preview
```

---

## 📁 Cấu trúc dự án

```
VN Travel/
├── 📄 README.md                    # File hướng dẫn này
├── 📄 tên các tỉnh.xlsx            # Dữ liệu gốc từ Excel
├── 📄 extract_travel.py            # Script Python trích xuất dữ liệu
├── 📄 VietnamMap34.jsx             # Component bản đồ gốc
│
└── 📁 vietnam-map/                 # Thư mục dự án React
    ├── 📄 package.json             # Dependencies & scripts
    ├── 📄 vite.config.js           # Cấu hình Vite
    ├── 📄 tailwind.config.js       # Cấu hình TailwindCSS
    ├── 📄 index.html               # HTML entry point
    │
    ├── 📁 public/                  # Static assets
    │
    └── 📁 src/
        ├── 📄 main.jsx             # React entry point
        ├── 📄 index.css            # Global styles + Tailwind
        ├── 📄 App.jsx              # Component chính (bản đồ)
        ├── 📄 travelData.json      # Dữ liệu 136 địa điểm du lịch
        └── 📄 provinceData.json    # Dữ liệu xã/phường các tỉnh
```

---

## 📖 Hướng dẫn sử dụng

### 1. Xem thông tin tỉnh/thành
1. **Click vào tỉnh** trên bản đồ hoặc trong danh sách bên trái
2. Panel thông tin sẽ hiển thị với:
   - Tên tỉnh/thành
   - Thông tin sáp nhập
   - Diện tích, dân số, mật độ
   - Danh sách các xã/phường (có thể scroll)

### 2. Khám phá địa điểm du lịch
1. Các **marker đỏ** trên bản đồ là địa điểm du lịch
2. **Click vào marker** để xem thông tin chi tiết
3. Nhấn **"Xem trên Google Maps"** để mở Google Maps

### 3. Điều khiển bản đồ
| Thao tác | Cách thực hiện |
|----------|----------------|
| Phóng to | Nút `+` hoặc scroll chuột lên |
| Thu nhỏ | Nút `-` hoặc scroll chuột xuống |
| Di chuyển | Kéo thả bản đồ |
| Reset view | Nút `Toàn VN` |

### 4. Tìm kiếm
- Nhập tên tỉnh vào ô tìm kiếm
- Hỗ trợ tìm kiếm không dấu (VD: "ha noi" → "Hà Nội")

### 5. Bật/tắt điểm du lịch
- Nhấn nút **"Ẩn điểm du lịch"** / **"Hiện điểm du lịch"** ở góc phải

---

## 📊 Dữ liệu

### Nguồn dữ liệu

| File | Mô tả | Số lượng |
|------|-------|----------|
| `tên các tỉnh.xlsx` | Dữ liệu gốc từ Excel | - |
| `travelData.json` | Địa điểm du lịch | 136 địa điểm |
| `provinceData.json` | Xã/phường các tỉnh | 34 tỉnh |
| `App.jsx` (DATA) | GeoJSON bản đồ | 34 tỉnh |

### Cấu trúc dữ liệu địa điểm du lịch

```json
{
  "province": "Tuyên Quang",
  "name": "Đèo Mã Pí Lèng",
  "description": "1. Đèo Mã Pí Lèng\nLoại: Danh lam thắng cảnh...",
  "image": "https://drive.google.com/file/d/xxx/view",
  "mapUrl": "https://www.google.com/maps/search/?api=1&query=...",
  "lat": 23.24062,
  "lng": 105.41208
}
```

### Cấu trúc dữ liệu xã/phường

```json
{
  "Tuyên Quang": "07 Phường: Phường Mỹ Lâm, Phường Minh Xuân...\n117 Xã: Thượng Lâm, Lâm Bình...",
  "Cao Bằng": "03 phường: Phường Thục Phán...\n53 xã: Quảng Lâm..."
}
```

### Cập nhật dữ liệu

Để cập nhật dữ liệu từ file Excel:

```bash
# 1. Cập nhật file "tên các tỉnh.xlsx"

# 2. Chạy script Python để trích xuất
cd "VN Travel"

# Trích xuất dữ liệu du lịch
python3 extract_travel.py > vietnam-map/src/travelData.json

# Trích xuất dữ liệu xã/phường
python3 extract_travel.py provinces > vietnam-map/src/provinceData.json
```

---

## 🛠️ Công nghệ sử dụng

### Frontend
| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| **React** | 19.1.0 | UI Framework |
| **Vite** | 6.3.5 | Build tool & Dev server |
| **D3.js** | 7.9.0 | Vẽ bản đồ & xử lý GeoJSON |
| **TailwindCSS** | 4.1.7 | Styling |

### Dữ liệu
| Công nghệ | Mục đích |
|-----------|----------|
| **Python** | Trích xuất dữ liệu từ Excel |
| **Pandas** | Xử lý file Excel |
| **GeoJSON** | Định dạng dữ liệu bản đồ |

---

## 🎨 Tùy chỉnh

### Thay đổi màu sắc tỉnh

Chỉnh sửa mảng `PAL` trong `App.jsx`:

```javascript
const PAL = [
  "#E8B4A0", "#A8C6A1", "#F2D8A7", // ... thêm màu
];
```

### Thay đổi kích thước bản đồ

```javascript
const W = 900;  // Chiều rộng
const H = 1000; // Chiều cao
```

### Thêm địa điểm du lịch mới

1. Cập nhật file `tên các tỉnh.xlsx`
2. Chạy lại script `extract_travel.py`
3. Hoặc thêm trực tiếp vào `travelData.json`

---

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

---

## 📝 License

Dự án này được phát triển cho mục đích học tập và tham khảo.

---

## 📞 Liên hệ

Nếu có câu hỏi hoặc góp ý, vui lòng tạo Issue trên repository.

---

<p align="center">
  Made with ❤️ for Vietnam Tourism 🇻🇳
</p>
