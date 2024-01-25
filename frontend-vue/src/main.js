import { createApp } from 'vue'
// 导入根组件
import App from './App.vue'
// 导入vue路由
import router from './router'

import pinia from "@/store/store"

// 导入bootstrap的样式文件
import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap/dist/js/bootstrap.bundle.min.js"

// 导入并使用v-md-editor编辑器
import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import Prism from 'prismjs';
VueMarkdownEditor.use(vuepressTheme, {
  Prism,
});

// 创建应用实例
const app = createApp(App)


app.use(router)
app.use(pinia)
app.use(VueMarkdownEditor);
// 挂载应用实例到div元素中
app.mount('#app')
