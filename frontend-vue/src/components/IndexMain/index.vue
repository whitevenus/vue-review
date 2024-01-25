<script>

import IndexLeft from '@/components/IndexLeft/index.vue'
import IndexRight from '@/components/IndexRight/index.vue'



export default {
  components: { IndexLeft, IndexRight },

}
</script>


<template>

    <main>
        <div class="container">
            <div class="row">
                <index-left></index-left>
                <index-right></index-right>
            </div>
        </div>
    </main>

</template>