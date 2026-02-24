<template>
    
    <div class="horizontal-menu">
      
      <client-only>

         <nav class="navbar top-navbar col-12 p-0 border-btm">
           <div class="container-fluid top-navbar-root">
             <div class="text-center navbar-brand-wrapper d-flex align-items-center justify-content-center">
                 <span class="color-black font-20 d-block font-weight-light text-center">
                 <NuxtLink to="/" class="color-black font-size-20">
                   <strong>Admission Works</strong>
                 </NuxtLink> 
                 </span>
             </div>
             <div class="navbar-menu-wrapper d-flex align-items-center justify-content-end">
               <ul class="navbar-nav mr-lg-2">
                 <li class="nav-item nav-search d-none d-lg-block">
                   <div class="input-group">
                     <div class="input-group-prepend hover-cursor" id="navbar-search-icon">
 
                     </div>
                   </div>
                 </li>
               </ul>
               <ul class="navbar-nav navbar-nav-right">
                 <li class="nav-item nav-profile dropdown">
                   <a class="nav-link" id="profileDropdown" href="#" data-toggle="dropdown" aria-expanded="false">
                     <div class="nav-profile-img">
                       <img src="../assets/images/hospital.jpg" alt="image">
                     </div>
                     <div class="nav-profile-text">
                       <p class="text-black font-weight-semibold m-0">User : {{ user }}</p>
                     </div>
 
                     &nbsp;&nbsp;&nbsp;&nbsp;
 
                     <button class="btn btn-success" @click="goToMicroServicesDashboard()">Micro-Services</button>
 
                     &nbsp;&nbsp;
 
                     <button class="btn btn-danger" @click="logout()"><i class="fa fa-share" aria-hidden="true"></i>&nbsp;Logout</button>
                     
                   </a>
                 </li>
               </ul>
             </div>
           </div>
         </nav>
     
     <Nuxt />

     </client-only>
 
     </div>
 
 </template>
 
 
 <script>
   import axios from 'axios'
 
   export default {
     name: 'LayoutMaster',
   
     computed: {

          user() {
            return this.$store.state.auth_user_data?.auth_user || ''
          },

          authToken() {
            return this.$store.state.auth_user_data?.auth_token || ''
          },

          userId() {
            return this.$store.state.auth_user_data?.user_id || ''
          }
      },

      methods: {
          // Go To Micro Services Dashboard
          goToMicroServicesDashboard() {
            
            //Go to Micro-Services Panel
            window.location.assign(this.$store.state.core_ui + "/prepare/welcome?username=" + this.user + "&user_id=" + this.userId + "&token=" + this.authToken , "_blank")
          },

         async logout() {
           //Send Logout Request
           await axios({
               method: 'POST',
               url: this.$store.state.entry_api + '/logout',
               headers: {
                   "Content-Type": "application/json",
                   "Auth-User": this.$store.state.auth_user,
                   "Auth-Token": this.$store.state.auth_token
               }
           }).then((response) => {
               var jsonData = JSON.parse(JSON.stringify(response.data));
 
               if (jsonData['status'] == true) {
                 //Show Notification
                 this.$Notice.success({
                     title: 'Logout Success',
                     desc: 'You have been Logged Out Successfully'
                 });
 
                 //Clear Auth Data
                 this.$store.commit('clear_auth_data')
           
                 //Go to Core UI
                 window.location.assign(this.$store.state.core_ui)
               }else {
                 //Show Error on Logout
                 this.$Notice.error({
                     title: 'Logout Failure',
                     desc: 'Failed to Logout. Please Try Again...'
                 });
               }
               
           });
   
         }
     }
 
   }
 </script>
 
 
 <style scoped>
   .top-navbar-root {
     padding: 10px;
   }
 
   .color-black {
     color: black;
     text-decoration: none;
   }
 
   .logout-fav {
     color: red;
     margin-left: 10px;
     font-size: 20px;
   }
 
   .border-btm {
     border-bottom: 2px solid black;
   }
 
   .none-padding {
     padding: none;
   }
 
 </style>