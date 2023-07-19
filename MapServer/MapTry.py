import folium
import webbrowser

if __name__ == "__main__":
    # 创建地图对象
    map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

    # 添加标记
    folium.Marker(location=[51.5074, -0.1278], popup="London").add_to(map)
    folium.Marker(location=[48.8566, 2.3522], popup="Paris").add_to(map)

    # 保存地图为 HTML 文件
    map.save("map.html")

    # 在浏览器中打开 HTML 文件
    webbrowser.get("safari").open("map.html")

