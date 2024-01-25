<script>
import pinia from "@/store/store.js";
import { useMainStore } from "@/store/index.js";
import { storeToRefs } from "pinia";

const mainStore = useMainStore(pinia);

// console.log(mainStore.posts);
const { postType, typeColor } = storeToRefs(mainStore);
export default {
  props: ["article", "user"],
  data() {
    return {
      postType,
      typeColor,
    };
  },
  computed: {
    getContent() {
      // console.log(this.article.content)
      var re = new RegExp("<[^<>]+>", "g");
      var text = this.article.content.replace(re, "");
      // console.log(text);
      if (text.length >= 80) {
        text = text.substring(0, 80);
      }
      // console.log(text);
      return text;
    },
    getDate() {
      // console.log(this.article.createtime);
      var text = this.article.createtime.substring(0, 17);
      return text;
    },
    // getType() {
    //   return this.postType[this.article.type];
    // },
  },
  methods: {
    storeArticle(articleid) {
      // console.log(article);
      window.localStorage.setItem("articleid", JSON.stringify(articleid));
    },
  },
};
</script>


<template>
  <!-- 文章卡片 -->
  <div class="card p-4 mb-4">
    <!-- 开启网格系统 -->
    <div class="row">
      <!-- 文章标题(大屏幕占5列,其他屏幕占12列) -->
      <div class="col-lg-5">
        <!-- 文章所属类别 -->
        <a
          class="badge me-2"
          href="#"
          :class="this.typeColor[this.article.type]"
        >
          <i class="bi bi-circle-fill"></i>
          {{ postType[article.type] }}
        </a>
        <!-- {{article.type}} -->

        <!-- 文章标题 -->
        <h4 class="card-title mt-3">
          <!-- <a href="/article/{{article.articleid}}"> {{ article.headline }}</a> -->
          <a href="/read" @click="storeArticle(article.articleid)">
            {{ article.headline }}</a
          >
        </h4>

        <!-- 作者信息 -->
        <div class="author d-flex flex-row align-items-center mt-4">
          <!-- 头像 -->
          <div class="avatar me-2">
            <img
              src="src/assets/img/avatar.jpg"
              alt="avatar-img"
              class="rounded-circle avatar-img"
            />
          </div>
          <!-- 昵称 -->
          <div>
            <a href="#" class="fw-bold">{{ user.nickname }}</a>
            <ul class="nav">
              <li class="nav-item me-3 sm-txt">
                发布于: {{ getDate }}
                <!-- Feb 12,2020 -->
              </li>

              <li class="nav-item sm-txt">
                <i class="bi bi-book-fill me-1"></i>阅读数:
                {{ article.readcount }} 次
              </li>

              <li class="nav-item sm-txt">消耗积分：{{ article.credit }} 分</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 文章摘要 -->
      <div class="col-md-6 col-lg-4 card-text p-1">
        <p class="text-secondary lh-lg">
          {{ getContent }}
        </p>
      </div>

      <!-- 文章图片 -->
      <div class="col-md-6 col-lg-3">
        <img
          src="src/assets/img/thumb.png"
          alt="Card-img"
          class="w-100 rounded-3"
        />
      </div>
    </div>
  </div>
</template>