```html
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>div+css实现frameset效果</title>
<style type="text/css">
.header{border-bottom:1px solid #ccc;margin-bottom:5px;}
.MainContainer{min-width:960px;max-width:1600px;}
.sidebar{width:180px;float:left;margin-right:-180px;border-right:1px solid #ccc;min-height:500px;padding:5px;}
.main{float:left;margin-left:200px;padding:5px;}
.content{padding:0 10px;}
</style>
</head>
<body>

    <div class="page">
        <div class="header">
            <div id="title">
                <h1>顶部</h1>
            </div>
        </div>
        <div class="MainContainer">
            <div class="sidebar">
            边栏
            </div>
            <div  id="main" class="main">
                内容
            </div>           
        </div>
    </div>
</body>
</html>
```