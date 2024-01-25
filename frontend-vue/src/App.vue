<script>


export default {
  data() {
    return {};
  },
};
</script>

<template>
  <RouterView />
</template>


<style>
body {
  background-color: rgba(250, 250, 250, 1);
}

main {
  margin-top: 130px;
}

a,
a:link,
a:visited {
  text-decoration: none;
  color: #000;
}

.card-title a:hover,
a:active {
  text-decoration: none;
  color: #337ab7;
}

.sm-txt {
  font-size: 10px;
}

.avatar-img {
  width: 50px;
  height: 50px;
}
.avatar-edit {
  width: 40px;
  height: 40px;
}

.foot {
  font-size: 12px;
}
</style>

