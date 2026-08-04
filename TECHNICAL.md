# 📐 Tài liệu Kỹ thuật - Bản đồ Du lịch Việt Nam

> **Tài liệu chi tiết về kiến trúc, thuật toán, và luồng xử lý của ứng dụng**

---

## 📋 Mục lục

- [Kiến trúc tổng quan](#-kiến-trúc-tổng-quan)
- [Luồng xử lý dữ liệu](#-luồng-xử-lý-dữ-liệu)
- [Thuật toán chính](#-thuật-toán-chính)
- [Chi tiết thành phần](#-chi-tiết-thành-phần)
- [Xử lý dữ liệu bản đồ GeoJSON](#-xử-lý-dữ-liệu-bản-đồ-geojson)
- [Quản lý trạng thái](#-quản-lý-trạng-thái)
- [Tối ưu hiệu năng](#-tối-ưu-hiệu-năng)

---

## 🏗️ Kiến trúc tổng quan

### Sơ đồ kiến trúc

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TẦNG GIAO DIỆN                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │ Panel trái  │  │  Bản đồ SVG │  │ Hộp thông   │  │  Điều      │ │
│  │ (Tìm kiếm + │  │  (D3.js +   │  │ tin (Tỉnh/  │  │  khiển     │ │
│  │  Danh sách) │  │   React)    │  │ Địa điểm)   │  │  (Zoom)    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         TẦNG XỬ LÝ LOGIC                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │
│  │  React Hooks    │  │  Động cơ D3.js  │  │  Xử lý dữ liệu      │  │
│  │  - useState     │  │  - geoMercator  │  │  - Khớp tỉnh        │  │
│  │  - useEffect    │  │  - geoPath      │  │  - Tính tọa độ      │  │
│  │  - useMemo      │  │  - zoom         │  │  - Lọc tìm kiếm     │  │
│  │  - useRef       │  │  - transform    │  │  - Chuẩn hóa chuỗi  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          TẦNG DỮ LIỆU                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │
│  │  Dữ liệu bản đồ │  │  Dữ liệu du     │  │  Dữ liệu xã/phường  │  │
│  │  GeoJSON        │  │  lịch (136 địa  │  │  (34 tỉnh)          │  │
│  │  (34 tỉnh)      │  │  điểm)          │  │                     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Cây thành phần

```
App (Thành phần gốc)
├── Panel trái
│   ├── Tiêu đề + Nút đóng
│   ├── Ô tìm kiếm
│   └── Danh sách tỉnh (đã lọc)
│
├── Vùng chứa bản đồ SVG
│   ├── <g> Nhóm biến đổi
│   │   ├── Đường viền tỉnh (34 cái)
│   │   ├── Nhãn tên tỉnh (34 cái)
│   │   └── Điểm đánh dấu du lịch (136 cái)
│   │
│   ├── Hộp thông tin tỉnh
│   ├── Hộp thông tin địa điểm
│   ├── Nút bật/tắt
│   └── Nút điều khiển zoom
│
└── Quản lý trạng thái (React Hooks)
```

---

## 🔄 Luồng xử lý dữ liệu

### 1. Luồng trích xuất dữ liệu (Python)

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  File Excel      │────▶│  Script Python   │────▶│  Các file JSON   │
│  (tên các        │     │  (extract_       │     │  - travelData    │
│   tỉnh.xlsx)     │     │   travel.py)     │     │  - provinceData  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

**Chi tiết xử lý trong `extract_travel.py`:**

```python
# 1. Đọc file Excel
df = pd.read_excel("tên các tỉnh.xlsx")

# 2. Điền tên tỉnh cho các dòng trống (lấy từ dòng trên)
df["Tỉnh/Thành phố sau sáp nhập"] = df["Tỉnh/Thành phố sau sáp nhập"].ffill()

# 3. Trích xuất tên địa điểm từ mẫu "1. Tên địa điểm\nLoại:..."
match = re.match(r"^\d+\.\s*(.+?)(?:\n|$)", str(khu_du_lich))

# 4. Trích xuất tọa độ từ đường dẫn Google Maps
# Mẫu: query=23.24062%2C105.41208
coord_match = re.search(r"query=([0-9.-]+)%2C([0-9.-]+)", str(vi_tri))
```

### 2. Luồng khởi tạo ứng dụng

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Nhập dữ    │────▶│  useMemo    │────▶│  useEffect  │────▶│  Hiển thị   │
│  liệu JSON  │     │  Tính toán  │     │  Thiết lập  │     │  bản đồ     │
│             │     │  phép chiếu │     │  D3 Zoom    │     │  SVG        │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### 3. Luồng tương tác người dùng

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TƯƠNG TÁC NGƯỜI DÙNG                              │
└─────────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│  Nhấn vào     │       │  Nhấn vào     │       │  Nhập tìm     │
│  tỉnh         │       │  điểm du lịch │       │  kiếm         │
└───────────────┘       └───────────────┘       └───────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ setSelected() │       │setSelectedTra │       │ setQuery()    │
│               │       │ vel()         │       │               │
└───────────────┘       └───────────────┘       └───────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│  Hiện hộp     │       │  Hiện hộp     │       │  Lọc danh     │
│  thông tin    │       │  thông tin    │       │  sách, vẽ     │
│  tỉnh         │       │  địa điểm     │       │  lại          │
└───────────────┘       └───────────────┘       └───────────────┘
```

---

## 🧮 Thuật toán chính

### 1. Thuật toán phép chiếu Mercator

**Mục đích:** Chuyển đổi tọa độ địa lý (kinh độ, vĩ độ) sang tọa độ điểm ảnh trên màn hình.

```javascript
// Khởi tạo phép chiếu với D3.js
const projection = d3.geoMercator()
  .fitExtent([[12, 12], [W - 12, H - 12]], DATA);

// fitExtent tự động tính toán:
// - scale: Tỷ lệ phóng đại phù hợp
// - translate: Vị trí dịch chuyển để căn giữa
```

**Công thức Mercator:**
```
x = λ (kinh độ)
y = ln(tan(π/4 + φ/2))  // φ = vĩ độ tính bằng radian
```

**Ví dụ:**
```javascript
// Tọa độ Hà Nội: [105.8342, 21.0278]
const [x, y] = projection([105.8342, 21.0278]);
// Kết quả: [450, 200] (tọa độ điểm ảnh)
```

### 2. Thuật toán tạo đường vẽ GeoPath

**Mục đích:** Chuyển đổi hình học GeoJSON thành chuỗi đường vẽ SVG.

```javascript
const path = d3.geoPath(projection);

// Đầu vào: Đối tượng GeoJSON
const feature = {
  type: "Feature",
  geometry: {
    type: "MultiPolygon",
    coordinates: [[[[103.49, 9.32], [103.50, 9.32], ...]]]
  }
};

// Đầu ra: Chuỗi đường vẽ SVG
const pathString = path(feature);
// "M 100,500 L 102,498 L 105,502 Z M 110,490 ..."
```

### 3. Thuật toán phóng to & di chuyển

**Cấu hình phóng to:**
```javascript
const zoom = d3.zoom()
  .scaleExtent([1, 16])           // Phóng nhỏ nhất: 1x, Phóng lớn nhất: 16x
  .translateExtent([[0, 0], [W, H]])  // Giới hạn di chuyển trong khung nhìn
  .on("zoom", (e) => setTransform(e.transform));
```

**Ma trận biến đổi:**
```javascript
// Đối tượng biến đổi zoom của D3
{
  k: 2.5,      // Hệ số tỷ lệ
  x: -150,     // Dịch chuyển theo X
  y: -200      // Dịch chuyển theo Y
}

// Áp dụng vào nhóm SVG
<g transform={`translate(${x},${y}) scale(${k})`}>
```

**Thuật toán phóng to vào đối tượng:**
```javascript
const zoomToFeature = (f) => {
  // 1. Tính hộp bao quanh của đối tượng
  const [[x0, y0], [x1, y1]] = path.bounds(f);
  
  // 2. Tính tỷ lệ để đối tượng vừa khung nhìn (80% khung nhìn)
  const scale = Math.min(
    14,  // Tỷ lệ tối đa
    0.8 / Math.max((x1 - x0) / W, (y1 - y0) / H)
  );
  
  // 3. Tính biến đổi để căn giữa đối tượng
  const t = d3.zoomIdentity
    .translate(W / 2, H / 2)           // Di chuyển gốc tọa độ ra giữa
    .scale(scale)                       // Áp dụng tỷ lệ
    .translate(-(x0 + x1) / 2, -(y0 + y1) / 2);  // Căn giữa đối tượng
  
  // 4. Tạo hiệu ứng chuyển động
  d3.select(svgRef.current)
    .transition()
    .duration(600)
    .call(zoomRef.current.transform, t);
};
```

### 4. Thuật toán chuẩn hóa chuỗi (Tìm kiếm tiếng Việt)

**Mục đích:** Cho phép tìm kiếm không dấu tiếng Việt.

```javascript
const strip = (s) =>
  s.normalize("NFD")                    // Tách dấu thành ký tự kết hợp
   .replace(/[\u0300-\u036f]/g, "")     // Xóa các ký tự dấu
   .replace(/đ/g, "d")                  // Thay đ → d
   .replace(/Đ/g, "D")                  // Thay Đ → D
   .toLowerCase();                       // Chuyển thành chữ thường

// Ví dụ:
strip("Hà Nội")     // → "ha noi"
strip("Đà Nẵng")    // → "da nang"
strip("Thừa Thiên") // → "thua thien"
```

**Phân tách Unicode NFD:**
```
"Hà" → "Ha" + "\u0300" (dấu huyền kết hợp)
normalize("NFD") tách dấu ra
replace loại bỏ dấu
```

### 5. Thuật toán khớp địa điểm du lịch với tỉnh

**Mục đích:** Gắn địa điểm du lịch vào đúng tỉnh trên bản đồ.

```javascript
const travelLocations = useMemo(() => {
  return travelData.map((loc, idx) => {
    // 1. Tìm tỉnh khớp trong dữ liệu GeoJSON
    const matchedFeature = DATA.features.find(f => {
      const provinceName = strip(f.properties.TinhThanh);
      const locProvince = strip(loc.province);
      // Khớp mờ: chứa lẫn nhau
      return provinceName.includes(locProvince) || 
             locProvince.includes(provinceName);
    });
    
    // 2. Tính tọa độ điểm ảnh
    let x, y;
    if (loc.lat && loc.lng) {
      // Có tọa độ chính xác từ Google Maps
      [x, y] = projection([loc.lng, loc.lat]);
    } else if (matchedFeature) {
      // Dùng tâm tỉnh + độ lệch để tránh chồng chéo
      const p = matchedFeature.properties;
      const provinceLocations = travelData.filter(
        l => strip(l.province) === strip(loc.province)
      );
      const locIndex = provinceLocations.findIndex(
        l => l.name === loc.name
      );
      
      // Mẫu độ lệch: lưới 3 cột
      const offsetX = (locIndex % 3 - 1) * 8;
      const offsetY = Math.floor(locIndex / 3) * 8;
      
      [x, y] = projection([
        p.lx + offsetX * 0.05,
        p.ly - offsetY * 0.05
      ]);
    }
    
    return { ...loc, id: idx, x, y, matchedProvince };
  }).filter(loc => loc.x && loc.y);  // Loại bỏ không hợp lệ
}, [projection]);
```

**Minh họa mẫu độ lệch:**
```
Với 9 địa điểm trong 1 tỉnh:
┌─────────────────┐
│  0    1    2    │   Hàng 0: độ lệch Y = 0
│  3    4    5    │   Hàng 1: độ lệch Y = 8
│  6    7    8    │   Hàng 2: độ lệch Y = 16
└─────────────────┘
   -8   0    8        độ lệch X
```

### 6. Thuật toán kích thước điểm đánh dấu thích ứng

**Mục đích:** Điều chỉnh kích thước điểm đánh dấu theo mức phóng to.

```javascript
const markerSize = Math.max(4, 8 / transform.k);

// transform.k = 1  → kích thước = 8px
// transform.k = 2  → kích thước = 4px (nhỏ nhất)
// transform.k = 4  → kích thước = 4px (nhỏ nhất)
// transform.k = 16 → kích thước = 4px (nhỏ nhất)
```

**Cỡ chữ thích ứng:**
```javascript
style={{
  fontSize: Math.max(5, 11 / transform.k),
  strokeWidth: 2.5 / transform.k,
}}

// Khi phóng to, chữ nhỏ lại để không che bản đồ
// Khi thu nhỏ, chữ lớn lên để vẫn đọc được
```

---

## 🧩 Chi tiết thành phần

### Cấu trúc thành phần App

```javascript
export default function App() {
  // ═══════════════════════════════════════════════════════════
  // QUẢN LÝ TRẠNG THÁI
  // ═══════════════════════════════════════════════════════════
  
  const [selected, setSelected] = useState(null);        // Tỉnh được chọn
  const [hovered, setHovered] = useState(null);          // Tỉnh đang rê chuột
  const [query, setQuery] = useState("");                // Từ khóa tìm kiếm
  const [transform, setTransform] = useState(d3.zoomIdentity);  // Trạng thái zoom
  const [panelOpen, setPanelOpen] = useState(true);      // Hiển thị panel trái
  const [showTravelSpots, setShowTravelSpots] = useState(true); // Hiển thị điểm du lịch
  const [selectedTravel, setSelectedTravel] = useState(null);   // Địa điểm được chọn
  
  const svgRef = useRef(null);   // Tham chiếu đến phần tử SVG
  const zoomRef = useRef(null);  // Tham chiếu đến hành vi zoom D3

  // ═══════════════════════════════════════════════════════════
  // TÍNH TOÁN GHI NHỚ (Tối ưu hiệu năng)
  // ═══════════════════════════════════════════════════════════
  
  const { path, projection } = useMemo(() => {
    // Chỉ tính 1 lần khi thành phần được gắn
    const projection = d3.geoMercator()
      .fitExtent([[12, 12], [W - 12, H - 12]], DATA);
    return { path: d3.geoPath(projection), projection };
  }, []);

  const feats = useMemo(() => 
    // Sắp xếp tỉnh theo thứ tự bảng chữ cái (tiếng Việt)
    [...DATA.features].sort((a, b) => 
      a.properties.TinhThanh.localeCompare(b.properties.TinhThanh, "vi")
    ),
  []);

  const travelLocations = useMemo(() => {
    // Gắn dữ liệu du lịch vào tọa độ màn hình
    // ... (xem thuật toán ở trên)
  }, [projection]);

  // ═══════════════════════════════════════════════════════════
  // HIỆU ỨNG PHỤ
  // ═══════════════════════════════════════════════════════════
  
  useEffect(() => {
    // Thiết lập hành vi zoom D3
    const svg = d3.select(svgRef.current);
    const zoom = d3.zoom()
      .scaleExtent([1, 16])
      .translateExtent([[0, 0], [W, H]])
      .on("zoom", (e) => setTransform(e.transform));
    
    svg.call(zoom);
    zoomRef.current = zoom;
    
    // Dọn dẹp
    return () => svg.on(".zoom", null);
  }, []);

  // ═══════════════════════════════════════════════════════════
  // HÀM XỬ LÝ SỰ KIỆN
  // ═══════════════════════════════════════════════════════════
  
  const zoomToFeature = (f) => { /* ... */ };
  const select = (f, zoom) => { /* ... */ };
  const resetView = () => { /* ... */ };

  // ═══════════════════════════════════════════════════════════
  // HIỂN THỊ
  // ═══════════════════════════════════════════════════════════
  
  return (
    <div className="flex w-full h-screen">
      {/* Panel trái */}
      {/* Bản đồ SVG */}
      {/* Các hộp thông tin */}
      {/* Điều khiển */}
    </div>
  );
}
```

---

## 🗺️ Xử lý dữ liệu bản đồ GeoJSON

### Cấu trúc GeoJSON

```javascript
const DATA = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      geometry: {
        type: "MultiPolygon",  // Nhiều polygon (đảo, vùng tách biệt)
        coordinates: [
          // Polygon 1 (mainland)
          [
            // Ring 1 (outer boundary)
            [[lng1, lat1], [lng2, lat2], ...],
            // Ring 2 (hole - nếu có)
            [[lng3, lat3], [lng4, lat4], ...]
          ],
          // Polygon 2 (island)
          [
            [[lng5, lat5], [lng6, lat6], ...]
          ]
        ]
      },
      properties: {
        Ma: "VN-01",           // Mã tỉnh
        TinhThanh: "Hà Nội",   // Tên tỉnh
        Loai: "Thành phố",     // Loại hình
        SapNhap: "Hà Nội, Hà Tây",  // Sáp nhập từ
        SoXa: 126,             // Số xã/phường
        Dtich_km2: 3358.6,     // Diện tích
        DanSo_ng: 8500000,     // Dân số
        MD_ngkm2: 2530,        // Mật độ
        lx: 105.8342,          // Label X (longitude)
        ly: 21.0278,           // Label Y (latitude)
        STT: 1                 // Số thứ tự (for color)
      }
    },
    // ... 33 features khác
  ]
};
```

### Hệ tọa độ

```
GeoJSON sử dụng hệ tọa độ WGS84:
- Kinh độ: -180 đến +180 (Đông dương, Tây âm)
- Vĩ độ: -90 đến +90 (Bắc dương, Nam âm)

Việt Nam:
- Kinh độ: ~102° đến ~110° Đông
- Vĩ độ: ~8° đến ~24° Bắc

Ví dụ: Hà Nội [105.8342, 21.0278]
       TP.HCM [106.6297, 10.8231]
```

---

## 📊 Quản lý trạng thái

### Sơ đồ luồng trạng thái

```
┌─────────────────────────────────────────────────────────────────────┐
│                       TRẠNG THÁI REACT                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │  selected   │    │selectedTrav │    │   query     │             │
│  │  (Province) │    │el (Travel)  │    │  (String)   │             │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘             │
│         │                  │                  │                      │
│         ▼                  ▼                  ▼                      │
│  ┌─────────────────────────────────────────────────────┐            │
│  │              TRẠNG THÁI DẪN XUẤT (Tính toán)           │            │
│  │  sp = selected?.properties                           │            │
│  │  giuNguyen = sp.SapNhap.split(",").length === 1     │            │
│  │  q = strip(query.trim())                             │            │
│  │  filteredFeats = feats.filter(...)                   │            │
│  └─────────────────────────────────────────────────────┘            │
│                                                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │  transform  │    │  panelOpen  │    │showTravel   │             │
│  │  (D3 Zoom)  │    │  (Boolean)  │    │Spots (Bool) │             │
│  └──────┬──────┘    └─────────────┘    └─────────────┘             │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────────────────────────────────────────────┐            │
│  │              BIẾN ĐỔI SVG                              │            │
│  │  <g transform={transform.toString()}>               │            │
│  │  // "translate(x,y) scale(k)"                       │            │
│  └─────────────────────────────────────────────────────┘            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Các mẫu cập nhật trạng thái

```javascript
// 1. Cập nhật trực tiếp
setSelected(feature);

// 2. Mẫu bật/tắt
setShowTravelSpots(!showTravelSpots);

// 3. Cập nhật có điều kiện
const select = (f, zoom) => {
  setSelected(f);
  if (zoom) zoomToFeature(f);
};

// 4. Mẫu đặt lại
const resetView = () => {
  setSelected(null);
  d3.select(svgRef.current)
    .transition()
    .duration(500)
    .call(zoomRef.current.transform, d3.zoomIdentity);
};

// 5. Loại trừ lẫn nhau
onClick={(e) => {
  e.stopPropagation();
  setSelectedTravel(loc);
  setSelected(null);  // Xóa lựa chọn tỉnh
}}
```

---

## ⚡ Tối ưu hiệu năng

### 1. useMemo cho các tính toán nặng

```javascript
// ❌ Không tốt: Tính lại mỗi lần vẽ
const projection = d3.geoMercator().fitExtent(...);

// ✅ Tốt: Tính một lần
const { path, projection } = useMemo(() => {
  const projection = d3.geoMercator().fitExtent(...);
  return { path: d3.geoPath(projection), projection };
}, []);  // Mảng rỗng = chạy một lần
```

### 2. Hiển thị có điều kiện

```javascript
// Chỉ vẽ khi cần
{showTravelSpots && travelLocations.map((loc) => (
  // Vẽ các điểm đánh dấu
))}

// Chỉ vẽ nhãn khi phóng to đủ lớn
{transform.k > 3 && (
  <text>{loc.name}</text>
)}
```

### 3. Ủy quyền sự kiện

```javascript
// ❌ Không tốt: Nhiều bộ lắng nghe sự kiện
{features.map(f => (
  <path onMouseEnter={() => setHovered(f.id)} />
))}

// ✅ Tốt hơn: Dùng ủy quyền sự kiện nếu có nhiều phần tử
// (Trong trường hợp này 34 đường vẽ là chấp nhận được)
```

### 4. Chuyển động CSS thay vì hoạt ảnh JS

```javascript
// Dùng CSS cho chuyển động đơn giản
className="transition-[fill-opacity] duration-150"

// Dùng chuyển động D3 cho hoạt ảnh phức tạp
d3.select(svgRef.current)
  .transition()
  .duration(600)
  .call(zoomRef.current.transform, t);
```

### 5. Tải hình ảnh chậm

```javascript
// Chỉ tải ảnh khi hộp thông tin mở
{selectedTravel && (
  <img src={getImageUrl(selectedTravel.image)} />
)}
```

---

## 🔧 Mẹo gỡ lỗi

### 1. Ghi lại trạng thái biến đổi

```javascript
useEffect(() => {
  console.log('Biến đổi:', {
    tyLe: transform.k,
    dichChuyenX: transform.x,
    dichChuyenY: transform.y
  });
}, [transform]);
```

### 2. Hiển thị hộp bao quanh

```javascript
// Thêm hình chữ nhật để gỡ lỗi hộp bao
const [[x0, y0], [x1, y1]] = path.bounds(feature);
<rect 
  x={x0} y={y0} 
  width={x1-x0} height={y1-y0}
  fill="none" stroke="red"
/>
```

### 3. Kiểm tra kết quả phép chiếu

```javascript
// Kiểm tra phép chiếu với tọa độ đã biết
console.log('Hà Nội:', projection([105.8342, 21.0278]));
console.log('TP.HCM:', projection([106.6297, 10.8231]));
```

---

## 📚 Tài liệu tham khảo

- [Phép chiếu địa lý D3.js](https://d3js.org/d3-geo/projection)
- [Đặc tả GeoJSON](https://geojson.org/)
- [Tài liệu React Hooks](https://react.dev/reference/react)
- [Lệnh đường vẽ SVG](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths)

---

<p align="center">
  <i>Phiên bản tài liệu: 1.0 | Cập nhật lần cuối: Tháng 7/2026</i>
</p>
