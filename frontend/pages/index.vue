<template>
 
    <div>

    </div>
</template>

<script>

import axios from "axios"

export default {
  name: 'IndexPage',
  layout: 'master',
  data() {
    return {

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
        
    }

}

</script>



<style scoped>


</style>