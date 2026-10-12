<template>
  <div class="page">
    <el-card>
      <h2>用户管理</h2>
      <el-table :data="list" v-loading="loading">
        <el-table-column prop="user_id" label="ID" width="60" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="role" label="角色" width="80" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }"><el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">{{ row.status }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button v-if="row.status === 'active'" size="small" type="danger" @click="handleDisable(row)">禁用</el-button>
            <el-button v-else size="small" type="success" @click="handleEnable(row)">启用</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-if="total > pageSize" :total="total" :page-size="pageSize" v-model:current-page="page" layout="prev, pager, next" @current-change="loadData" class="pager" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listUsers, enableUser, disableUser } from '../../api/common'
import { ElMessage } from 'element-plus'

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)

const loadData = async () => {
  loading.value = true
  try { const res = await listUsers({ page: page.value, page_size: pageSize }); list.value = res.data.list; total.value = res.data.total } catch (e) {} finally { loading.value = false }
}
onMounted(loadData)

const handleDisable = async (row) => { await disableUser(row.user_id); ElMessage.success('已禁用'); loadData() }
const handleEnable = async (row) => { await enableUser(row.user_id); ElMessage.success('已启用'); loadData() }
</script>

<style scoped>
h2 { margin-bottom: 16px; }
.pager { margin-top: 16px; text-align: center; }
</style>