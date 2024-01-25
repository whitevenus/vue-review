<script>

import ReadLeft from '@/components/ReadLeft/index.vue'
import IndexRight from '@/components/IndexRight/index.vue'



export default {
  components: { IndexRight, ReadLeft },

}
</script>


<template>

    <main>
        <div class="container">
            <div class="row">
                <read-left></read-left>
                <index-right></index-right>
            </div>
        </div>
    </main>

</template>