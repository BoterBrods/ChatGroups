import { createRouter, createWebHistory } from 'vue-router';
import AuthLogin from '../views/AuthLogin.vue';
import RoomSelect from '../views/RoomSelect.vue';

const routes = [
  { path: '/', redirect: '/auth/login' },
  { path: '/auth/login', component: AuthLogin },
  { path: '/rooms', component: RoomSelect },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
