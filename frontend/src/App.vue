<script setup lang="ts">
import { de } from "@nuxt/ui/locale";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const year = new Date().getFullYear();
</script>

<template>
  <UApp :locale="de">
    <UHeader :title="t('app.title')" to="/" :toggle="false" />
    <UMain>
      <RouterView />
    </UMain>
    <UFooter class="sticky bottom-0 z-10 bg-default">
      <template #left>
        <p class="text-sm text-muted">{{ t("footer.copyright", { year }) }}</p>
      </template>
    </UFooter>
  </UApp>
</template>
