<template>
  <div class="file-list">
    <div class="left">
      <h2>PDF :</h2>
      <ul>
        <li v-for="(file, index) in pdfFiles" :key="index">
          <div class="file-item">
            <label>
              <input type="checkbox" v-model="selectedFiles" :value="file" />
              <span class="file-name">{{ file.name }}</span>
            </label>
          </div>
        </li>
          <div class="buttons">
              <button @click="downloadSelectedFiles('pdf')">下載</button>
              <button @click="openSelectedFiles('pdf')">開啟</button>
          </div>
      </ul>
    </div>
    
    <div class="right">
      <h2>PPT : </h2>
      <ul>
        <li v-for="(file, index) in pptFiles" :key="index">
          <div class="file-item">
            <label>
              <input type="checkbox" v-model="selectedFiles" :value="file" />
              <span class="file-name">{{ file.name }}</span>
            </label>
          </div>
        </li>
          <div class="buttons">
              <button @click="downloadSelectedFiles('ppt')">下載</button>
              <button @click="openSelectedFiles('ppt')">開啟</button>
          </div>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    fileList: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      selectedFiles: [] 
    };
  },
  computed: {
    pdfFiles() {
      return this.fileList.filter(file => file.type === 'pdf');
    },
    pptFiles() {
      return this.fileList.filter(file => file.type === 'ppt');
    }
  },
  methods: {
    downloadSelectedFiles(fileType) {
      const selectedFiles = this.selectedFiles.filter(file => file.type === fileType);
      selectedFiles.forEach(file => {
        console.log(`下載 ${fileType.toUpperCase()} 檔案：`, file.name);
      });
    },
    openSelectedFiles(fileType) {
      const selectedFiles = this.selectedFiles.filter(file => file.type === fileType);
      selectedFiles.forEach(file => {
        console.log(`開啟 ${fileType.toUpperCase()} 檔案：`, file.name);
      });
    }
  }
};
</script>

<style scoped>
.file-list {
  display: flex;
  width: 100%;
}

.left {
  flex: flwx;
  width: 50%;
  background-color: #A5C2BB; 
  display: flex;
  justify-content: center; 
}

.right {
  flex: flex;
  width: 50%;
  background-color: #e1e1e1; 
  display: flex;
  justify-content: center; 
}

h2 {
  margin-bottom: 10px;
  margin-right: 20px;
  text-align: center; 
}

ul {
  list-style-type: none;
  padding: 0;
  max-height: 200px; 
  overflow-y: auto; 
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-grow: 1;
  width: 100%;
  overflow: hidden; 
  text-overflow: ellipsis;
  text-align: center; /* 将文本水平居中对齐 */
}

.buttons {
  display: flex;
}

.file-name {
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis;
}

li {
  margin-bottom: 10px;
}

button {
  margin-right: 10px;
}
</style>
