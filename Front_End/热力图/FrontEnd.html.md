```html
<!DOCTYPE HTML>
<html>
<head>
  <title>加载海量点</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
  <style type="text/css">
    html,body{
        margin:0;
        width:100%;
        height:100%;
        background:#ffffff;
    }
    #map{
        width:100%;
        height:100%;
    }

  </style>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=your_api_key"></script>


<script type="text/javascript" src="data.json"></script>
//data.json内容
//var data = {"data":[[74.438,39.006,1],...]}


</head>
<body>
    <div id="map"></div>
    <script type="text/javascript">
    var map = new BMap.Map("map", {});                        // 创建Map实例
    map.centerAndZoom(new BMap.Point(105.000, 38.000), 5);     // 初始化地图,设置中心点坐标和地图级别
    map.enableScrollWheelZoom();                        //启用滚轮放大缩小
    if (document.createElement('canvas').getContext) {  // 判断当前浏览器是否支持绘制海量点
        var options = {
            size: BMAP_POINT_SIZE_SMALLER,
            shape: BMAP_POINT_SHAPE_CIRCLE,
            color: 'red'
        }
        var pointCollection = new BMap.PointCollection(points, options);  // 初始化PointCollection
        pointCollection.addEventListener('click', function (e) {
          alert('单击点的坐标为：' + e.point.lng + ',' + e.point.lat);  // 监听点击事件
        });
        map.addOverlay(pointCollection);  // 添加Overlay
    } else {
        alert('请在chrome、safari、IE8+以上浏览器查看本示例');
    }
  </script>
</body>
</html>
```