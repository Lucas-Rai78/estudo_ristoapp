<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: string | number | null
  id?: string
  label?: string
  type?: string
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  error?: string
  hint?: string
}

const props = withDefaults(defineProps<Props>(), {
  id: () => `input-${Math.random().toString(36).substring(2, 9)}`,
  type: 'text',
  placeholder: '',
  disabled: false,
  readonly: false,
  required: false,
  error: '',
  hint: ''
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'focus', event: FocusEvent): void
  (e: 'blur', event: FocusEvent): void
}>()

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const inputClasses = computed(() => [
  'w-full rounded-lg text-sm transition-colors duration-150 ease-in-out focus:outline-none',
  'bg-bg-surface text-text-primary placeholder-text-muted',
  'px-3.5 py-2',
  props.error
    ? 'border-2 border-status-danger focus:ring-2 focus:ring-status-danger-bg'
    : 'border border-border-main focus:border-brand-primary focus:ring-2 focus:ring-brand-light',
  props.disabled ? 'opacity-60 cursor-not-allowed bg-bg-hover' : ''
])
</script>

<template>
  <div class="w-full flex flex-col gap-1.5">
    <label
      v-if="label"
      :for="id"
      class="text-xs font-semibold text-text-secondary tracking-wide"
    >
      {{ label }}
      <span v-if="required" class="text-status-danger">*</span>
    </label>

    <div class="relative flex items-center">
      <div
        v-if="$slots['icon-left']"
        class="absolute left-3 flex items-center pointer-events-none text-text-muted"
      >
        <slot name="icon-left" />
      </div>

      <input
        :id="id"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :class="[
          inputClasses,
          $slots['icon-left'] ? 'pl-9' : '',$slots['icon-right'] ? 'pr-9' : ''
        ]"
        @input="handleInput"
        @focus="$emit('focus',$event)"
        @blur="$emit('blur',$event)"
      />

      <div
        v-if="$slots['icon-right']"
        class="absolute right-3 flex items-center pointer-events-none text-text-muted"
      >
        <slot name="icon-right" />
      </div>
    </div>

    <span v-if="error" class="text-xs text-status-danger font-medium">
      {{ error }}
    </span>
    <span v-else-if="hint" class="text-xs text-text-muted">
      {{ hint }}
    </span>
  </div>
</template>