<template>
  <div v-show="contentType == 3">
    <div class="Reupload-section">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      請選擇/輸入要輸出的頁面
    </div>
    <div class="actions">
      <div v-for="option in options" :key="option.value">
      <button class="action-btn">
        <input type="checkbox" :value="option.value" v-model="selectedOptions" />
        {{ option.label }}
      </button>
    </div>
          <!-- <button class="action-btn" @click="changeContentType(4)">Introduction</button>
          <button class="action-btn" @click="changeContentType(4)">Related Work</button>
          <button class="action-btn" @click="changeContentType(4)">Methdology</button>
          <button class="action-btn" @click="changeContentType(4)">Conclusion</button> -->
        </div>
    <!-- <button class="send-btn" @click="changeContentType(4)" >
    </button> -->
    <button class="pdf-input" @click="changeContentType(0)">
      重新匯入PDF
    </button>
  </div>

  <div v-show="contentType == 4">
    <div class="Reupload-section">
      <img class="robot-img" src="@/components/home/content/assets/robot_icon.png" />
      已轉檔完成！
    </div>
    <div class="actions">
      <button class="download-btn">下載Power Point</button>
    </div>
    <button class="pdf-input" @click="changeContentType(0)">
      重新匯入PDF
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, inject, defineProps } from "vue";

const contentType = inject("contentType", ref(0));
const options = [
  { value: 'option1', label: 'Introduction' },
  { value: 'option2', label: 'Related Work' },
  { value: 'option3', label: 'Methdology' },
  { value: 'option4', label: 'Conclusion' }
];

const props = defineProps({
  contentType: Number
});

</script>


<style scoped lang="scss">
.Reupload-section {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 10px;
}

.robot-img {
  height: 30px;
  padding: 10px 10px 10px 10px;
}

.actions {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  .action-btn {
    background-color: white;
    border: 1px solid white;
    padding: 10px 20px;
    cursor: pointer;
    margin: 0 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 4px;
  }
}

.download-btn {
  background-color: #91c5b5;
  border: 1px solid white;
  padding: 10px 20px;
  cursor: pointer;
  margin: 0 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.pdf-input {
  background-color: #4285f4;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  margin-left: 500px;
  display: flex;
  align-items: center;
  border-radius: 10;
  font-size: 10px;
}
</style>