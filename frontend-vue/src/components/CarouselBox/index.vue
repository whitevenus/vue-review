<script>
export default {
    
}
</script>


<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <!-- 轮播图盒子 -->
        <div
          id="carouselExampleIndicators"
          class="carousel slide"
          data-bs-ride="true"
        >
          <!-- 轮播图下方指示器 -->
          <div class="carousel-indicators">
            <button
              type="button"
              data-bs-target="#carouselExampleIndicators"
              data-bs-slide-to="0"
              class="active"
              aria-current="true"
              aria-label="Slide 1"
            ></button>
            <button
              type="button"
              data-bs-target="#carouselExampleIndicators"
              data-bs-slide-to="1"
              aria-label="Slide 2"
            ></button>
            <button
              type="button"
              data-bs-target="#carouselExampleIndicators"
              data-bs-slide-to="2"
              aria-label="Slide 3"
            ></button>
          </div>

          <!-- 幻灯片主体 -->
          <div class="carousel-inner rounded rounded-5">
            <div class="carousel-item active">
              <img src="src/assets/img/banner-1.jpg" alt="..." class="w-100" />
            </div>
            <div class="carousel-item">
              <img src="src/assets/img/banner-2.jpg" alt="..." class="w-100" />
            </div>
            <div class="carousel-item">
              <img src="src/assets/img/banner-3.jpg" alt="..." class="w-100" />
            </div>
          </div>

          <!-- 幻灯片左右按钮 -->
          <button
            class="carousel-control-prev"
            type="button"
            data-bs-target="#carouselExampleIndicators"
            data-bs-slide="prev"
          >
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <!-- <span class="visually-hidden">Previous</span> -->
          </button>
          <button
            class="carousel-control-next"
            type="button"
            data-bs-target="#carouselExampleIndicators"
            data-bs-slide="next"
          >
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <!-- <span class="visually-hidden">Next</span> -->
          </button>
        </div>
      </div>
    </div>
  </div>
</template>