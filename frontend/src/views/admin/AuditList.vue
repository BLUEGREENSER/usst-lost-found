<template>
  <div class="page">
    <el-card>
      <h2>审核管理</h2>
      <el-radio-group v-model="type" @change="loadData" class="type-switch">
        <el-radio-button label="lost">失物</el-radio-button>
        <el-radio-button label="found">拾物</el-radio-button>
      </el-radio-group>
      <el-table :data="list" v-loading="loading" class="table">
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="category" label="类别" width="100" />
        <el-table-column prop="location" label="地点" />
        <el-table-column prop="publisher_name" label="发布者" width="100" />
        <el-table-column prop="created_at" label="提交时间" width="180" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleApprove(row)">通过</el-button>
            <el-button size="small" @click="handleReject(row)">驳回</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-if="total > pageSize" :total="total" :page-size="pageSize" v-model:current-page="page" layout="prev, pager, next" @current-change="loadData" class="pager" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { auditList, approve, reject, takedown } from '../../api/common'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)
const type = ref('lost')

const loadData = async () => {
  loading.value = true
  try { const res = await auditList({ type: type.value, page: page.value, page_size: pageSize }); list.value = res.data.list; total.value = res.data.total } catch (e) {} finally { loading.value = false }
}
onMounted(loadData)

const handleApprove = async (row) => { await approve(type.value, row.id); ElMessage.success('已通过'); loadData() }
const handleReject = async (row) => {
  const { value } = await ElMessageBox.prompt('请输入驳回理由', '驳回', { inputValidator: (v) => !!v?.trim() || '理由不能为空' })
  await reject(type.value, row.id, { reason: value })
  ElMessage.success('已驳回')
  loadData()
}
</script>

<style scoped>
.page { }
h2 { margin-bottom: 16px; }
.type-switch { margin-bottom: 16px; }
.table { margin-bottom: 16px; }
.pager { text-align: center; }
</style>