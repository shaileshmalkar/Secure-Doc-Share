
import { createRouter, createWebHistory } from 'vue-router'
import Upload from '../views/Upload.vue'
import Access from '../views/Access.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Upload },
    { path: '/view/:id', component: Access }
  ]
})
