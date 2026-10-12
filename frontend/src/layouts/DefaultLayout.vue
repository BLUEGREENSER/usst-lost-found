<template>
  <el-container class="default-layout">
    <el-header class="header">
      <div class="logo" @click="$router.push('/')">上理工失物招领</div>
      <el-menu mode="horizontal" :default-active="activeMenu" router class="menu">
        <el-menu-item index="/search">搜索</el-menu-item>
        <el-menu-item index="/lost/publish" v-if="userStore.isLoggedIn">发布失物</el-menu-item>
        <el-menu-item index="/found/publish" v-if="userStore.isLoggedIn">发布拾物</el-menu-item>
        <el-menu-item index="/lost/mine" v-if="userStore.isLoggedIn">我的失物</el-menu-item>
        <el-menu-item index="/found/mine" v-if="userStore.isLoggedIn">我的拾物</el-menu-item>
        <el-menu-item index="/matches" v-if="userStore.isLoggedIn">匹配</el-menu-item>
        <el-menu-item index="/admin" v-if="userStore.isAdmin">管理后台</el-menu-item>
      </el-menu>
      <div class="right-area">
        <template v-if="userStore.isLoggedIn">
          <el-badge :value="notifStore.unreadCount" :hidden="notifStore.unreadCount === 0" class="badge">
            <el-button text @click="$router.push('/notifications')">
              <el-icon><Bell /></el-icon>
            </el-button>
          </el-badge>
          <el-dropdown @command="handleCommand">
            <span class="user-name">{{ userStore.userInfo?.name }}</span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button text @click="$router.push('/login')">登录</el-button>
          <el-button text @click="$router.push('/register')">注册</el-button>
        </template>
      </div>
    </el-header>
    <el-main class="main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useNotificationStore } from '../stores/notification'
import { Bell } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const notifStore = useNotificationStore()

const activeMenu = computed(() => route.path)

onMounted(() => {
  if (userStore.isLoggedIn) notifStore.startPolling()
})
onUnmounted(() => notifStore.stopPolling())

const handleCommand = async (cmd) => {
  if (cmd === 'logout') {
    await userStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.default-layout { min-height: 100vh; }
.header { display: flex; align-items: center; background: #fff; border-bottom: 1px solid #eee; }
.logo { font-size: 18px; font-weight: bold; color: #409eff; cursor: pointer; margin-right: 30px; white-space: nowrap; }
.menu { flex: 1; border-bottom: none; }
.right-area { display: flex; align-items: center; gap: 12px; }
.user-name { cursor: pointer; color: #606266; }
.badge { margin-right: 8px; }
.main { background: #f5f7fa; min-height: calc(100vh - 60px); }
</style>