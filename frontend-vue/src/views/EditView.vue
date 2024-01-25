<script>
// import EditHeader from "@/components/EditHeader/index.vue";

export default {
  data() {
    return {
      text: "",
    };
  },
  methods: {
    goHome() {
      window.location.href = "/";
    },

    handleUploadImage(event, insertImage, files) {
      // 拿到 files 之后上传到文件服务器，然后向编辑框中插入对应的内容
      console.log(files);

      // 此处只做示例
      insertImage({
        url: "upload/image/" + files[0].name + ".jpg",
        desc: files[0].name,
        // width: 'auto',
        // height: 'auto',
      });
    },

    doPost() {
      var headline = $.trim($("#headline").val());

      // console.log(headline)

      // var contentPlain = UE.getEditor("content").getContentTxt();
      var contentPlain = this.text;
      // console.log(contentPlain)

      if (headline.length < 5) {
        bootbox.alert({ title: "错误提示", message: "标题不能少于5个字" });
        return false;
      } else if (contentPlain.length < 100) {
        bootbox.alert({ title: "错误提示", message: "内容不能低于100个字" });
        return false;
      }

      var article_id = windows.localStorage.getItem("article_id");
      var param = "headline=" + headline;
      param += "&content=" + encodeURIComponent(contentPlain);
      param += "&type=" + $("#type").val();
      param += "&credit=" + $("#credit").val();
      param += "&drafted=0&checked=1&article_id=" + article_id;

      console.log(param);

      $.post("/api/article", param, function (data) {
        if (data == "perm-denied") {
          bootbox.alert({
            title: "错误提示",
            message: "权限不足，无法发布文章.",
          });
        } else if (data == "post-fail") {
          bootbox.alert({
            title: "错误提示",
            message: "文章发布失败，请联系管理员.",
          });
        } else if (data.match(/^\d+$/)) {
          bootbox.alert({
            title: "信息提示",
            message: "恭喜你，文章发布成功.",
          });
          window.localStorage.setItem("articleid", JSON.stringify(data));
          setTimeout(function () {
            location.href = "/read";
          }, 1000);
        } else {
          bootbox.alert({
            title: "错误提示",
            message: "文章发布失败，可能没有权限.",
          });
        }
      });
    },

    doDraft() {
      var headline = $.trim($("#headline").val());

      // console.log(headline)

      // var contentPlain = UE.getEditor("content").getContentTxt();
      var contentPlain = this.text;
      // console.log(contentPlain)

      if (headline.length < 5) {
        bootbox.alert({ title: "错误提示", message: "草稿标题不能少于5个字" });
        return false;
      } else if (contentPlain.length < 10) {
        bootbox.alert({ title: "错误提示", message: "草稿内容不能低于10个字" });
        return false;
      }

      var article_id = window.localStorage.getItem("article_id");
      var param = "headline=" + headline;

      param += "&content=" + encodeURIComponent(contentPlain);
      param += "&type=" + $("#type").val();
      param += "&credit=" + $("#credit").val();
      param += "&drafted=1&checked=1&article_id=" + article_id;
      $.post("/api/article", param, function (data) {
        if (data == "perm-denied") {
          bootbox.alert({
            title: "错误提示",
            message: "权限不足，无法保存草稿.",
          });
        } else if (data == "post-fail") {
          bootbox.alert({
            title: "错误提示",
            message: "保存草稿失败，请联系管理员.",
          });
        } else if (data.match(/^\d+$/)) {
          bootbox.alert({
            title: "信息提示",
            message: "恭喜你，草稿保存成功.",
          });
          // 保存草稿后，不跳转页面，重新为全局变量赋值。
          window.localStorage.setItem("article_id", JSON.stringify(data));
        } else {
          bootbox.alert({
            title: "错误提示",
            message: "保存草稿失败，可能没有权限.",
          });
        }
      });
    },
  },
  created() {
    window.localStorage.setItem("article_id", JSON.stringify(0));
  }
};
</script>


<template>
  <div id="main" class="container-fluid">
    <!-- <edit-header></edit-header> -->
    <div class="row mx-2">
      <div class="col-7">
        <label for="headline" class="visually-hidden">Headline</label>
        <input
          class="form-control form-control-lg border-0"
          type="text"
          placeholder="请输入文章标题..."
          aria-label=".form-control-lg example"
          id="headline"
        />
      </div>

      <div class="col-5 row align-items-center justify-content-between">
        <div class="col-auto ms-3">
          <label class="visually-hidden" for="type">类型</label>
          <select class="form-select form-select-sm" id="type">
            <option selected value="0">文章类型</option>
            <option value="1">PHP开发</option>
            <option value="2">Java开发</option>
            <option value="3">Python开发</option>
            <option value="4">Web前端</option>
            <option value="5">测试开发</option>
            <option value="6">数据科学</option>
            <option value="7">网络安全</option>
            <option value="8">蜗牛杂谈</option>
          </select>
        </div>

        <div class="col-auto">
          <label class="visually-hidden" for="credit">积分</label>
          <select class="form-select form-select-sm" id="credit">
            <option selected>积分</option>
            <option value="0">免费</option>
            <option value="1">1分</option>
            <option value="2">2分</option>
            <option value="5">5分</option>
            <option value="10">10分</option>
            <option value="20">20分</option>
            <option value="50">50分</option>
          </select>
        </div>

        <div class="col-auto">
          <button
            type="submit"
            class="btn border border-primary btn-sm me-3"
            @click="doDraft()"
          >
            保存草稿
          </button>
          <button
            type="submit"
            class="btn btn-primary btn-sm me-4"
            @click="doPost()"
          >
            发布
          </button>
          <button
            class="btn me-4 border-0 btn-sm btn-warning"
            @click="goHome()"
          >
            <i class="bi bi-house-door"></i>首页
          </button>
          <img
            src="src/assets/img/avatar.jpg"
            alt="avatar-img"
            class="rounded-circle avatar-edit my-1"
          />
        </div>
      </div>
    </div>

    <v-md-editor
      height="650px"
      :disabled-menus="[]"
      @upload-image="handleUploadImage"
      v-model="text"
    ></v-md-editor>
  </div>
</template>

<style>
</style>


