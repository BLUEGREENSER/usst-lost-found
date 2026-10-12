<template>
  <el-upload
    :action="uploadAction"
    :headers="uploadHeaders"
    :on-success="handleSuccess"
    :on-error="handleError"
    :before-upload="beforeUpload"
    :file-list="fileList"
    list-type="picture-card"
    :limit="maxCount"
    :on-exceed="() => $message.warning(`最多上传${maxCount}张`)"
    accept=".jpg,.jpeg,.png"
  >
    <el-icon><Plus /></el-icon>
  </el-upload>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { API_BASE, resolveImageUrl } from '../api/config'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  maxCount: { type: Number, default: 5 },
  maxSizeMB: { type: Number, default: 5 },
})
const emit = defineEmits(['update:modelValue'])

const uploadAction = API_BASE + '/api/v1/upload/image'
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
}))
const fileList = ref([])

watch(() => props.modelValue, (urls) => {
  fileList.value = (urls || []).map((url, i) => ({ name: `image-${i}`, url: resolveImageUrl(url) }))
}, { immediate: true })

const beforeUpload = (file) => {
  if (file.size > props.maxSizeMB * 1024 * 1024) {
    ElMessage.error(`图片大小不能超过${props.maxSizeMB}MB`)
    return false
  }
  return true
}

const handleSuccess = (res) => {
  if (res.code === 0) {
    const urls = [...props.modelValue, res.data.url]
    emit('update:modelValue', urls)
  } else {
    ElMessage.error(res.message || '上传失败')
  }
}

const handleError = () => ElMessage.error('上传失败')
</script>