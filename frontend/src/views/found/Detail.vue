<template>
  <div class="page" v-loading="loading">
    <el-card v-if="item">
      <div class="header"><h2>{{ item.name }}</h2><StatusTag :status="item.status" /></div>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="类别">{{ item.category }}</el-descriptions-item>
        <el-descriptions-item label="拾获时间">{{ item.found_time }}</el-descriptions-item>
        <el-descriptions-item label="拾获地点">{{ item.location }}</el-descriptions-item>
        <el-descriptions-item label="保管方式">{{ item.custody }}</el-descriptions-item>
        <el-descriptions-item label="联系方式可见">{{ item.contact_visibility }}</el-descriptions-item>
        <el-descriptions-item label="详细描述" :span="2">{{ item.description }}</el-descriptions-item>
        <el-descriptions-item label="发布者" :span="2">{{ publisherInfo }}</el-descriptions-item>
      </el-descriptions>
      <div class="images" v-if="item.image_urls && item.image_urls.length">
        <el-image v-for="(url, i) in item.image_urls" :key="i" :src="url" class="img" fit="cover" :preview-src-list="item.image_urls" />
      </div>
      <div class="actions" v-if="isSelf">
        <el-button @click="$router.push(`/found/edit/${item.id}`)" v-if="['待审核','已发布','已驳回'].includes(item.status)">编辑</el-button>
        <el-button type="danger" @click="handleDelete" v-if="['待审核','已发布'].includes(item.status)">撤回</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { foundDetail, deleteFound } from '../../api/item'
import { useUserStore } from '../../stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import StatusTag from '../../components/StatusTag.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const item = ref(null)
const isSelf = computed(() => item.value?.publisher_id === userStore.userInfo?.user_id)
const publisherInfo = computed(() => {
  const p = item.value?.publisher
  if (!p) return ''
  return p.name + (p.email ? ` (${p.email})` : '')
})
onMounted(async () => {
  loading.value = true
  try { const res = await foundDetail(route.params.id); item.value = res.data } catch (e) {} finally { loading.value = false }
})
const handleDelete = async () => {
  await ElMessageBox.confirm('确认撤回该拾物信息？', '提示', { type: 'warning' })
  await deleteFound(item.value.id)
  ElMessage.success('已撤回')
  router.push('/found/mine')
}
</script>

<style scoped>
.page { max-width: 700px; margin: 0 auto; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.images { display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
.img { width: 120px; height: 120px; border-radius: 4px; }
.actions { margin-top: 16px; }
</style>