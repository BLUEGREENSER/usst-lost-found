<template>
  <div class="page">
    <el-card>
      <div class="header"><h2>站内消息</h2>
        <el-button text @click="handleReadAll" v-if="list.some(n => !n.is_read)">全部已读</el-button>
      </div>
      <div v-loading="loading">
        <div v-for="n in list" :key="n.id" class="msg-item" :class="{ unread: !n.is_read }" @click="handleClick(n)">
          <div class="msg-header">
            <el-tag size="small" :type="tagType(n.type)">{{ typeLabel(n.type) }}</el-tag>
            <span class="time">{{ n.created_at }}</span>
            <el-badge is-dot :hidden="n.is_read" />
          </div>
          <div class="msg-body">{{ n.summary }}</div>
        </div>
        <EmptyState v-if="!list.length" text="暂无消息" />
        <el-pagination v-if="total > pageSize" :total="total" :page-size="pageSize" v-model:current-page="page" layout="prev, pager, next" @current-change="loadData" class="pager" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { listNotifications, markRead, markAllRead } from '../../api/common'
import { useNotificationStore } from '../../stores/notification'
import EmptyState from '../../components/EmptyState.vue'

const router = useRouter()
const notifStore = useNotificationStore()
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)

const TYPE_LABELS = { match: '匹配', claim: '认领', audit: '审核' }
const typeLabel = (t) => TYPE_LABELS[t] || t
const tagType = (t) => ({ match: 'primary', claim: 'success', audit: 'warning' }[t] || 'info')

const loadData = async () => {
  loading.value = true
  try { const res = await listNotifications({ page: page.value, page_size: pageSize }); list.value = res.data.list; total.value = res.data.total } catch (e) {} finally { loading.value = false }
}
onMounted(loadData)

const handleClick = async (n) => {
  if (!n.is_read) { await markRead(n.id); n.is_read = true; notifStore.fetchUnreadCount() }
  if (n.target_url) router.push(n.target_url)
}
const handleReadAll = async () => {
  await markAllRead()
  list.value.forEach(n => n.is_read = true)
  notifStore.fetchUnreadCount()
}
</script>

<style scoped>
.page { max-width: 700px; margin: 0 auto; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
h2 { margin: 0; }
.msg-item { padding: 12px; border-bottom: 1px solid #eee; cursor: pointer; }
.msg-item.unread { background: #f0f9ff; }
.msg-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.time { color: #909399; font-size: 12px; flex: 1; }
.msg-body { font-size: 14px; color: #303133; }
.pager { margin-top: 16px; text-align: center; }
</style>