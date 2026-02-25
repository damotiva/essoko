<template>
  <div>
    <!-- Hero Section -->
    <header class="hero bg-light text-center py-5">
      <div class="container">
        <h1 class="display-4">Welcome to ESSOKO</h1>
        <p class="lead">Connecting farmers, markets, and families with transparency and sustainability.</p>
        <a href="#journey" class="btn btn-primary">Learn More</a>
      </div>
    </header>

    <!-- Sample Farmer Products Section -->
    <section id="products" class="py-5 bg-light">
      <div class="container">
        <h2 class="display-4 text-center">Farmer Products</h2>
        <p class="lead text-center">Explore a selection of farmer products available on our platform.</p>

        <br/>

        <!-- Product Cards -->
        <div class="row">
          <div class="col-md-4" v-for="product in products" :key="product.id">
            <div class="card mb-4 shadow-sm">
              <img :src="product.image" style="width: 400px; height: 300px;" class="card-img-top" alt="product image">
              <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text">Price: {{ product.price }} USD</p>
                <p class="card-text">Available in {{ product.godowns }} godowns</p>
                <button class="btn btn-primary">View Product</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script>

import axios from "axios"

export default {
  name: 'IndexPage',
  layout: 'master',
  data() {
    return {
      
      products: [
        {
          id: 1,
          name: "Maize",
          price: "20.00",
          godowns: 5,
          image: "https://www.harvestplus.org/wp-content/uploads/2021/11/zinc-maize_1-1024x747.png"
        },
        {
          id: 2,
          name: "Beans",
          price: "30.00",
          godowns: 3,
          image: "https://static.vecteezy.com/system/resources/previews/049/096/407/non_2x/variety-of-colorful-beans-and-legumes-on-plate-transparent-png.png"
        },
        {
          id: 3,
          name: "Rice",
          price: "40.00",
          godowns: 7,
          image: "https://static.vecteezy.com/system/resources/thumbnails/021/217/698/small/cooked-rice-food-png.png"
        },

        {
          id: 4,
          name: "Maize",
          price: "20.00",
          godowns: 5,
          image: "https://www.harvestplus.org/wp-content/uploads/2021/11/zinc-maize_1-1024x747.png"
        },
        {
          id: 5,
          name: "Beans",
          price: "30.00",
          godowns: 3,
          image: "https://static.vecteezy.com/system/resources/previews/049/096/407/non_2x/variety-of-colorful-beans-and-legumes-on-plate-transparent-png.png"
        },
        {
          id: 6,
          name: "Rice",
          price: "40.00",
          godowns: 7,
          image: "https://static.vecteezy.com/system/resources/thumbnails/021/217/698/small/cooked-rice-food-png.png"
        },
      ]
    }
  },

  computed: {
    authUser() {
      return this.$store.state.auth_user_data?.auth_user || ''
    },
    authToken() {
      return this.$store.state.auth_user_data?.auth_token || ''
    },
    userId() {
      return this.$store.state.auth_user_data?.user_id || ''
    },
  },

  methods: {
    // Additional methods for fetching real product data can go here if needed
  }

}
</script>

<style scoped>
.hero {
  background-color: #f8f9fa;
}

.hero h1 {
  font-family: 'Playfair Display', serif;
}

.card {
  border-radius: 8px;
}

.card-title {
  font-weight: bold;
}

.card-body {
  text-align: center;
}

.card-text {
  font-size: 1rem;
}

.bg-light {
  background-color: #f8f9fa !important;
}
</style>