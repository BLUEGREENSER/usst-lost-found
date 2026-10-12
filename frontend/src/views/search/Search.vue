<template>
  <div class="page">
    <el-card class="search-card">
      <div class="search-bar">
        <el-input v-model="keyword" placeholder="搜索物品名称或描述" clearable class="keyword" @keyup.enter="loadData" />
        <el-select v-model="type" placeholder="类型" class="type-select">
          <el-option label="失物" value="lost" />
          <el-option label="拾物" value="found" />
        </el-select>
        <el-select v-model="category" placeholder="类别" clearable class="cat-select">
          <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
        </el-select>
        <el-input v-model="location" placeholder="地点" clearable class="loc-input" />
        <el-button type="primary" @click="loadData">搜索</el-button>
      </div>
    </el-card>
    <div class="result-list" v-loading="loading">
      <ItemCard v-for="item in list" :key="item.id" :item="item" @click="goDetail(item)" />
      <EmptyState v-if="!list.length && !loading" text="暂无匹配结果" />
      <el-pagination v-if="total > pageSize" :total="total" :page-size="pageSize" v-model:current-page="page" layout="prev, pager, next" @current-change="loadData" class="pager" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { search } from '../../api/common'
import ItemCard from '../../components/ItemCard.vue'
import EmptyState from '../../components/EmptyState.vue'

const CATEGORIES = ['电子产品', '证件', '钥匙', '书籍文具', '衣物', '钱包', '卡类', '其他']
const router = useRouter()
const categories = CATEGORIES
const keyword = ref('')
const type = ref('lost')
const category = ref('')
const location = ref('')
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)

const loadData = async () => {
  loading.value = true
  try {
    const res = await search({ keyword: keyword.value, type: type.value, category: category.value, location: location.value, page: page.value, page_size: pageSize })
    list.value = res.data.list
    total.value = res.data.total
  } catch (e) {} finally { loading.value = false }
}
onMounted(loadData)

const goDetail = (item) => router.push(`/${type.value}/${item.id}`)
</script>

<style scoped>
.page { max-width: 800px; margin: 0 auto; }
.search-card { margin-bottom: 16px; }
.search-bar { display: flex; gap: 8px; flex-wrap: wrap; }
.keyword { flex: 1; min-width: 200px; }
.type-select { width: 100px; }
.cat-select { width: 120px; }
.loc-input { width: 150px; }
.pager { margin-top: 16px; text-align: center; }
</style>