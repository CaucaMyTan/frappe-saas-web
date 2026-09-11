<template>
  <VoiceListPage
    doctype="AI Agent"
    title="Kịch bản Lễ tân"
    :fields="fields"
    :columns="columns"
  />
</template>

<script setup>
import VoiceListPage from './VoiceListPage.vue'

const fields = ['name', 'agent_name', 'retell_agent_id', 'creation']

const columns = [
  { key: 'name', label: 'Mã / Slug' },
  { key: 'agent_name', label: 'Tên kịch bản' },
  { key: 'retell_agent_id', label: 'Retell Agent ID' },
]
</script>
