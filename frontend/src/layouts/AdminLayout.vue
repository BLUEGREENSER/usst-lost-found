<template>
  <el-container class="admin-layout">
    <el-aside width="200px" class="aside">
      <div class="logo">管理后台</div>
      <el-menu :default-active="activeMenu" router>
        <el-menu-item index="/admin/audit">审核管理</el-menu-item>
        <el-menu-item index="/admin/users">用户管理</el-menu-item>
        <el-menu-item index="/admin/stats">统计查看</el-menu-item>
        <el-menu-item index="/">返回前台</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span>管理员：{{ userStore.userInfo?.name }}</span>
        <el-button text @click="logout">退出</el-button>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const activeMenu = computed(() => route.path)

const logout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout { min-height: 100vh; }
.aside { background: #304156; }
.logo { color: #fff; font-size: 16px; font-weight: bold; padding: 20px 16px; text-align: center; }
:deep(.el-menu) { background: #304156; border-right: none; }
:deep(.el-menu-item) { color: #bfcbd9; }
:deep(.el-menu-item.is-active) { color: #409eff; background: #263445; }
.header { display: flex; justify-content: space-between; align-items: center; background: #fff; border-bottom: 1px solid #eee; }
.main { background: #f5f7fa; }
</style>