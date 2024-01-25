<script>


export default {

};
</script>


<template>
  <!-- 发布文章区域布局 -->
  <div class="container">
    <div class="row form-group mb-3">
      <label for="headline" class="col-1">文章标题</label>
      <input type="text" class="col-11" id="headline" />
    </div>

    <div class="row">
      <!--与UE绑定的元素在此引用，注意是script标签 -->
      <script
        id="content"
        name="content"
        type="text/plain"
        class="col-12"
      ></script>
    </div>

    <!-- <div class="row form-group">
                <label for="type" class="col-1">类型：</label>
                <select class="form-control col-2" id="type">
                    <option value="1">PHP开发</option>
                    <option value="2">Java开发</option>
                    <option value="3">Python开发</option>
                    <option value="4">Web前端</option>
                    <option value="5">测试开发</option>
                    <option value="6">数据科学</option>
                    <option value="7">网络安全</option>
                    <option value="8">蜗牛杂谈</option>
                </select>
                <label class="col-1"></label>
                <label for="credit" class="col-1">积分：</label>
                <select class="form-control col-2" id="credit">
                    <option value="0">免费</option>
                    <option value="1">1分</option>
                    <option value="2">2分</option>
                    <option value="5">5分</option>
                    <option value="10">10分</option>
                    <option value="20">20分</option>
                    <option value="50">50分</option>
                </select>
                <label class="col-1"></label>
                <button class="form-control btn-default col-2">保存草稿</button>
                <button class="form-control btn-primary col-2">发布文章</button>
                </select>
            </div> -->
  </div>
  <!--首先需要在页面中引入UEditor库，并初始化编辑器高度 -->
  <script type="text/javascript" src="../assets/ue/ueditor.config.js"></script>
  <script type="text/javascript" src="../assets/ue/ueditor.all.min.js"></script>
  <script
    type="text/javascript"
    src="../assets/ue/lang/zh-cn/zh-cn.js"
  ></script>


  
  </script>
</template>