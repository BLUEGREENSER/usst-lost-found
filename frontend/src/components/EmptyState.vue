<template>
  <div class="empty-state">
    <el-icon class="icon"><Box /></el-icon>
    <p>{{ text }}</p>
  </div>
</template>

<script setup>
import { Box } from '@element-plus/icons-vue'
defineProps({ text: { type: String, default: '暂无数据' } })
</script>

<style scoped>
.empty-state { text-align: center; padding: 40px; color: #909399; }
.icon { font-size: 48px; margin-bottom: 8px; }
</style>