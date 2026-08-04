import pandas as pd
import json
import re
import sys

df = pd.read_excel("tên các tỉnh.xlsx")

# Forward fill province names and xa/phuong data
df["Tỉnh/Thành phố sau sáp nhập"] = df["Tỉnh/Thành phố sau sáp nhập"].ffill()
df["Các xã/phường sau sáp nhập"] = df["Các xã/phường sau sáp nhập"].ffill()

# Extract province data with xa/phuong
province_data = {}
for _, row in df.iterrows():
    province = row["Tỉnh/Thành phố sau sáp nhập"]
    xa_phuong = row["Các xã/phường sau sáp nhập"]
    
    if province and pd.notna(xa_phuong) and province not in province_data:
        province_data[province] = str(xa_phuong)

# Extract travel locations
travel_data = []
for _, row in df.iterrows():
    province = row["Tỉnh/Thành phố sau sáp nhập"]
    khu_du_lich = row["Khu du lịch tiêu biểu"]
    hinh_anh = row["Hình ảnh"]
    vi_tri = row["Vị trí"]
    
    if pd.notna(khu_du_lich):
        # Extract name from "1. Name\nLoại:..." pattern
        match = re.match(r"^\d+\.\s*(.+?)(?:\n|$)", str(khu_du_lich))
        name = match.group(1).strip() if match else str(khu_du_lich)[:50]
        
        # Extract coordinates from Google Maps URL
        lat, lng = None, None
        if pd.notna(vi_tri):
            # Try to extract from query parameter
            coord_match = re.search(r"query=([0-9.-]+)%2C([0-9.-]+)", str(vi_tri))
            if coord_match:
                lat, lng = float(coord_match.group(1)), float(coord_match.group(2))
        
        travel_data.append({
            "province": province,
            "name": name,
            "description": str(khu_du_lich) if pd.notna(khu_du_lich) else "",
            "image": str(hinh_anh) if pd.notna(hinh_anh) else "",
            "mapUrl": str(vi_tri) if pd.notna(vi_tri) else "",
            "lat": lat,
            "lng": lng
        })

# Output based on argument
if len(sys.argv) > 1 and sys.argv[1] == "provinces":
    print(json.dumps(province_data, ensure_ascii=False, indent=2))
else:
    print(json.dumps(travel_data, ensure_ascii=False, indent=2))
