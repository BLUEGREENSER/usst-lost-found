<template>
  <div class="page">
    <el-card>
      <h2>发布失物信息</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="物品名称" prop="name">
          <el-input v-model="form.name" placeholder="如：黑色钱包" />
        </el-form-item>
        <el-form-item label="物品类别" prop="category">
          <el-select v-model="form.category" placeholder="请选择">
            <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
          </el-select>
        </el-form-item>
        <el-form-item label="丢失时间" prop="lost_time">
          <el-date-picker v-model="form.lost_time" type="datetime" value-format="YYYY-MM-DDTHH:mm:ss" placeholder="选择时间" />
        </el-form-item>
        <el-form-item label="丢失地点" prop="location">
          <el-input v-model="form.location" placeholder="如：教学楼A栋3楼" />
        </el-form-item>
        <el-form-item label="详细描述">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="物品特征、颜色、品牌等" />
        </el-form-item>
        <el-form-item label="联系方式">
          <el-radio-group v-model="form.contact_visibility">
            <el-radio label="公开" />
            <el-radio label="仅匹配可见" />
            <el-radio label="仅登录可见" />
          </el-radio-group>
        </el-form-item>
        <el-form-item label="图片">
          <ImageUploader v-model="form.image_urls" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">提交发布</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { publishLost } from '../../api/item'
import { ElMessage } from 'element-plus'
import ImageUploader from '../../components/ImageUploader.vue'

const CATEGORIES = ['电子产品', '证件', '钥匙', '书籍文具', '衣物', '钱包', '卡类', '其他']
const router = useRouter()
const formRef = ref()
const loading = ref(false)
const categories = CATEGORIES

const form = reactive({
  name: '', category: '', lost_time: '', location: '',
  description: '', contact_visibility: '仅匹配可见', image_urls: [],
})
const rules = {
  name: [{ required: true, message: '请输入物品名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择类别', trigger: 'change' }],
  lost_time: [{ required: true, message: '请选择时间', trigger: 'change' }],
  location: [{ required: true, message: '请输入地点', trigger: 'blur' }],
}

const handleSubmit = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    await publishLost(form)
    ElMessage.success('发布成功，等待审核')
    router.push('/lost/mine')
  } catch (e) {} finally { loading.value = false }
}
</script>

<style scoped>
.page { max-width: 700px; margin: 0 auto; }
h2 { margin-bottom: 20px; }
</style>