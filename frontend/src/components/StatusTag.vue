<template>
  <el-tag :type="tagType" size="small">{{ status }}</el-tag>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ status: String })

const STATUS_MAP = {
  '待审核': 'warning',
  '已发布': 'success',
  '已匹配': 'primary',
  '已认领': 'success',
  '已关闭': 'info',
  '已驳回': 'danger',
  '待确认': 'warning',
  '已确认': 'success',
  '已拒绝': 'danger',
  '已失效': 'info',
  '进行中': 'warning',
  '已完成': 'success',
  '已取消': 'info',
  '已生成': 'warning',
  '已使用': 'success',
  '已失效': 'info',
}

const tagType = computed(() => STATUS_MAP[props.status] || 'info')
</script>