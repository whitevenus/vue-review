<script>
import axios from "axios";
import pinia from "@/store/store.js";
import { useMainStore } from "@/store/index.js";
import { storeToRefs } from "pinia";
import commentComponent from "@/components/CommentComponent/index.vue";

const mainStore = useMainStore(pinia);

// console.log(mainStore.posts);
const { postType, session } = storeToRefs(mainStore);
export default {
  components: {
    commentComponent,
  },

  data() {
    return {
      article: "",
      position: "",
      payed: "",
      // user: "",
      postType,
      session,
      is_favorite: "",
      prev_next: {},
      comment_user: {},
    };
  },
  computed: {
    getDate() {
      // console.log(this.article.createtime);
      if (this.article.createtime) {
        var text = this.article.createtime.substring(0, 17);
        return text;
      }
      return "";
    },
    // ifRead() {
    //   return
    // }
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
    readAll() {
      // 构建POST请求参数
      var param =
        "article_id=" + this.article.articleid + "&position=" + this.position;
      // console.log(param)
      // console.log(this.article.content)
      $.post("/api/readall", param, function (data) {
        // console.log(data)
        $("#content").append(data);
        $(".readall").hide(); // 读取完成后隐藏阅读全文按钮
      });
    },

    addFavorite(articleid) {
      $.post("/api/favorite", "article_id=" + articleid, function (data) {
        if (data == "not-login") {
          bootbox.alert({
            title: "错误提示",
            message: "你还没有登录，不能收藏文章.",
          });
        } else if (data == "favorite-pass") {
          // bootbox.alert({
          //   title: "信息提示",
          //   message: "文章收藏成功，可在我的收藏中查看.",
          // });

          this.is_favorite = false;
          console.log(this.is_favorite);
          // 取消收藏后，延迟0.5秒钟重新刷新当前页面
          setTimeout("location.reload();", 500);
          // // 修改当前元素的内容
          // $(".favorite-btn").html(
          //   '<i class="bi bi-heart-fill me-1"></i> 感谢收藏'
          // );
          // // 解除当前元素的单击事件，使其无法进行任何单击操作
          // $(".favorite-btn").attr("onclick", "").unbind("click");
        } else if (data == "favorite-fail") {
          bootbox.alert({
            title: "错误提示",
            message: "收藏文章出错，请联系管理员.",
          });
        }
      });
    },

    cancelFavorite(articleid) {
      console.log(articleid);
      $.ajax({
        url: "/api/favorite/" + articleid,
        type: "delete", // 发送DELETE请求
        success: function (data) {
          if (data == "not-login") {
            bootbox.alert({
              title: "错误提示",
              message: "你还没有登录，不能收藏文章.",
            });
          } else if (data == "cancel-pass") {
            // bootbox.alert({ title: "信息提示", message: "取消收藏成功." });
            this.is_favorite = false;
            console.log(this.is_favorite);
            // 取消收藏后，延迟0.5秒钟重新刷新当前页面
            setTimeout("location.reload();", 500);
            // $(".favorite-btn").html('<span class="oi oi-heart aria-hidden="true"></span> 欢迎再来');
            // $(".favorite-btn").attr('onclick', '').unbind('click');
          } else if (data == "cancel-fail") {
            bootbox.alert({
              title: "错误提示",
              message: "取消收藏出错，请联系管理员.",
            });
          }
        },
      });
    },

    storeArticle(articleid) {
      // console.log(article);
      window.localStorage.setItem("articleid", JSON.stringify(articleid));
    },
  },
  created() {
    // console.log(window.localStorage.getItem("article"));
    var articleid = JSON.parse(window.localStorage.getItem("articleid"));
    // console.log(this.article.articleid);
    axios.get("/api/article/" + `${articleid}`).then(
      (Response) => {
        // console.log("请求成功了", Response.data);
        this.article = Response.data.article;
        this.position = Response.data.position;
        this.payed = Response.data.payed;
        this.is_favorite = Response.data.is_favorite;
        this.prev_next = Response.data.prev_next;
        this.comment_user = Response.data.comment_user;
        // console.log(this.comment_user)
        // this.user = Response.data.user;
      },
      (error) => {
        console.log("请求出错了", error.message);
      }
    );
  },
  // unmounted() {
  //   // console.log(window.localStorage.getItem("article"))
  //   // window.localStorage.setItem("article", JSON.stringify(""))
  // }
};
</script>

<template>
  <div class="col-sm-9 col-12">
    <div class="col-12 border mb-4 p-5">
      <div class="mb-4 row">
        <div class="col-9 fs-3 fw-bold">
          {{ article.headline }}
          <!-- {{ this.article.headline }} -->
        </div>

        <!-- <div class="col-3">
          <label> <i class="bi bi-heart-fill me-2"></i> 收藏本文 </label>
        </div> -->
      </div>

      <div class="col-12 text-secondary">
        作者：{{ article.nickname }} 类别: {{ postType[article.type] }} 日期：{{
          getDate
        }}
        阅读：{{ article.readcount }} 消耗积分：{{ article.credit }} 分
      </div>

      <hr />

      <div v-html="article.content" class="col-12 my-4" id="content"></div>

      <div class="col-12 readall" v-if="article.credit > 0 && payed == false">
        <button
          class="col-sm-10 col-12"
          @click="readAll()"
          v-if="session.isLogin"
        >
          <span class="oi oi-data-transfer-download" aria-hidden="true"></span>
          阅读全文（消耗积分：{{ article.credit }}）
        </button>

        <button class="col-sm-10 col-12" @click="showLogin()" v-else>
          <span class="oi oi-data-transfer-download" aria-hidden="true"></span>
          你还未登录，在此登陆后可阅读全文
        </button>
      </div>

      <div class="col-12 d-flex justify-content-end">
        <label class="me-3" v-if="article.userid == session.userid">
          <i class="bi bi-pencil-square me-1"></i> 编辑内容
        </label>

        <label
          class="favorite-btn"
          v-if="is_favorite == true"
          @click="cancelFavorite(article.articleid)"
          ><i class="bi bi-heart-fill me-1"></i> 取消收藏
        </label>

        <label
          class="favorite-btn"
          v-else
          @click="addFavorite(article.articleid)"
          ><i class="bi bi-heart me-1"></i> 收藏本文
        </label>
      </div>
    </div>

    <div class="col-12 border mb-4 p-4">
      <!-- <div>
        版权所有，转载本站文章请注明出处：蜗牛笔记，
        http://www.woniunote.com/article/1
      </div> -->
      <div>
        上一篇：
        <a href="/read" @click="storeArticle(prev_next.prev_id)">{{
          prev_next.prev_headline
        }}</a>
      </div>
      <div>
        下一篇：
        <a href="/read" @click="storeArticle(prev_next.next_id)">{{
          prev_next.next_headline
        }}</a>
      </div>
    </div>

    <comment-component
      :session="session"
      :article="article"
      :com_user="comment_user"
    ></comment-component>
  </div>
</template>