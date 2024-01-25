<script>
import axios from "axios";
import pinia from "@/store/store.js";
import { useMainStore } from "@/store/index.js";
import { storeToRefs } from "pinia";

const mainStore = useMainStore(pinia);

// console.log(mainStore.posts);
const { postType, session } = storeToRefs(mainStore);

export default {
  data() {
    return {
      postType,
      session,
      // islogin: false,
      // nickname: "张三",
    };
  },
  methods: {
    getPost(key) {
      axios.get("/api/type/" + `${key}-1`).then(
        (Response) => {
          // console.log("请求成功了.", Response.data);
          mainStore.posts = Response.data.result;
          mainStore.page = Response.data.page;
          mainStore.total = Response.data.total;
          mainStore.type = Response.data.type;
          // console.log(mainStore.total)
          // console.log(mainStore.page)
          // console.log(this.posts);
          // window.location.href = "/"
        },
        (err) => {
          console.log("请求失败了", err.message);
        }
      );
    },
    // 显示模态框中的登录面板
    showLogin() {
      // console.log("打开登录面板")
      $("#login").addClass("active");
      $("#reg").removeClass("active");
      $("#loginpanel").addClass("active");
      $("#regpanel").removeClass("active");
      $("#mymodal").modal("show");
    },

    //  显示模态框中的注册面板
    showReg() {
      $("#login").removeClass("active");
      $("#reg").addClass("active");
      $("#loginpanel").removeClass("active");
      $("#regpanel").addClass("active");
      $("#mymodal").modal("show");
    },
    doSendMail(obj) {
      var email = $.trim($("#regname").val());
      // 使用正则表达式验证邮箱地址格式是否正确
      if (!email.match(/.+@.+\..+/)) {
        bootbox.alert({ title: "错误提示", message: "邮箱地址格式不正确." });
        $("#regname").focus();
        return false;
      }
      // 如果邮件格式正确，则让发送邮件按钮变成不可用，避免二次操作
      $(obj).attr("disabled", true);

      $.post("/api/ecode", "email=" + email, function (data) {
        // console.log(data);
        if (data == "email-invalid") {
          bootbox.alert({ title: "错误提示", message: "邮箱地址格式不正确." });
          $("#regname").focus();
          return false;
        }
        if (data == "send-pass") {
          bootbox.alert({
            title: "信息提示",
            message: "邮箱验证码已成功发送，请查收.",
          });
          $("#regname").attr("disabled", true); // 验证码发送后禁止修改注册邮箱
          $(obj).attr("disabled", true); // 发送邮件按钮变成不可用
          return false;
        } else {
          bootbox.alert({
            title: "错误提示",
            message: "邮箱验证码未发送成功.",
          });
          return false;
        }
      });
    },
    doReg(e) {
      if (e != null && e.keyCode != 13) {
        return false;
      }

      var regname = $.trim($("#regname").val());
      var regpass = $.trim($("#regpass").val());
      var regcode = $.trim($("#regcode").val());
      if (!regname.match(/.+@.+\..+/) || regpass.length < 5) {
        bootbox.alert({
          title: "错误提示",
          message: "注册邮箱不正确或密码少于5位.",
        });
        return false;
      } else {
        // 构建POST请求的正文数据
        var param = "username=" + regname;
        param += "&password=" + regpass;
        param += "&ecode=" + regcode;
        // 利用jQuery框架发送POST请求，并获取到后台注册接口的响应内容
        $.post("/api/user", param, function (data) {
          // console.log(data);
          if (data["info"] == "ecode-error") {
            bootbox.alert({ title: "错误提示", message: "验证码无效." });
            $("#regcode").val(""); // 清除验证码框的值
            $("#regcode").focus(); // 让验证码框获取到焦点供用户输入
          } else if (data["info"] == "up-invalid") {
            bootbox.alert({
              title: "错误提示",
              message: "用户名和密码不能少于5位.",
            });
          } else if (data["info"] == "user-repeated") {
            bootbox.alert({
              title: "错误提示",
              message: "该用户名已经被注册.",
            });
            $("#regname").focus();
          } else if (data["info"] == "reg-pass") {
            bootbox.alert({ title: "信息提示", message: "恭喜你，注册成功." });

            // console.log(data["session"]);

            mainStore.session = data["session"];
            // console.log(mainStore.session);
            window.localStorage.setItem(
              "session",
              JSON.stringify(mainStore.session)
            );
            // console.log(window.localStorage.getItem("session"));

            // $("#mymodal").modal("hide");
            // 注册成功后，延迟1秒钟重新刷新当前页面
            setTimeout("location.reload();", 1000);
          } else if (data == "reg-fail") {
            bootbox.alert({
              title: "错误提示",
              message: "注册失败，请联系管理员.",
            });
          }
        });
      }
    },
    doLogin(e) {
      if (e != null && e.keyCode != 13) {
        return false;
      }

      var loginname = $.trim($("#loginname").val());
      var loginpass = $.trim($("#loginpass").val());
      var logincode = $.trim($("#logincode").val());
      if (loginname.length < 5 || loginpass.length < 5) {
        bootbox.alert({ title: "错误提示", message: "用户名或密码少于5位." });
        return false;
      } else {
        // 构建POST请求的正文数据
        var param = "username=" + loginname;
        param += "&password=" + loginpass;
        param += "&vcode=" + logincode;
        // 利用jQuery框架发送POST请求，并获取到后台登录接口的响应内容
        $.post("/api/login", param, function (data) {
          console.log(data);
          if (data["info"] == "vcode-error") {
            bootbox.alert({ title: "错误提示", message: "验证码无效." });
            $("#logincode").val(""); // 清除验证码框的值
            $("#logincode").focus(); // 让验证码框获取到焦点供用户输入
          } else if (data["info"] == "login-pass") {
            bootbox.alert({ title: "信息提示", message: "恭喜你，登录成功." });

            // console.log(data["session"]);

            mainStore.session = data["session"];
            // console.log(mainStore.session);
            window.localStorage.setItem(
              "session",
              JSON.stringify(mainStore.session)
            );
            // console.log(window.localStorage.getItem("session"));

            // 注册成功后，延迟1秒钟重新刷新当前页面
            setTimeout("location.reload();", 1000);
          } else if (data["info"] == "login-fail") {
            bootbox.alert({
              title: "错误提示",
              message: "登录失败，请确认用户名和密码是否正确.",
            });
          }
        });
      }
    },
    logout() {
      axios.get("/api/logout").then(
        (Response) => {
          // console.log("请求成功了.", Response.data);
          window.localStorage.setItem("session", JSON.stringify(""));
          // 注销后，延迟1秒钟重新刷新当前页面
          setTimeout("location.reload();", 1000);
        },
        (err) => {
          console.log("请求失败了", err.message);
        }
      );
    },
  },
  created() {
    // console.log(mainStore.session);
    // console.log(this.session);
    if (window.localStorage.getItem("session")) {
      mainStore.session = JSON.parse(window.localStorage.getItem("session"));
    }
  },
};
</script>


