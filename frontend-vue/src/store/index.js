import { defineStore } from "pinia";

// 1.定义容器
// 参数1：容器的ID，必须唯一，将来Pinia会把所有的容器挂载到跟组件
// 参数2： 选项对象
export const useMainStore = defineStore("main", {
    // 类似组件的data,用来存储全局状态
    // 1.必须是函数：这是为了在服务端渲染的时候避免交叉请求导致数据状态污染
    // 2.必须是箭头函数，这是为了更好的TS类型推导
    state: () => {
        return {
            posts: [],
            page: 1,
            total: 0,
            type: "",
            postType: {
                1: "PHP开发",
                2: "Java开发",
                3: "Python开发",
                4: "Web前端",
                5: "测试开发",
                6: "数据科学",
                7: "网络安全",
                8: "蜗牛杂谈",
            },
            typeColor: {
                1: "text-bg-danger",
                2: "text-bg-warning",
                3: "text-bg-dark",
                4: "text-bg-info",
                5: "text-bg-success",
                6: "text-bg-secondary",
                7: "text-bg-light",
                8: "text-bg-light",
            },
            session: {}
        }
    },

    getters: {


    },
    actions: {

    }
})

// 2.使用容器

// 3.修改state

// 4.容器内action的使用