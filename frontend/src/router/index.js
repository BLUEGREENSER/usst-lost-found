import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/search' },
  { path: '/login', name: 'Login', component: () => import('../views/auth/Login.vue'), meta: { guest: true } },
  { path: '/register', name: 'Register', component: () => import('../views/auth/Register.vue'), meta: { guest: true } },
  { path: '/search', name: 'Search', component: () => import('../views/search/Search.vue') },
  {
    path: '',
    component: () => import('../layouts/DefaultLayout.vue'),
    children: [
      { path: '/lost/publish', name: 'LostPublish', component: () => import('../views/lost/Publish.vue'), meta: { auth: true } },
      { path: '/lost/edit/:id', name: 'LostEdit', component: () => import('../views/lost/Edit.vue'), meta: { auth: true } },
      { path: '/lost/mine', name: 'LostMine', component: () => import('../views/lost/MineList.vue'), meta: { auth: true } },
      { path: '/lost/:id', name: 'LostDetail', component: () => import('../views/lost/Detail.vue') },
      { path: '/found/publish', name: 'FoundPublish', component: () => import('../views/found/Publish.vue'), meta: { auth: true } },
      { path: '/found/edit/:id', name: 'FoundEdit', component: () => import('../views/found/Edit.vue'), meta: { auth: true } },
      { path: '/found/mine', name: 'FoundMine', component: () => import('../views/found/MineList.vue'), meta: { auth: true } },
      { path: '/found/:id', name: 'FoundDetail', component: () => import('../views/found/Detail.vue') },
      { path: '/matches', name: 'Matches', component: () => import('../views/match/MatchList.vue'), meta: { auth: true } },
      { path: '/claims/:id', name: 'ClaimDetail', component: () => import('../views/claim/ClaimDetail.vue'), meta: { auth: true } },
      { path: '/notifications', name: 'Notifications', component: () => import('../views/notify/NotifyList.vue'), meta: { auth: true } },
    ],
  },
  {
    path: '/admin',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { auth: true, admin: true },
    children: [
      { path: '', redirect: '/admin/audit' },
      { path: 'audit', name: 'AdminAudit', component: () => import('../views/admin/AuditList.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('../views/admin/UserList.vue') },
      { path: 'stats', name: 'AdminStats', component: () => import('../views/admin/Stats.vue') },
    ],
  },
]

const router = createRouter({
  // GitHub Pages 部署在子路径下时需设置 base；本地开发默认 '/'
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')
  if (to.meta.auth && !token) {
    next('/login')
  } else if (to.meta.admin && role !== 'admin') {
    next('/')
  } else if (to.meta.guest && token) {
    next('/')
  } else {
    next()
  }
})

export default router