<template>
  <!-- 导览列 Start -->
  <header
    class="p-4 navbar fixed-top navbar-expand-lg bg-body navbar-light shadow-sm"
  >
    <!-- 定宽容器 -->
    <div class="container">
      <!-- Logo Start -->
      <a class="navbar-brand text-primary" href="/">
        <img
          src="@/assets/icon/bootstrap.svg"
          alt="Logo"
          width="30"
          height="25"
        />
        <strong>蜗牛笔记</strong>
      </a>
      <!-- Logo End -->

      <!-- 当屏幕小于lg断点对应的尺寸时,就会只显示折叠按钮,将data-bs-target属性值对应的元素给隐藏起来 -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarCollapsiable"
        aria-controls="navbarCollapsiable"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- id为navbarCollapisable的div盒子 -->
      <div class="collapse navbar-collapse" id="navbarCollapsiable">
        <!-- Search Start -->
        <form class="d-flex ms-2" role="search">
          <input
            class="form-control me-2"
            type="search"
            placeholder="搜索文章"
            aria-label="Search"
          />
          <button class="btn btn-outline-primary" type="submit">Search</button>
        </form>
        <!-- Search End -->

        <!-- 导航条目 Start-->
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="/"
              ><i class="bi bi-house-heart-fill me-2"></i>首页</a
            >
          </li>

          <!-- 下拉选单 Start -->
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#dropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
              ><i class="bi bi-archive me-2"></i>
              文章分类
            </a>

            <ul class="dropdown-menu">
              <li>
                <a
                  class="dropdown-item"
                  href="javascript:void(0)"
                  v-for="(value, key) in postType"
                  :key="key"
                  @click="getPost(key)"
                  >{{ value }}</a
                >
              </li>
            </ul>
          </li>
          <!-- 下拉选单 End -->

          <!-- <li class="nav-item">
              <a href="#" class="nav-link"
                ><i class="bi bi-currency-exchange me-2"></i>捐助</a
              >
            </li> -->

          <template v-if="session['isLogin']">


            <a class="nav-item nav-link" href="/admin" v-if="session['role'] == 'admin'"
              ><i class="bi bi-file-person me-2">系统管理</i></a
            >

            <a class="nav-item nav-link" href="/user" v-else
              ><i class="bi bi-file-person me-2">用户中心</i></a
            >


            <a class="nav-item nav-link" href="javascript:void(0)"
              >欢迎你：{{ session["nickname"] }}</a
            >
            <a
              class="nav-item nav-link"
              href="javascript:void(0)"
              @click="logout()"
              >注销</a
            >
          </template>

          <template v-else>
            <a
              class="nav-item nav-link"
              href="#"
              data-bs-toggle="modal"
              @click="showLogin()"
              >登录</a
            >
            <a
              class="nav-item nav-link"
              href="#"
              @click="showReg()"
              data-bs-toggle="modal"
              >注册</a
            >
          </template>
        </ul>
      </div>
      <!-- 导航条目 End -->
    </div>
  </header>
  <!-- 导览列 End -->

  <!-- 登录和注册模态框 -->
  <!-- data-backdrop="static" 表示用户必须要手工关闭模态框才能操作其他页面 -->
  <!-- 点击登入弹出Modal组件 -->
  <div
    class="modal fade"
    id="mymodal"
    tabindex="-1"
    data-bs-backdrop="static"
    aria-labelledby="mymodalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <!-- 模态框组件头部 -->
        <div class="modal-header">
          <!-- 配置tab组件 -->
          <ul class="nav nav-tabs" role="tablist">
            <li class="nav-item active" id="login">
              <a href="#loginpanel" class="nav-link" data-bs-toggle="tab"
                >登入</a
              >
            </li>
            <li class="nav-item" id="reg">
              <a href="#regpanel" class="nav-link" data-bs-toggle="tab">注册</a>
            </li>
          </ul>
          <!-- <h5 class="modal-title" id="exampleModalLabel">Modal title</h5> -->
          <!-- 关闭Modal组件的按钮（右上角） -->
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>

        <!-- tab组件内容，内部包含Modal组件的body部分 -->
        <div class="tab-content">
          <!-- 绘制登录窗口 -->
          <div class="tab-pane container active" id="loginpanel">
            <div class="modal-body">
              <div class="form-floating mb-3 row">
                <input
                  type="email"
                  class="form-control"
                  id="loginname"
                  placeholder="name@example.com"
                />
                <label for="loginname">登入邮箱地址</label>
              </div>

              <div class="form-floating mb-3 row">
                <input
                  type="password"
                  class="form-control"
                  id="loginpass"
                  placeholder="Password"
                />
                <label for="loginpass">登入密码</label>
              </div>

              <div class="row mb-3 row">
                <div class="form-floating col-9 p-0 pe-1">
                  <input
                    type="text"
                    class="form-control"
                    id="logincode"
                    placeholder="键入邮箱地址"
                  />
                  <label for="logincode">图片验证码</label>
                </div>

                <div class="col-3">
                  <img
                    src="/api/vcode"
                    id="loginvcode"
                    style="cursor: pointer"
                  />
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-dark" data-dismiss="modal">
                关闭
              </button>
              <button
                type="button"
                class="btn btn-primary"
                @click="doLogin(null)"
              >
                登录
              </button>
            </div>
          </div>

          <!-- 绘制注册窗口 -->
          <div class="tab-pane container" id="regpanel">
            <div class="modal-body">
              <div class="form-floating mb-3 row">
                <input
                  type="text"
                  class="form-control"
                  id="regname"
                  placeholder="键入邮箱地址"
                />
                <label for="regname">键入邮箱地址</label>
              </div>

              <div class="form-floating mb-3 row">
                <input
                  type="password"
                  class="form-control"
                  id="regpass"
                  placeholder="键入注册密码"
                />
                <label for="regpass">键入注册密码</label>
              </div>

              <div class="row mb-3">
                <div class="col-9 form-floating p-0 pe-1">
                  <input
                    type="text"
                    id="regcode"
                    class="form-control"
                    placeholder="请键入邮箱验证码"
                  />
                  <label for="regcode">邮箱验证码</label>
                </div>
                <button
                  type="button"
                  class="btn btn-primary col-3"
                  @click="doSendMail(this)"
                >
                  获取验证码
                </button>
              </div>
            </div>
            <!-- Modal组件 页脚部分 -->
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                关闭
              </button>
              <button
                type="button"
                class="btn btn-primary"
                @click="doReg(null)"
              >
                注册
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>