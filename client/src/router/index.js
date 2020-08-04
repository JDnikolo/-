import Vue from 'vue';
import VueRouter from 'vue-router';
import core from '../components/core.vue';

Vue.use(VueRouter);

const routes = [

  {
    path: '/',
    name: 'page',
    component: core,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
