import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/home/Home.vue'
// import main from '@/components/main.vue'
// import maintext from '@/components/maintext.vue'
// import maintext1 from '@/components/maintext1.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // },
    // {
    //   path: '/main',
    //   component: main
    // },
    // {
    //   path: '/text',
    //   component: maintext1
    // }
  ]
})

export default router
