import Vue from 'vue';
import VueRouter from 'vue-router';
import page from '../components/page.vue';

Vue.use(VueRouter);

const routes = [

  {
    path: '/page',
    name: 'page',
    component: page,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
