<template>
  <div class="page">
    <el-card>
      <div class="header">
        <h2>我的失物</h2>
        <el-button type="primary" @click="$router.push('/lost/publish')">发布失物</el-button>
      </div>
      <el-tabs v-model="activeStatus" @tab-change="loadData">
        <el-tab-pane label="全部" name="" />
        <el-tab-pane label="待审核" name="待审核" />
        <el-tab-pane label="已发布" name="已发布" />
        <el-tab-pane label="已匹配" name="已匹配" />
        <el-tab-pane label="已认领" name="已认领" />
        <el-tab-pane label="已关闭" name="已关闭" />
        <el-tab-pane label="已驳回" name="已驳回" />
      </el-tabs>
      <div v-loading="loading">
        <ItemCard v-for="item in list" :key="item.id" :item="item" @click="$router.push(`/lost/${item.id}`)" />
        <EmptyState v-if="!list.length" text="暂无失物记录" />
        <el-pagination v-if="total > pageSize" :total="total" :page-size="pageSize" v-model:current-page="page" layout="prev, pager, next" @current-change="loadData" class="pager" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { myLostList, deleteLost } from '../../api/item'
import { ElMessage, ElMessageBox } from 'element-plus'
import ItemCard from '../../components/ItemCard.vue'
import EmptyState from '../../components/EmptyState.vue'

const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)
const activeStatus = ref('')

const loadData = async () => {
  loading.value = true
  try {
    const res = await myLostList({ page: page.value, page_size: pageSize, status: activeStatus.value })
    list.value = res.data.list
    total.value = res.data.total
  } catch (e) {} finally { loading.value = false }
}
onMounted(loadData)
</script>

<style scoped>
.page { max-width: 800px; margin: 0 auto; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
h2 { margin: 0; }
.pager { margin-top: 16px; text-align: center; }
</style>