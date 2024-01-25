<script>
export default {
  props: ["user", "comment", "session", "article"],
  // data() {
  //   return {
  //     session
  //   }
  // }
  // computed: {
  //   condation() {
  //     return article.userid == session.userid || session.role == 'admin' || comment.userid == session.userid
  //   }
  // }
};
</script>


<template>
  <!-- <div class="col-12 list row"> -->
  <div class="col-12 row mb-4 border p-2">
    <div class="col-2 icon">
      <img
        src="@/assets/img/avatar.jpg"
        class="img-fluid"
        style="width: 70px"
      />
    </div>
    <div class="col-10 comment">
      <div class="col-12 row" style="padding: 0px">
        <div class="col-7 commenter">
          {{ user.nickname }} {{ comment.createtime.substring(0, 26) }}
        </div>

        <div class="col-5 reply">
          <template
            v-if="
              article.userid == session.userid ||
              session.role == 'admin' ||
              comment.userid == session.userid
            "
          >
            <label @click="gotoReply(comment.commentid)" class="me-3"
              ><i class="bi bi-pencil-square me-1"></i> 回复
            </label>
            <label @click="hideComment(this, comment.commentid)"
              ><i class="bi bi-aspect-ratio-fill me-1"></i>隐藏
            </label>
          </template>

          <template v-else>
            <label @click="gotoReply(comment.commentid)" class="me-3"
              ><i class="bi bi-pencil-square me-1"></i> 回复
            </label>
            <label @click="agreeComment(this, comment.commentid)" class="me-3">
              <!-- <span v-if="session.isLogin"></span> -->
              <i class="bi bi-hand-thumbs-up me-1"></i>
              赞成 (<span>{{ comment.agreecount }}</span
              >)
            </label>
            <label @click="opposeComment(this, comment.commentid)" class="me-3">
              <span class="oi oi-x" aria-hidden="true"> </span>
              <i class="bi bi-hand-thumbs-down me-1"></i>反对 (<span>{{
                comment.opposecount
              }}</span
              >)
            </label>
          </template>
        </div>
      </div>
      <div class="col-12 content mt-2">
        {{ comment.content }}
      </div>
    </div>
  </div>
</template>