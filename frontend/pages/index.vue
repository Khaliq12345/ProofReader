<template>
  <div class="flex-col p-5">
    <UInput type="file" accept="*" @change="handleFileChange" multiple/>
    <h3>FILE: {{ file }}</h3>
  </div>
</template>

<script setup lang="ts">

const file = ref()

const handleFileChange = async (event: any) => {
  const inputElement = event.target as HTMLInputElement;
  file.value = inputElement.files

  const formData = new FormData()
  formData.append('file', file.value)

  console.log(formData.entries())

  // formData.forEach((file) => {
  //   console.log(file.toString())
  // })
  
  const response = await fetch('/api/upload', {
    method: 'POST',
    body: formData
  })

  $fetch('/api/analyse-document')

  
};
 
useStorage("ouputs").watch(() => {
  
})
</script>
