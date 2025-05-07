<script setup lang="ts">
import TopInfos from '../components/dashboard/TopInfos.vue';
import Loading from '../components/Loading.vue';
// Notifications
const { showToast } = useNotifications();
// Files
const selectedFiles = ref();
const isImporting = ref(false);
const uploadProgress = ref(0);
const importError = ref();
const importSuccess = ref(false);
const handleFileChange = (event: any) => {
  const inputElement = event.target as HTMLInputElement;
  selectedFiles.value = inputElement.files;
  // console.log(selectedFiles.value);
};
const importFile = async () => {
  if (!selectedFiles.value || selectedFiles.value.length === 0) {
    importError.value = 'Select at Least one File .';
    return;
  }
  isImporting.value = true;
  uploadProgress.value = 0;
  importError.value = null;
  importSuccess.value = false;

  const formData = new FormData();
  for (let i = 0; i < selectedFiles.value.length; i++) {
    formData.append('files', selectedFiles.value[i]);
  }

  try {
    // const response = await axios.post(urlAPI + '/upload', formData, {
    //   headers: {
    //     'Content-Type': 'multipart/form-data',
    //   },
    //   onUploadProgress: (progressEvent: any) => {
    //     uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
    //   },
    // });
    setInterval(() => {
      uploadProgress.value = uploadProgress.value + 10;
      if (uploadProgress.value == 100) {
        isImporting.value = false;
        importSuccess.value = true;
      }
    }, 500);


    // console.log('Upload successful:', response.data);
  } catch (error) {
    importError.value = 'Error while uploading your file !';
    console.error('Upload error:', error);
  } finally {
    // isImporting.value = false;
  }
}
// Processing
const processingStarted = ref(false);
const processingDone = ref(false);
const isDownloading = ref(false);
const startProcessing = async () => {
  processingStarted.value = false;
  processingDone.value = false;
  // const accessToken = sessionStorage.getItem('AccessToken');
  // const refToken = sessionStorage.getItem('RefreshToken');
  try {
    // const response = await axios.get(urlAPI + "/start_sprocessing",
    //     {
    //         params: {
    //             access_token: accessToken,
    //             refresh_token: refToken,
    //         },
    //         headers: {
    //             "accept": "application/json",
    //             "content-type": "application/x-www-form-urlencoded",
    //         },
    //     },
    // );

    // 
    processingStarted.value = true;
    showToast('Success', "Successfully Started Processing. Once Ready, you'll be able to dowload the outputs", 'i-heroicons-check-badge', 'success');
    // Store Renewed Tokens
    // sessionStorage.setItem('AccessToken', response.data.session.session.access_token);
    // sessionStorage.setItem('RefreshToken', response.data.session.session.refresh_token);
    // sessionStorage.setItem('ExpiresAt', response.data.session.session.expires_at);

  } catch (err) {
    console.error('Erreur de requete:', err);
    showToast('Error !', "Failled to Start Scraping, maybe server error !", 'i-heroicons-exclamation-triangle', 'error');
  } finally {
    // 
    setTimeout(() => {
      processingDone.value = true;
    }, 10000);
  }

}
const downloadOutput = async () => {
  isDownloading.value = true;
  try {

    // const response = await axios.get('/api/download-file', { // Remplacez '/api/download-file' par l'URL de votre API pour le téléchargement
    //   responseType: 'blob', // Indique à Axios de traiter la réponse comme un Blob (données binaires)
    // });

    // const blob = new Blob([response.data]);
    // const url = window.URL.createObjectURL(blob);
    // const link = document.createElement('a');
    // link.href = url;
    // link.setAttribute('download', 'nom_du_fichier_telecharge.ext'); // Remplacez 'nom_du_fichier_telecharge.ext' par le nom de fichier souhaité
    // document.body.appendChild(link);
    // link.click();
    // window.URL.revokeObjectURL(url); // Libérer la mémoire

    showToast('Success', "Successfully Downloaded the file", 'i-heroicons-check-badge', 'success');

  } catch (err) {
    console.error('Erreur de requete:', err);
    showToast('Error !', "Failled to Download the file !", 'i-heroicons-exclamation-triangle', 'error');
  } finally {
    isDownloading.value = false;
  }
}
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
            <UInput type="file" multiple icon="i-heroicons-document-duplicate" @change="handleFileChange"
              accept=".doc, .pdf" />
            <UButton class="text-white" :disabled="!selectedFiles" :loading="isImporting" @click="importFile"
              label="Upload" color="primary" icon="i-heroicons-arrow-down-tray" />
          </UButtonGroup>
          <!-- <div class="" v-if="selectedFiles">
            Got Files
          </div> -->
          <!-- Loading Upload -->
          <UProgress v-if="isImporting" :value="uploadProgress" :max="100" class="mt-4 mb-2" />
          <p v-if="isImporting">Uploading : <span class="font-bold text-info-600">{{ uploadProgress }}</span> %</p>
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
          <div v-if="processingDone" class="flex flex-col place-items-center py-5">
            <!-- <img class="w-30 h-30" src="../public/api-process.gif" alt="Animated GIF"> -->
            <div class="my-8">
              <UButton class="text-white rounded-full h-35 w-35 cursor-pointer" @click="downloadOutput" color="primary">
                <div class=" w-full h-full flex flex-col text-center place-content-center items-center">
                  <UIcon name="i-heroicons-folder-arrow-down" class="size-20" />
                  <h4>Download</h4>
                </div>
              </UButton>
            </div>
            <p class="text-gray-900 mt-1">Now Just Download the Outputs !</p>
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