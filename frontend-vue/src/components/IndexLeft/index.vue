<script>
import ArticleCard from "@/components/ArticleCard/index.vue";
import CarouselBox from "@/components/CarouselBox/index.vue";
import axios from "axios";

import pinia from "@/store/store.js";
import { useMainStore } from "@/store/index.js";
import { storeToRefs } from "pinia";

const mainStore = useMainStore(pinia);

// console.log(mainStore.posts);
const { posts, page, total, type } = storeToRefs(mainStore);

export default {
  components: { ArticleCard, CarouselBox },
  data() {
    return {
      posts,
      page,
      total,
      type
    };
  },
  methods: {
    getPost(page) {
      // console.log(page);
      mainStore.page = page;
      axios.get("/api/page/" + `${page}`).then(
        (Response) => {
          // console.log("请求成功了.", Response.data);
          mainStore.posts = Response.data.result;
          // console.log(this.posts);
        },
        (err) => {
          console.log("请求失败了", err.message);
        }
      );
    },
    getPost_(page) {
      // console.log(page);
      mainStore.page = page;
      axios.get("/api/type/" + `${this.type}-${page}`).then(
        (Response) => {
          // console.log("请求成功了.", Response.data);
          mainStore.posts = Response.data.result;
          // console.log(this.posts);
        },
        (err) => {
          console.log("请求失败了", err.message);
        }
      );
    },
  },
  mounted() {
    // console.log(mainStore.posts)
    axios.get("http://localhost:8080/api/get_index_article").then(
      (Response) => {
        // console.log("请求成功了.", Response.data);
        mainStore.posts = Response.data.result;
        mainStore.total = Response.data.total;
        // console.log(mainStore.posts);
        // console.log(this.posts);
      },
      (err) => {
        console.log("请求失败了", err.message);
      }
    );
  },
};
</script>


<template>
  <!-- 左侧 -->
  <div class="col-12 col-md-9">
    <!-- 幻灯片区域 -->
    <section class="mb-4">
      <!-- 幻灯片盒子组件 -->
      <carousel-box></carousel-box>
    </section>

    <!-- 文章列表区域 -->
    <section class="mb-4">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <!-- 文章卡片组件 -->
            <article-card
              v-for="(item, index) in posts"
              :key="index + 1"
              :user="item.user"
              :article="item.article"
            ></article-card>

            <nav aria-label="Page navigation example" v-if="total > 10">
              <ul class="pagination justify-content-center">
                <li class="page-item" v-if="page == 1">
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost(1)"
                    >上一页</a
                  >
                </li>
                <li class="page-item" v-else>
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost(page - 1)"
                    >上一页</a
                  >
                </li>
                <li class="page-item" v-for="n in total">
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost(n)"
                    >{{ n }}</a
                  >
                </li>

                <li class="page-item" v-if="page == total">
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost(page)"
                    >下一页</a
                  >
                </li>
                <li class="page-item" v-else>
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost(page + 1)"
                    >下一页</a
                  >
                </li>
              </ul>
            </nav>

            <nav aria-label="Page navigation example" v-else>
              <ul class="pagination justify-content-center">
                <li class="page-item" v-if="page == 1">
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost_(1)"
                    >上一页</a
                  >
                </li>
                <li class="page-item" v-else>
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost_(page - 1)"
                    >上一页</a
                  >
                </li>
                <li class="page-item" v-for="n in total">
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost_(n)"
                    >{{ n }}</a
                  >
                </li>

                <li class="page-item" v-if="page == total">
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost_(page)"
                    >下一页</a
                  >
                </li>
                <li class="page-item" v-else>
                  <a
                    class="page-link"
                    href="javascript:void(0)"
                    @click="getPost_(page + 1)"
                    >下一页</a
                  >
                </li>
              </ul>
            </nav>

            <!-- <div class="col-12 paginate">
              <a href="#">上一页</a>&nbsp;&nbsp; <a href="#">1</a>&nbsp;&nbsp;
              <a href="#">2</a>&nbsp;&nbsp; <a href="#">3</a>&nbsp;&nbsp;
              <a href="#">4</a>&nbsp;&nbsp; <a href="#">5</a>&nbsp;&nbsp;
              <a href="#">下一页</a>
            </div>

            <button type="button" class="btn btn-primary w-100">
              加载更多<i class="bi bi-arrow-down-circle ms-2"></i>
            </button> -->
          </div>
        </div>
      </div>
    </section>
  </div>
</template>