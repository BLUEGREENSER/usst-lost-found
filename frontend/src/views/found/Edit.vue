<template>
  <div class="page">
    <el-card v-loading="loading">
      <h2>编辑拾物信息</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="物品名称" prop="name"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="物品类别" prop="category">
          <el-select v-model="form.category"><el-option v-for="c in categories" :key="c" :label="c" :value="c" /></el-select>
        </el-form-item>
        <el-form-item label="拾获时间" prop="found_time">
          <el-date-picker v-model="form.found_time" type="datetime" value-format="YYYY-MM-DDTHH:mm:ss" />
        </el-form-item>
        <el-form-item label="拾获地点" prop="location"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="保管方式" prop="custody">
          <el-radio-group v-model="form.custody">
            <el-radio label="本人保管" /><el-radio label="已交失物招领处" /><el-radio label="已交保卫处" />
          </el-radio-group>
        </el-form-item>
        <el-form-item label="详细描述"><el-input v-model="form.description" type="textarea" :rows="4" /></el-form-item>
        <el-form-item label="联系方式">
          <el-radio-group v-model="form.contact_visibility">
            <el-radio label="公开" /><el-radio label="仅匹配可见" /><el-radio label="仅登录可见" />
          </el-radio-group>
        </el-form-item>
        <el-form-item label="图片"><ImageUploader v-model="form.image_urls" /></el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">保存</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { foundDetail, editFound } from '../../api/item'
import { ElMessage } from 'element-plus'
import ImageUploader from '../../components/ImageUploader.vue'

const CATEGORIES = ['电子产品', '证件', '钥匙', '书籍文具', '衣物', '钱包', '卡类', '其他']
const route = useRoute()
const router = useRouter()
const formRef = ref()
const loading = ref(false)
const submitting = ref(false)
const categories = CATEGORIES
const form = reactive({ name: '', category: '', found_time: '', location: '', custody: '本人保管', description: '', contact_visibility: '仅匹配可见', image_urls: [] })
const rules = {
  name: [{ required: true, message: '请输入物品名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择类别', trigger: 'change' }],
  found_time: [{ required: true, message: '请选择时间', trigger: 'change' }],
  location: [{ required: true, message: '请输入地点', trigger: 'blur' }],
}
onMounted(async () => {
  loading.value = true
  try { const res = await foundDetail(route.params.id); Object.assign(form, res.data) } catch (e) {} finally { loading.value = false }
})
const handleSubmit = async () => {
  await formRef.value.validate()
  submitting.value = true
  try { await editFound(route.params.id, form); ElMessage.success('已更新，等待审核'); router.push('/found/mine') } catch (e) {} finally { submitting.value = false }
}
</script>

<style scoped>
.page { max-width: 700px; margin: 0 auto; }
h2 { margin-bottom: 20px; }
</style>