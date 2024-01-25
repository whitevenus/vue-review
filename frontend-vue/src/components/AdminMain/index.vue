<script>
import axios from "axios";

export default {
  data() {
    return {
      result: [],
      page: [],
      total: 0,
    };
  },
  methods: {
    getArticle() {
      axios.get("/api/admin").then(
        (Response) => {
          //   console.log("请求成功了.", Response.data);
          this.result = Response.data.result;
          this.page = Response.data.page;
          this.total = Response.data.total;
        },
        (err) => {
          console.log("请求失败了", err.message);
        }
      );
    },

    getArticle_(page) {
      axios.get("/api/admin/article/" + page).then(
        (Response) => {
          // console.log("请求成功了.", Response.data);
          this.result = Response.data.result;
          this.page = Response.data.page;
          this.total = Response.data.total;
        },
        (err) => {
          console.log("请求失败了", err.message);
        }
      );
    },

    // 为了直接展示搜索结果，不需要使用Ajax，而是直接跳转页面
    doSearchByType() {
      var type = $("#type").val();

      axios.get("/api/admin/type/" + type + "-1").then(
        (Response) => {
          // console.log("请求成功了.", Response.data);
          this.result = Response.data.result;
          this.page = Response.data.page;
          this.total = Response.data.total;
        },
        (err) => {
          console.log("请求失败了", err.message);
        }
      );
    },

    doSearchByHeadline() {
      var keyword = $("#keyword").val();

      axios.get("/api/admin/search/" + keyword).then(
        (Response) => {
          // console.log("请求成功了.", Response.data);
          this.result = Response.data.result;
          this.page = Response.data.page;
          this.total = Response.data.total;
        },
        (err) => {
          console.log("请求失败了", err.message);
        }
      );
    },

    switchHide(obj, articleid) {
      $.get("/api/admin/article/hide/" + articleid, function (data) {
        if (data == "1") {
          $(obj).html('<span class="text-danger">已隐</sapn>');
        } else {
          $(obj).text('<span class="text-primary">隐藏</span>');
        }
        setTimeout("location.reload();", 500);
      });
    },

    switchRecommend(obj, articleid) {
      $.get("/api/admin/article/recommend/" + articleid, function (data) {
        if (data == "1") {
          $(obj).html('<span class="text-danger">已推</sapn>');
        } else {
          $(obj).text('<span class="text-primary">推荐</span>');
        }
        setTimeout("location.reload();", 500);
      });
    },
    switchCheck(obj, articleid) {
      $.get("/api/admin/article/check/" + articleid, function (data) {
        if (data == "0") {
          $(obj).html('<span class="text-danger">待审</span>');
        } else {
          $(obj).text('<span class="text-primary">已审</span>');
        }
        setTimeout("location.reload();", 500);
      });
    },
  },

  mounted() {
    this.getArticle();
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
            id="v-pills-article-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-article"
            type="button"
            role="tab"
            aria-controls="v-pills-article"
            aria-selected="true"
          >
            文章管理
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
            评论管理
          </button>
          <button
            class="nav-link"
            id="v-pills-user-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-user"
            type="button"
            role="tab"
            aria-controls="v-pills-user"
            aria-selected="false"
          >
            用户管理
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
            积分管理
          </button>

          <button
            class="nav-link"
            id="v-pills-favorite-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-favorite"
            type="button"
            role="tab"
            aria-controls="v-pills-favorite"
            aria-selected="false"
          >
            收藏管理
          </button>

          <button
            class="nav-link"
            id="v-pills-recommend-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-recommend"
            type="button"
            role="tab"
            aria-controls="v-pills-recommend"
            aria-selected="false"
          >
            推荐管理
          </button>
          <button
            class="nav-link"
            id="v-pills-hide-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-hide"
            type="button"
            role="tab"
            aria-controls="v-pills-hide"
            aria-selected="false"
          >
            隐藏管理
          </button>

          <button
            class="nav-link"
            id="v-pills-check-tab"
            data-bs-toggle="pill"
            data-bs-target="#v-pills-check"
            type="button"
            role="tab"
            aria-controls="v-pills-check"
            aria-selected="false"
          >
            投稿审核
          </button>
        </div>

        <div class="col-10 tab-content border" id="v-pills-tabContent">
          <div
            class="tab-pane fade show active"
            id="v-pills-article"
            role="tabpanel"
            aria-labelledby="v-pills-article-tab"
          >
            <div class="col-12 row p-3">
              <div class="col-3">
                <!-- 根据article_type字典对象填充分类下拉框 -->
                <select id="type" class="form-select">
                  <option selected value="0">所有分类</option>
                  <option value="1">PHP开发</option>
                  <option value="2">Java开发</option>
                  <option value="3">Python开发</option>
                  <option value="4">Web前端</option>
                  <option value="5">测试开发</option>
                  <option value="6">数据科学</option>
                  <option value="7">网络安全</option>
                  <option value="8">蜗牛杂谈</option>
                  <!-- {% for key, value in article_type.items() %}
                  <option value="{{ key }}">{{ value }}</option>
                  {% endfor %} -->
                </select>
              </div>
              <div class="col-2">
                <input
                  type="button"
                  class="btn btn-primary"
                  value="分类搜索"
                  @click="doSearchByType()"
                />
              </div>
              <div class="col-2"></div>
              <div class="col-3">
                <input type="text" class="form-control" id="keyword" />
              </div>
              <div class="col-2">
                <input
                  type="button"
                  class="btn btn-primary"
                  value="标题搜索"
                  @click="doSearchByHeadline()"
                />
              </div>
            </div>

            <table class="table">
              <thead>
                <tr>
                  <th width="10%" class="text-center">编号</th>
                  <th width="50%" class="text-center">标题</th>
                  <th width="8%" class="text-center">浏览</th>
                  <th width="8%" class="text-center">评论</th>
                  <th width="24%" class="text-center">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(article, index) in result" :key="index">
                  <th class="text-center">{{ article.articleid }}</th>
                  <td>
                    <a
                      class="text-primary"
                      href="/article/{{ article.articleid }}"
                      target="_blank"
                      >{{ article.headline }}</a
                    >
                  </td>
                  <td class="text-center">{{ article.readcount }}</td>
                  <td class="text-center">{{ article.replycount }}</td>
                  <td>
                    <a
                      class="me-2 text-primary"
                      href="/edit/{{ article.articleid }}"
                      target="_blank"
                    >
                      编辑
                    </a>
                    <a
                      class="me-2"
                      href="javascript:void(0)"
                      @click="switchRecommend(this, article.articleid)"
                    >
                      <span class="text-primary" v-if="article.recommended == 0"
                        >推荐</span
                      >
                      <span class="text-danger" v-else>已推</span></a
                    >
                    <a
                      class="me-2"
                      href="javascript:void(0)"
                      @click="switchHide(this, article.articleid)"
                    >
                      <span class="text-primary" v-if="article.hidden == 0"
                        >隐藏</span
                      >
                      <span class="text-danger" v-else>已隐</span></a
                    >
                    <a
                      href="javascript:void(0)"
                      @click="switchCheck(this, article.articleid)"
                    >
                      <span class="text-primary" v-if="article.checked == 1"
                        >已审</span
                      >
                      <span class="text-danger" v-else>待审</span>
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>

            <table class="table">
              <tr>
                <td valign="middle" align="center">
                  <a
                    href="javascript:void(0)"
                    v-if="page == 1"
                    class="me-2"
                    @click="getArticle_(page)"
                    >上一页</a
                  >
                  <a
                    href="javascript:void(0)"
                    v-else
                    class="me-2"
                    @click="getArticle_(page - 1)"
                    >上一页</a
                  >

                  <a
                    href="javascript:void(0)"
                    class="me-2"
                    v-for="i in total"
                    @click="getArticle_(i)"
                    >{{ i }}</a
                  >

                  <a
                    href="javascript:void(0)"
                    v-if="page == total"
                    @click="getArticle_(page)"
                    >下一页</a
                  >

                  <a
                    href="javascript:void(0)"
                    v-else
                    @click="getArticle_(page + 1)"
                    >下一页</a
                  >
                </td>
              </tr>
            </table>
          </div>

          <div
            class="tab-pane fade"
            id="v-pills-comment"
            role="tabpanel"
            aria-labelledby="v-pills-comment-tab"
          >
            评论管理页面
          </div>
          <div
            class="tab-pane fade"
            id="v-pills-user"
            role="tabpanel"
            aria-labelledby="v-pills-user-tab"
          >
            用户管理页面
          </div>
          <div
            class="tab-pane fade"
            id="v-pills-credit"
            role="tabpanel"
            aria-labelledby="v-pills-credit-tab"
          >
            积分管理页面
          </div>
          <div
            class="tab-pane fade"
            id="v-pills-favorite"
            role="tabpanel"
            aria-labelledby="v-pills-favorite-tab"
          >
            收藏管理页面
          </div>

          <div
            class="tab-pane fade"
            id="v-pills-recommend"
            role="tabpanel"
            aria-labelledby="v-pills-recommend-tab"
          >
            推荐管理页面
          </div>

          <div
            class="tab-pane fade"
            id="v-pills-hide"
            role="tabpanel"
            aria-labelledby="v-pills-hide-tab"
          >
            隐藏管理页面
          </div>

          <div
            class="tab-pane fade"
            id="v-pills-check"
            role="tabpanel"
            aria-labelledby="v-pills-check-tab"
          >
            投稿审核页面
          </div>
        </div>
      </div>
    </div>
  </main>
</template>