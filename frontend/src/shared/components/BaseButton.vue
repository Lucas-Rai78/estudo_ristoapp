<script setup lang="ts">
import { computed } from 'vue'

export type ButtonVariant =
  'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
export type ButtonSize = 'sm' | 'md' | 'lg'

interface Props {
  variant?: ButtonVariant
  size?: ButtonSize
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
  fullWidth?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  type: 'button',
  disabled: false,
  loading: false,
  fullWidth: false,
})

defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const baseClasses =
  'inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed select-none'

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    'bg-brand-primary hover:bg-brand-hover text-white focus:ring-brand-primary shadow-sm',
  secondary:
    'bg-bg-sidebar hover:bg-bg-hover text-text-primary focus:ring-border-main',
  outline:
    'border border-border-main bg-transparent hover:bg-bg-hover text-text-primary focus:ring-brand-primary',
  ghost:
    'bg-transparent hover:bg-bg-hover text-text-secondary hover:text-text-primary focus:ring-border-main',
  danger:
    'bg-status-danger hover:opacity-90 text-white focus:ring-status-danger shadow-sm',
}

const sizeClasses: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-xs gap-1.5',
  md: 'px-4 py-2 text-sm gap-2',
  lg: 'px-5 py-2.5 text-base gap-2.5',
}

const buttonClasses = computed(() => [
  baseClasses,
  variantClasses[props.variant],
  sizeClasses[props.size],
  props.fullWidth ? 'w-full' : '',
])
</script>

<template>
  <button
    :type="type"
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <svg
      v-if="loading"
      class="animate-spin h-4 w-4 text-current shrink-0"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>

    <slot name="icon-left" />
    <slot />
    <slot name="icon-right" />
  </button>
</template>
