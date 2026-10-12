<template>
  <el-card class="item-card" shadow="hover" @click="$emit('click')">
    <div class="card-header">
      <span class="name">{{ item.name }}</span>
      <StatusTag :status="item.status" />
    </div>
    <div class="card-body">
      <div class="info-row"><span class="label">类别：</span>{{ item.category }}</div>
      <div class="info-row"><span class="label">地点：</span>{{ item.location }}</div>
      <div class="info-row"><span class="label">时间：</span>{{ timeField }}</div>
      <div class="info-row" v-if="item.custody"><span class="label">保管：</span>{{ item.custody }}</div>
    </div>
    <div class="images" v-if="item.image_urls && item.image_urls.length">
      <el-image v-for="(url, i) in item.image_urls.slice(0, 3)" :key="i" :src="url" class="thumb" fit="cover" />
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import StatusTag from './StatusTag.vue'

const props = defineProps({ item: Object })
defineEmits(['click'])

const timeField = computed(() => props.item.lost_time || props.item.found_time || '')
</script>

<style scoped>
.item-card { cursor: pointer; margin-bottom: 12px; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.name { font-size: 16px; font-weight: bold; }
.card-body { font-size: 13px; color: #606266; }
.info-row { margin-bottom: 4px; }
.label { color: #909399; }
.images { display: flex; gap: 8px; margin-top: 8px; }
.thumb { width: 60px; height: 60px; border-radius: 4px; }
</style>