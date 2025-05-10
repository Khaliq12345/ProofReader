<script setup lang="ts">
import TopInfos from '../components/dashboard/TopInfos.vue';
import Loading from '../components/Loading.vue';

// Notifications
const { showToast } = useNotifications();
// Files
const filesList: Ref<string[]> = ref([]);
const selectedFiles = ref();
const isUploading = ref(false);
const importError = ref();
const importSuccess = ref(false);
const handleFileChange = (event: any) => {
  const inputElement = event.target as HTMLInputElement;
  selectedFiles.value = inputElement.files;
  // console.log(selectedFiles.value);
};
const uploadFile = async () => {
  if (!selectedFiles.value || selectedFiles.value.length === 0) {
    importError.value = 'Select at Least one File .';
    return;
  }
  isUploading.value = true;
  importError.value = null;
  importSuccess.value = false;
  const formData = new FormData();
  for (let i = 0; i < selectedFiles.value.length; i++) {
    const file = selectedFiles.value[i];
    const timestamp = Date.now().toString();
    const newFileName = timestamp + '_' + file.name.trim();
    const newFile = new File([file], newFileName, { type: file.type, lastModified: file.lastModified });
    formData.append('files', newFile);
    filesList.value.push(newFileName);
  }
  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });
    // console.log("Upload response : ", response)
    // console.log("filesList.value : ", filesList.value)
    importSuccess.value = true;
  } catch (error) {
    importError.value = 'Error while uploading your file !';
    console.error('Upload error:', error);
  } finally {
    isUploading.value = false;
  }
}

// Processing
const processingStarted = ref(false);
const processingError = ref(false);
const processingDone = ref(false);
const isDownloading = ref(false);
const outputFile = ref<string>()
// Download File
const downloadOutput = async () => {
  let filename = outputFile.value ?? ""
  try {
    isDownloading.value = true;
    const response = await $fetch('/api/download', {
      query: { file: filename },
      responseType: 'blob'
    })
    const url = URL.createObjectURL(response)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
    // showToast('Success', "Successfully Downloaded the file", 'i-heroicons-check-badge', 'success');
  } catch (err) {
    console.error('Erreur de requete:', err);
    // showToast('Error !', "Failled to Download the file !", 'i-heroicons-exclamation-triangle', 'error');
  } finally {
    isDownloading.value = false;
  }
}
const startProcessing = async () => {
  processingStarted.value = false;
  processingDone.value = false;
  processingError.value = false;
  try {
    processingStarted.value = true;
    // 
    const response = await $fetch('/api/analyse-document', {
      method: 'POST',
      body: filesList.value,
    }) as any;
    console.log("processing result : ", response)
    localStorage.setItem('output_folder', response.output_folder);
    // 
    //
    showToast('Success', "Successfully Started Processing. Once Ready, you'll be able to dowload the outputs", 'i-heroicons-check-badge', 'success');
    // 
  } catch (err) {
    console.error('Erreur de requete:', err);
    showToast('Error !', "Failled to Start Processing, maybe server error !", 'i-heroicons-exclamation-triangle', 'error');
    processingStarted.value = false;
  } finally {
    // 
  }
}
const checkStatus = async () => {
  processingDone.value = false
  processingError.value = false
  let folder = localStorage.getItem('output_folder')
  try {
    const response = await $fetch('/api/check-status', {
      method: 'GET',
      params: {
        'folder': folder
      }
    }) as any
    console.log("status : ", response)
    if (response.status == 'success') {
      processingDone.value = true;
      outputFile.value = folder + "/output.zip"
      localStorage.setItem('output_file', outputFile.value )
      showToast('Success', "Last Processing Successfully Completed.", 'i-heroicons-check-badge', 'success');
    } else if(response.status == null){
      return;
    } else {
      showToast('Infos !', `Last Processing Failled : got status  -- ${response.status} --`, 'i-heroicons-exclamation-triangle', 'error');
      processingStarted.value = false
      processingError.value = true
    }
  } catch (error) {
    console.error('Erreur de requete:', error);
    showToast('Error !', "Last Processing Failled ", 'i-heroicons-exclamation-triangle', 'error');
    processingStarted.value = false
    processingError.value = true
  }
}
// Mounting this page
onMounted(async () => {
  if (localStorage.getItem('output_file')) {
    outputFile.value = localStorage.getItem('output_file') ?? undefined
  }
  if (localStorage.getItem('output_folder')) {
    checkStatus()
  }
  // Check Status if something is going
  setInterval(() => {
    if (processingStarted.value == true && processingDone.value != true) {
      checkStatus()
    }
  }, 10000);
})
// 
definePageMeta({
  middleware: ["auth"]
})
</script>

