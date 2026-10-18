<script setup lang="ts">
import { de } from "@nuxt/ui/locale";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
  <UApp :locale="de">
    <UHeader :title="t('app.title')" to="/" :toggle="false" />
    <UMain>
      <RouterView />
    </UMain>
  </UApp>
</template>
