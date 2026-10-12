<template>
  <div class="page">
    <el-card>
      <h2>匹配列表</h2>
      <el-tabs v-model="activeStatus" @tab-change="loadData">
        <el-tab-pane label="全部" name="" />
        <el-tab-pane label="待确认" name="待确认" />
        <el-tab-pane label="已确认" name="已确认" />
        <el-tab-pane label="已拒绝" name="已拒绝" />
        <el-tab-pane label="已失效" name="已失效" />
      </el-tabs>
      <div v-loading="loading">
        <el-card v-for="m in list" :key="m.id" class="match-card" shadow="hover">
          <div class="match-header">
            <span>匹配 #{{ m.id }}</span>
            <span class="similarity">相似度: {{ (m.similarity * 100).toFixed(1) }}%</span>
            <StatusTag :status="m.status" />
          </div>
          <div class="match-body">
            <div class="item-block">
              <div class="label">失物</div>
              <div>{{ m.lost?.name }} - {{ m.lost?.category }} - {{ m.lost?.location }}</div>
            </div>
            <div class="item-block">
              <div class="label">拾物</div>
              <div>{{ m.found?.name }} - {{ m.found?.category }} - {{ m.found?.location }}</div>
            </div>
            <div class="dims" v-if="m.dimensions">
              <span>命中关键词: {{ m.dimensions.hit_keywords?.join(', ') || '无' }}</span>
            </div>
          </div>
          <div class="actions" v-if="m.status === '待确认'">
            <el-button type="primary" size="small" @click="handleConfirm(m)">确认</el-button>
            <el-button size="small" @click="handleReject(m)">拒绝</el-button>
          </div>
          <div class="actions" v-if="m.status === '已确认'">
            <el-button type="success" size="small" @click="handleClaim(m)">发起认领</el-button>
          </div>
        </el-card>
        <EmptyState v-if="!list.length" text="暂无匹配记录" />
        <el-pagination v-if="total > pageSize" :total="total" :page-size="pageSize" v-model:current-page="page" layout="prev, pager, next" @current-change="loadData" class="pager" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { listMatches, confirmMatch, rejectMatch, createClaim } from '../../api/common'
import { ElMessage } from 'element-plus'
import StatusTag from '../../components/StatusTag.vue'
import EmptyState from '../../components/EmptyState.vue'

const router = useRouter()
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)
const activeStatus = ref('')

const loadData = async () => {
  loading.value = true
  try { const res = await listMatches({ page: page.value, page_size: pageSize, status: activeStatus.value }); list.value = res.data.list; total.value = res.data.total } catch (e) {} finally { loading.value = false }
}
onMounted(loadData)

const handleConfirm = async (m) => { await confirmMatch(m.id); ElMessage.success('已确认'); loadData() }
const handleReject = async (m) => { await rejectMatch(m.id); ElMessage.success('已拒绝'); loadData() }
const handleClaim = async (m) => {
  const res = await createClaim({ match_id: m.id })
  ElMessage.success('认领已发起，校验码已发送')
  router.push(`/claims/${res.data.claim_id}`)
}
</script>

<style scoped>
.page { max-width: 800px; margin: 0 auto; }
h2 { margin-bottom: 16px; }
.match-card { margin-bottom: 12px; }
.match-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.similarity { color: #409eff; font-weight: bold; }
.match-body { font-size: 13px; color: #606266; }
.item-block { margin-bottom: 4px; }
.label { color: #909399; display: inline-block; width: 40px; }
.dims { margin-top: 4px; color: #909399; }
.actions { margin-top: 8px; }
.pager { margin-top: 16px; text-align: center; }
</style>