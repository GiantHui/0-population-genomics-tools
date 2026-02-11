import googlemaps
import csv

# 替换为你的Google Maps API密钥
api_key = ''
gmaps = googlemaps.Client(key=api_key)

# 从文件中读取省份和市区列表
file_path = 'C:/Users/LuzHu/Desktop/地区.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    # 分割每一行来获取市区名称
    regions = [line.strip().split('\t')[1] for line in file if '\t' in line]

# 查询市区的经纬度并实时写入CSV
output_file = 'C:/Users/LuzHu/Desktop/result.csv'
with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # 写入标题行
    writer.writerow(['Region', 'Latitude', 'Longitude'])
    
    for region in regions:
        geocode_result = gmaps.geocode(region)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            writer.writerow([region, location['lat'], location['lng']])
            print(f"Processed {region},{location}")
        else:
            writer.writerow([region, None, None])
            print(f"Processed {region}, no location found")
        csvfile.flush()

print("Data has been saved to CSV.")


