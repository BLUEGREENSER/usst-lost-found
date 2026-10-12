<template>
  <div class="page">
    <el-card>
      <h2>统计查看</h2>
      <el-radio-group v-model="period" @change="loadData" class="period-switch">
        <el-radio-button label="day">今日</el-radio-button>
        <el-radio-button label="week">本周</el-radio-button>
        <el-radio-button label="month">本月</el-radio-button>
      </el-radio-group>
      <div class="stats-grid" v-loading="loading">
        <el-card class="stat-card"><div class="num">{{ data.publish_count }}</div><div class="label">发布数</div></el-card>
        <el-card class="stat-card"><div class="num">{{ data.match_count }}</div><div class="label">匹配数</div></el-card>
        <el-card class="stat-card"><div class="num">{{ data.claim_count }}</div><div class="label">认领数</div></el-card>
        <el-card class="stat-card"><div class="num">{{ data.audit_pending_count }}</div><div class="label">待审核</div></el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { stats } from '../../api/common'

const period = ref('day')
const loading = ref(false)
const data = reactive({ publish_count: 0, match_count: 0, claim_count: 0, audit_pending_count: 0 })

const loadData = async () => {
  loading.value = true
  try { const res = await stats({ period: period.value }); Object.assign(data, res.data) } catch (e) {} finally { loading.value = false }
}
onMounted(loadData)
</script>

<style scoped>
h2 { margin-bottom: 16px; }
.period-switch { margin-bottom: 16px; }
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.stat-card { text-align: center; }
.num { font-size: 32px; font-weight: bold; color: #409eff; }
.label { font-size: 14px; color: #909399; margin-top: 4px; }
</style>