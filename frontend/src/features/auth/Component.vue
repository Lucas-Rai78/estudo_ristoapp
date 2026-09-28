<script setup lang="ts">
defineProps<{
  title: string
  subtitle: string
}>()
</script>

<template>
  <main class="flex min-h-dvh items-center justify-center bg-bg-app px-4 py-10">
    <div class="w-full max-w-md">
      <div class="mb-8 text-center">
        <div
          class="mx-auto mb-5 flex size-12 items-center justify-center rounded-xl bg-brand-primary text-xl font-bold text-white"
        >
          R
        </div>

        <span class="text-sm font-semibold text-brand-primary">
          RistoApp
        </span>

        <h1 class="mt-3 text-3xl font-bold tracking-tight text-text-primary">
          {{ title }}
        </h1>

        <p class="mt-2 text-sm text-text-secondary">
          {{ subtitle }}
        </p>
      </div>

      <div
        class="rounded-2xl border border-border-main bg-bg-surface p-6 shadow-sm sm:p-8"
      >
        <slot />
      </div>
    </div>
  </main>
</template>