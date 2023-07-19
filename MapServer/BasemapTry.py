import folium

# 创建地图对象
map = folium.Map(location=[39.9087, 116.3974], zoom_start=14)  # 设置初始地图中心点和缩放级别

# 添加起点和终点标记
folium.Marker(location=[39.9087, 116.3974], popup='故宫').add_to(map)
folium.Marker(location=[39.9927, 116.3075], popup='圆明园').add_to(map)

# 添加路线
route = folium.PolyLine(locations=[[39.9087, 116.3974], [39.9857, 116.3264], [39.9872, 116.3302], [39.9904, 116.3288], [39.9927, 116.3075]], color='blue')
map.add_child(route)

# 显示地图
map