<template>
  <div class="min-h-screen min-w-screen bg-gradient-to-br from-blue-50 to-blue-100 flex flex-col items-center  ">
    <UContainer class="pt-5  ">
      <!-- Top Infos -->
      <TopInfos />
      <!-- Main Card for Content Processing -->
      <div class="">
        <USeparator label="Process Your Files" />
        <div class="container mx-auto px-4 pt-5 my-3 text-center">
          <h1 class="text-2xl font-bold mb-4">Start By Uploading Your Files</h1>
          <!-- Files Input -->
          <UButtonGroup class="my-3 ">
            <UInput type="file" accept=".doc, .docx, .pdf" multiple icon="i-heroicons-document-duplicate"
              @change="handleFileChange" />
            <UButton class="text-white" :disabled="!selectedFiles" :loading="isUploading" @click="uploadFile"
              label="Upload" color="primary" icon="i-heroicons-arrow-down-tray" />
          </UButtonGroup>
          <div class="my-2 font-bold text-info-800" v-if="selectedFiles">
            {{ selectedFiles.length }} File(s) Selected !
          </div>
          <!-- Loading Upload -->
          <UProgress v-if="isUploading" :max="100" class="mt-4 mb-2 font-bold text-info-600" />
          <p v-if="isUploading">... Uploading ...</p>
          <!-- When Error -->
          <UAlert v-if="importError" :title="importError" color="error" class="mt-2 mb-4"
            close-icon="i-heroicons-x-mark" icon="i-heroicons-exclamation-triangle" />
          <!-- When Success -->
          <UAlert v-if="importSuccess" title="Successfully imported Files !" class="mt-2 mb-4 bg-success-300"
            close-icon="i-heroicons-x-mark" icon="i-heroicons-check-badge" />
          <!-- Start -->
          <div v-if="importSuccess" class="justify-end flex">
            <UButton label="Start Processing" :disabled="processingStarted" icon="i-heroicons-cog"
              class="justify-center text-white" @click="startProcessing" color="info" />
          </div>
          <!-- Loading and Output -->
          <!-- Loading -->
          <div v-if="processingStarted && !processingDone" class="  flex flex-col place-items-center py-5">
            <!-- <img class="w-30 h-30" src="../public/api-process.gif" alt="Animated GIF"> -->
            <div class="my-8">
              <Loading />
            </div>
            <p class="text-gray-900 mt-1">We are processing your Files ...</p>
          </div>
          <!-- Outputs -->
          <div v-if="processingError" class="my-4 flex justify-center">
            <!-- On Processing Error -->
            <UAlert color="error" variant="subtle" typ title="Last Processing Failled !" class="my-3 md:w-2/3 lg:w-1/2"
              close-icon="i-heroicons-x-mark" icon="i-heroicons-check-badge" />
          </div>
          <div v-if="processingDone && outputFile && !processingError" class="flex flex-col place-items-center py-5">
            <!-- <img class="w-30 h-30" src="../public/api-process.gif" alt="Animated GIF"> -->
            <div class="my-8">
              <UButton class="text-white rounded-full h-35 w-35 cursor-pointer" @click="downloadOutput" color="primary">
                <div class=" w-full h-full flex flex-col text-center place-content-center items-center">
                  <UIcon name="i-heroicons-folder-arrow-down" class="size-20" />
                  <h4>Download</h4>
                </div>
              </UButton>
            </div>
            <p class="text-gray-900 mt-1">Last Processing Completed. Just Download the Outputs !</p>
            <UAlert color="success" variant="subtle" typ title="Successfully processed your Files !"
              class="my-3 md:w-2/3 lg:w-1/2" close-icon="i-heroicons-x-mark" icon="i-heroicons-check-badge" />
          </div>
        </div>
      </div>
    </UContainer>
  </div>
</template>

<style scoped>
.container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25),
    0 10px 10px rgba(0, 0, 0, 0.22);
  position: relative;
  overflow: hidden;
  max-width: 100%;
  min-height: 480px;
}
</style>