<!-- map_visualization.js (optional if you prefer external JS) -->
<script src="https://cesium.com/downloads/cesiumjs/releases/1.85/Build/Cesium/Widgets/widgets.js"></script>
<script src="https://cesium.com/downloads/cesiumjs/releases/1.85/Build/Cesium/Cesium.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.85/Build/Cesium/Widgets/widgets.css" rel="stylesheet">

<script>
    const viewer = new Cesium.Viewer('cesiumContainer');
    viewer.entities.add({
        name: 'Landing Site',
        position: Cesium.Cartesian3.fromDegrees(-75.59777, 40.03883),
        point: { pixelSize: 10, color: Cesium.Color.RED }
    });
</script>
