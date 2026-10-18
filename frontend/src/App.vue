<script setup lang="ts">
import { de } from "@nuxt/ui/locale";
import type { NavigationMenuItem } from "@nuxt/ui";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const navItems = computed<NavigationMenuItem[]>(() => [
  { label: t("nav.home"), icon: "i-lucide-house", to: "/" },
  { label: t("nav.upload"), icon: "i-lucide-upload", to: "/upload" },
  { label: t("nav.analysis"), icon: "i-lucide-chart-pie", to: "/analysis" },
]);
const sidebarOpen = ref(true);
const year = new Date().getFullYear();
</script>

<template>
  <UApp :locale="de">
    <UHeader :toggle="false" :ui="{ container: 'max-w-none mx-0 px-4 sm:px-4 lg:px-4' }">
      <template #left>
        <UButton
          color="neutral"
          variant="ghost"
          icon="i-lucide-panel-left"
          :aria-label="t('nav.toggle')"
          :aria-expanded="sidebarOpen"
          @click="sidebarOpen = !sidebarOpen"
        />
        <RouterLink to="/" class="text-xl font-bold text-highlighted">{{
          t("app.title")
        }}</RouterLink>
      </template>
    </UHeader>
    <div class="flex">
      <USidebar
        v-model:open="sidebarOpen"
        :title="t('nav.title')"
        rail
        :ui="{
          container: 'top-(--ui-header-height) h-[calc(100svh-var(--ui-header-height))]',
          header: 'lg:hidden',
        }"
      >
        <UNavigationMenu :items="navItems" orientation="vertical" />
      </USidebar>
      <div class="flex min-h-[calc(100svh-var(--ui-header-height))] min-w-0 flex-1 flex-col">
        <UMain class="min-h-0 flex-1">
          <RouterView />
        </UMain>
        <UFooter class="sticky bottom-0 z-10 bg-default">
          <template #left>
            <p class="text-sm text-muted">{{ t("footer.copyright", { year }) }}</p>
          </template>
        </UFooter>
      </div>
    </div>
  </UApp>
</template>
