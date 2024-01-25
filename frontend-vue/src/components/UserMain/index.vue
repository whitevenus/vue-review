<script>
import axios from "axios";
import pinia from "@/store/store.js";
import { useMainStore } from "@/store/index.js";
import { storeToRefs } from "pinia";

const mainStore = useMainStore(pinia);

// console.log(mainStore.posts);
const { session } = storeToRefs(mainStore);

export default {
  data() {
    return {
      session,
      result: [],
    };
  },
  methods: {
    getFavorite() {
      axios.get("/api/ucenter").then(
        (Response) => {
        //   console.log("请求成功了.", Response.data);
          this.result = Response.data.result;
        },
        (err) => {
          console.log("请求失败了", err.message);
        }
      );
    },
  },

  mounted() {
    this.getFavorite();
  },
};
</script>


<template>
  <main>
    <div class="container">
      <div class="d-flex align-items-start">
        <div
          class="
            col-2
            nav
            flex-column
            nav-pills
            me-3
            border
            p-4
            rounded rounded-3
          "
          style="height: 400px"
          id="v-pills-tab"
          role="tablist"
          aria-orientation="vertical"
        >
          <button
            @click="getArticle()"
            class="nav-link active"
            id="v-pills-favorite-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-favorite"
            type="button"
            role="tab"
            aria-controls="v-pills-favorite"
            aria-selected="true"
          >
            我的收藏
          </button>
          <button
            class="nav-link"
            id="v-pills-post-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-post"
            type="button"
            role="tab"
            aria-controls="v-pills-post"
            aria-selected="false"
            v-if="session['role'] == 'user'"
          >
            我要投稿
          </button>

          <template v-if="session['role'] == 'editor'">
            <button
              class="nav-link"
              id="v-pills-prepost-tab"
              data-bs-toggle="pill"
              data-bs-target="#v-pills-prepost"
              type="button"
              role="tab"
              aria-controls="v-pills-prepost"
              aria-selected="false"
            >
              发布文章
            </button>

            <button
              class="nav-link"
              id="v-pills-draft-tab"
              data-bs-toggle="pill"
              data-bs-target="#v-pills-draft"
              type="button"
              role="tab"
              aria-controls="v-pills-draft"
              aria-selected="false"
            >
              我的草稿
            </button>
          </template>

          <button
            class="nav-link"
            id="v-pills-article-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-article"
            type="button"
            role="tab"
            aria-controls="v-pills-article"
            aria-selected="false"
          >
            我的文章
          </button>

          <button
            class="nav-link"
            id="v-pills-comment-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-comment"
            type="button"
            role="tab"
            aria-controls="v-pills-comment"
            aria-selected="false"
          >
            我的评论
          </button>
          <button
            class="nav-link"
            id="v-pills-info-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-info"
            type="button"
            role="tab"
            aria-controls="v-pills-info"
            aria-selected="false"
          >
            个人资料
          </button>

          <button
            class="nav-link"
            id="v-pills-credit-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-credit"
            type="button"
            role="tab"
            aria-controls="v-pills-credit"
            aria-selected="false"
          >
            我的积分
          </button>
        </div>

        <div class="col-10 tab-content border" id="v-pills-tabContent">
          <div
            class="tab-pane fade show active"
            id="v-pills-favorite"
            role="tabpanel"
            aria-labelledby="v-pills-favorite-tab"
          >
            <table class="table">
              <thead>
                <tr>
                  <th width="10%" class="text-center">编号</th>
                  <th width="60%" class="text-center">标题</th>
                  <th width="8%" class="text-center">浏览</th>
                  <th width="8%" class="text-center">评论</th>
                  <th width="14%" class="text-center">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in result" :key="index">
                  <td align="center">{{ item.article.articleid }}</td>
                  <td>
                    <a
                      href="/article/{{item.article.articleid}}"
                      target="_blank"
                      >{{ item.article.headline }}</a
                    >
                  </td>
                  <td align="center">{{ item.article.readcount }}</td>
                  <td align="center">{{ item.article.replycount }}</td>
                  <td align="center">
                    <a
                      href="#"
                      onclick="switchFavorite(this, {{item.favorite.favoriteid}})"
                    >
                      <span
                        class="text-primary"
                        v-if="item.favorite.canceled == 0"
                        >取消收藏</span
                      >
                      <span class="text-danger" v-else>继续收藏</span>
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div
            class="tab-pane fade"
            id="v-pills-post"
            role="tabpanel"
            aria-labelledby="v-pills-post-tab"
          >
            我要投稿页面
          </div>
          <div
            class="tab-pane fade"
            id="v-pills-prepost"
            role="tabpanel"
            aria-labelledby="v-pills-prepost-tab"
          >
            发布文章页面
          </div>
          <div
            class="tab-pane fade"
            id="v-pills-draft"
            role="tabpanel"
            aria-labelledby="v-pills-draft-tab"
          >
            我的草稿页面
          </div>
          <div
            class="tab-pane fade"
            id="v-pills-article"
            role="tabpanel"
            aria-labelledby="v-pills-article-tab"
          >
            我的文章页面
          </div>

          <div
            class="tab-pane fade"
            id="v-pills-comment"
            role="tabpanel"
            aria-labelledby="v-pills-comment-tab"
          >
            我的评论页面
          </div>

          <div
            class="tab-pane fade"
            id="v-pills-info"
            role="tabpanel"
            aria-labelledby="v-pills-info-tab"
          >
            个人资料页面
          </div>

          <div
            class="tab-pane fade"
            id="v-pills-credit"
            role="tabpanel"
            aria-labelledby="v-pills-credit-tab"
          >
            我的积分页面
          </div>
        </div>
      </div>
    </div>
  </main>
</template>