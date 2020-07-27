import Vue from 'vue';
import VueRouter from 'vue-router';
import scoreboard from '../components/scoreboard.vue';
import core from '../components/core.vue';

Vue.use(VueRouter);

const routes = [

  {
    path: '/page',
    name: 'page',
    component: core,
  },
  {
    path: '/scores',
    name: 'scoreboard',
    component: scoreboard,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
