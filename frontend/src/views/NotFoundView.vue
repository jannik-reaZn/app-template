<script setup lang="ts">
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
  <UError
    :error="{
      statusCode: 404,
      statusMessage: t('notFound.title'),
      message: t('notFound.message'),
    }"
    :clear="{ label: t('notFound.home'), to: '/' }"
  />
</template>
