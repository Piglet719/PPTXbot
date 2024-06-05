<template>
  <footer id="bottom-tab-region">
    <div class="input-section">
      <input v-model="question" type="text" placeholder="Input here..." @keyup.enter="sendQuestion" />
      <button class="send-btn" @click="sendQuestion">
        <img src="@/components/home/content/assets/send_msg.png" />
      </button>
    </div>
  </footer>

  <div class="message-section" ref="messageSection">
    <div v-for="(message, index) in messages" :key="index" class="message-group">
      <div class="user-conversation" v-if="message.role === 'user'">
        <div class="message user-message">{{ message.content }}</div>
      </div>
      <div class="assistant-conversation" v-else>
        <div class="message assistant-message">{{ message.content }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import axios from 'axios';

const question = ref(""); 
const messages = ref([]); 

const sendQuestion = async () => {
  if (question.value.trim()) {
    // 添加用户消息到messages
    messages.value.push({ role: 'user', content: question.value });
    
    try {
      const response = await axios.post('http://testeb-env.eba-3tf5iadp.us-east-1.elasticbeanstalk.com/api/chat', { prompt: question.value });
      console.log('Response from backend:', response.data); 
      if (response.data.success && response.data.messages) {
        // 将助手的消息添加到messages
        response.data.messages.forEach(msg => {
          if (msg.role === 'assistant') {
            messages.value.push({ role: 'assistant', content: msg.content });
          }
        });
      }
    } catch (error) {
      console.error('Error sending question:', error);
    }
    question.value = ""; 
  }
  nextTick(() => {
    scrollToBottom();
  });
}

const scrollToBottom = () => {
  const messageSection = document.querySelector('.message-section');
  if (messageSection) {
    messageSection.scrollTop = messageSection.scrollHeight;
  }
}

onMounted(() => {
  scrollToBottom();
});

</script>

<style scoped lang="scss">

.message-section {
  width: calc(100%/2);
  transform: translate(40px,0);
  overflow-x: hidden;
  overflow-y: scroll;
  .message {
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 15px;
    max-width: 40%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .user-conversation {
    align-self: flex-end; 
    .user-message {
      margin-left: auto; 
      background-color: #ffffff; 
    }
  }

  .assistant-conversation {
    align-self: flex-start; 
    .assistant-message {
      background-color: #A5C2BB; 
      margin-right: auto; 
    }
  }
}


#bottom-tab-region {
  width: 100%;
  
  .input-section {
    position: fixed; // 固定位置
    bottom: 20px; // 距離底部 20px
    left: 50%; // 從左側 50%
    transform: translateX(-50%); // 向左移動 50% 以居中
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%; // 撑满整个宽度
    padding: 10px; // 增加 padding 以便更好看
    
    input {
      font-family: "Noto Sans TC-Bold", Helvetica;
      width: 70%;
      border: none;
      border-bottom: 2px solid #A5C2BB;
      outline: none;
      padding: 10px;
      border-radius: 4px;
      margin-right: 10px;
    }

    .send-btn {
      border: none;
      background-color: white;
      cursor: pointer;
      img {
        height: 25px;
      }
    }
  }
}

</style>
