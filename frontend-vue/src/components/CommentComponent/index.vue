

<script>
import commentCard from "@/components/CommentCard/index.vue";

export default {
  props: ["article", "session", "com_user"],
  components: {
    commentCard,
  },
  methods: {
    // 显示模态框中的登录面板
    showLogin() {
      // console.log("打开登录面板")
      $("#login").addClass("active");
      $("#reg").removeClass("active");
      $("#loginpanel").addClass("active");
      $("#regpanel").removeClass("active");
      $("#mymodal").modal("show");
    },

    // 添加评论
    addComment(articleid) {
      var content = $.trim($("#comment").val());
      if (content.length < 5 || content.length > 1000) {
        bootbox.alert({
          title: "错误提示",
          message: "评论内容在5-1000字之间.",
        });
        return false;
      }
    //   console.log(articleid, content);
      var param = "article_id=" + articleid + "&content=" + content;
      console.log(param);

      $.post("/api/comment", param, function (data) {

        if (data == "content-invalid") {
          bootbox.alert({
            title: "错误提示",
            message: "评论内容在5-1000字之间.",
          });
        } else if (data == "add-limit") {
          bootbox.alert({
            title: "错误提示",
            message: "当天已用完5条评论的限额.",
          });
        } else if (data == "add-pass") {
          location.reload();
        } else {
          bootbox.alert({
            title: "错误提示",
            message: "发表评论出错，请联系管理员.",
          });
        }
      });
    },
  },

  // created() {
  //   console.log(this.com_user)
  // }
};
</script>


<template>

  <!-- 评论组件 -->
  <div class="col-12 border mb-4 p-4">
    <div class="col-12 row mb-2">
      <div class="col-sm-2 col-12">
        <label for="nickname">你的昵称：</label>
      </div>
      <div class="col-sm-10 col-12">
        <input
          type="text"
          class="form-control"
          id="nickname"
          v-if="session.isLogin"
          :value="session.nickname"
          readonly
        />

        <input
          type="text"
          class="form-control"
          id="nickname"
          v-else
          value="你还未登录,双击此处可登录."
          @dblclick="showLogin()"
          readonly
        />
      </div>
    </div>
    <div class="col-12 row mb-2">
      <div class="col-sm-2 col-12">
        <label for="comment">你的评论：</label>
      </div>
      <div class="col-sm-10 col-12">
        <textarea
          id="comment"
          class="form-control"
          placeholder="请在此留下你的真诚的、感人的、发自肺腑的赞美之词."
        ></textarea>
      </div>
    </div>

    <div class="col-12 row" style="margin-bottom: 20px">
      <div class="col-2"></div>
      <div class="col-sm-8 col-12" style="text-align: left; color: #888888">
        提示：登录后添加有效评论可享受积分哦！
      </div>

      <div class="col-sm-2 col-12" style="text-align: right">
        <button
          type="button"
          class="btn btn-primary"
          @click="addComment(article.articleid)"
          v-if="session.isLogin"
        >
          提交评论
        </button>
        <button
          type="button"
          class="btn btn-primary"
          @click="showLogin()"
          v-else
        >
          点击登录
        </button>
      </div>
    </div>

    <!-- <div class="col-12 row mb-4 border p-2">
      <div class="col-2 icon">
        <img
          src="@/assets/img/avatar.jpg"
          class="img-fluid"
          style="width: 70px"
        />
      </div>
      <div class="col-10 comment">
        <div class="col-12 row">
          <div class="col-7 commenter">强哥 2020-02-06 15:58:10</div>
          <div class="col-5 reply">
            <label>
              <span class="oi oi-chevron-bottom" aria-hidden="true"> </span>
              赞成 (<span>25</span>)
            </label>
            <label>
              <span class="oi oi-x" aria-hidden="true"> </span> 反对
              (<span>13</span>)
            </label>
          </div>
        </div>
        <div class="col-12 content">
          感谢作者的无私奉献，这是一条真诚表达谢意的评论;
        </div>
      </div>
    </div> -->

    <comment-card v-for="(item, index) in com_user" :user="item.user" :comment="item.article" :session="session" :article="article"></comment-card>
    <!-- {{ com_user }} -->
    <!-- <comment-card></comment-card>
    <comment-card></comment-card> -->
  </div>
</template>