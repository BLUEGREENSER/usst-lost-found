<template>
  <div class="page" v-loading="loading">
    <el-card v-if="claim">
      <h2>认领详情 #{{ claim.id }}</h2>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="认领状态"><StatusTag :status="claim.status" /></el-descriptions-item>
        <el-descriptions-item label="校验码状态"><StatusTag :status="claim.code_status" /></el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ claim.created_at }}</el-descriptions-item>
        <el-descriptions-item label="完成时间">{{ claim.completed_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="失物" :span="2">{{ claim.lost?.name }} - {{ claim.lost?.location }}</el-descriptions-item>
        <el-descriptions-item label="拾物" :span="2">{{ claim.found?.name }} - {{ claim.found?.location }}</el-descriptions-item>
      </el-descriptions>

      <div class="actions" v-if="claim.status === '进行中'">
        <template v-if="claim.is_loser">
          <el-alert title="您是失主" type="info" :closable="false" class="alert" />
          <p class="tip">校验码已通过站内消息发送给您和拾到者，请与拾到者联系并告知校验码。</p>
          <el-button type="warning" @click="handleResend">重发校验码</el-button>
          <el-button @click="handleCancel">取消认领</el-button>
        </template>
        <template v-if="claim.is_finder">
          <el-alert title="您是拾到者" type="info" :closable="false" class="alert" />
          <p class="tip">请输入失主提供的校验码完成认领。</p>
          <el-form @submit.prevent="handleVerify">
            <el-input v-model="codeInput" placeholder="输入6位校验码" maxlength="6" class="code-input" />
            <el-button type="primary" @click="handleVerify" :loading="verifying">核验</el-button>
          </el-form>
        </template>
      </div>
      <el-alert v-if="claim.status === '已完成'" title="认领已完成" type="success" :closable="false" class="alert" />
      <el-alert v-if="claim.status === '已取消'" title="认领已取消" type="info" :closable="false" class="alert" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { claimDetail, verifyClaim, cancelClaim, resendCode } from '../../api/common'
import { ElMessage } from 'element-plus'
import StatusTag from '../../components/StatusTag.vue'

const route = useRoute()
const loading = ref(false)
const verifying = ref(false)
const claim = ref(null)
const codeInput = ref('')

const loadData = async () => {
  loading.value = true
  try { const res = await claimDetail(route.params.id); claim.value = res.data } catch (e) {} finally { loading.value = false }
}
onMounted(loadData)

const handleVerify = async () => {
  if (!codeInput.value) { ElMessage.warning('请输入校验码'); return }
  verifying.value = true
  try { await verifyClaim(route.params.id, { verify_code: codeInput.value }); ElMessage.success('核验成功，认领完成'); loadData() } catch (e) {} finally { verifying.value = false }
}
const handleCancel = async () => { await cancelClaim(route.params.id); ElMessage.success('已取消'); loadData() }
const handleResend = async () => { const res = await resendCode(route.params.id); ElMessage.success('校验码已重发'); loadData() }
</script>

<style scoped>
.page { max-width: 700px; margin: 0 auto; }
h2 { margin-bottom: 16px; }
.actions { margin-top: 16px; }
.alert { margin-bottom: 12px; }
.tip { margin: 8px 0; color: #909399; font-size: 13px; }
.code-input { width: 200px; margin-right: 8px; }
</style>