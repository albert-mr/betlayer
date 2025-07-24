<template>
  <div class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
    <!-- Debate Header -->
    <div class="flex justify-between items-start mb-4">
      <div class="flex-1">
        <h3 class="text-lg font-medium text-gray-900 mb-2">{{ debate.assertion }}</h3>
        <div class="flex items-center text-sm text-gray-500 space-x-4">
          <span>Created by: <Address :address="debate.creator" /></span>
          <span>{{ formatTimeRemaining(debate.endTime) }}</span>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <span :class="getStatusColor(debate.status)" class="px-2 py-1 rounded-full text-xs font-medium">
          {{ debate.status.toUpperCase() }}
        </span>
      </div>
    </div>

    <!-- Betting Stats -->
    <div class="grid grid-cols-3 gap-4 mb-4">
      <div class="text-center p-3 bg-green-50 rounded-lg">
        <div class="text-sm font-medium text-green-800">AGREE</div>
        <div class="text-lg font-bold text-green-600">{{ debate.totalBets.agree }}</div>
        <div class="text-xs text-green-600">tokens</div>
      </div>
      <div class="text-center p-3 bg-red-50 rounded-lg">
        <div class="text-sm font-medium text-red-800">DISAGREE</div>
        <div class="text-lg font-bold text-red-600">{{ debate.totalBets.disagree }}</div>
        <div class="text-xs text-red-600">tokens</div>
      </div>
      <div class="text-center p-3 bg-yellow-50 rounded-lg">
        <div class="text-sm font-medium text-yellow-800">NEUTRAL</div>
        <div class="text-lg font-bold text-yellow-600">{{ debate.totalBets.neutral }}</div>
        <div class="text-xs text-yellow-600">tokens</div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="mb-4">
      <div class="flex text-xs text-gray-600 mb-1">
        <span>Total Pool: {{ totalPool }} tokens</span>
        <span class="ml-auto">{{ debate.argumentCount }} arguments</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div class="flex h-2 rounded-full overflow-hidden">
          <div 
            class="bg-green-500" 
            :style="{ width: agreePercentage + '%' }"
          ></div>
          <div 
            class="bg-red-500" 
            :style="{ width: disagreePercentage + '%' }"
          ></div>
          <div 
            class="bg-yellow-500" 
            :style="{ width: neutralPercentage + '%' }"
          ></div>
        </div>
      </div>
      <div class="flex justify-between text-xs text-gray-500 mt-1">
        <span>{{ agreePercentage.toFixed(1) }}% agree</span>
        <span>{{ disagreePercentage.toFixed(1) }}% disagree</span>
        <span>{{ neutralPercentage.toFixed(1) }}% neutral</span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-between items-center">
      <button
        @click="$emit('view-arguments', debate)"
        class="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center"
      >
        <span class="mr-1">💬</span>
        View Arguments ({{ debate.argumentCount }})
      </button>
      
      <div class="flex space-x-2">
        <button
          v-if="debate.status === 'active' && userAddress"
          @click="$emit('place-bet', debate)"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-sm"
        >
          Place Bet
        </button>
        <button
          v-if="debate.status === 'resolved'"
          @click="showResults = !showResults"
          class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded text-sm"
        >
          {{ showResults ? 'Hide' : 'Show' }} Results
        </button>
      </div>
    </div>

    <!-- Results Section (for resolved debates) -->
    <div v-if="debate.status === 'resolved' && showResults" class="mt-4 p-4 bg-gray-50 rounded-lg">
      <h4 class="font-medium text-gray-900 mb-2">Debate Resolution</h4>
      <div class="text-sm text-gray-600 mb-2">
        <strong>LLM Jury Decision:</strong> {{ debate.juryDecision }}
      </div>
      <div class="text-sm text-gray-600 mb-2">
        <strong>Winning Position:</strong> 
        <span :class="getPositionColor(debate.winningPosition)">
          {{ debate.winningPosition?.toUpperCase() }}
        </span>
      </div>
      <div class="text-sm text-gray-600">
        <strong>Tokens Distributed:</strong> {{ debate.tokensDistributed }} tokens
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Address from './Address.vue';

const props = defineProps({
  debate: {
    type: Object,
    required: true
  },
  userAddress: {
    type: String,
    default: null
  }
});

defineEmits(['place-bet', 'view-arguments']);

const showResults = ref(false);

const totalPool = computed(() => {
  return props.debate.totalBets.agree + props.debate.totalBets.disagree + props.debate.totalBets.neutral;
});

const agreePercentage = computed(() => {
  return totalPool.value > 0 ? (props.debate.totalBets.agree / totalPool.value) * 100 : 0;
});

const disagreePercentage = computed(() => {
  return totalPool.value > 0 ? (props.debate.totalBets.disagree / totalPool.value) * 100 : 0;
});

const neutralPercentage = computed(() => {
  return totalPool.value > 0 ? (props.debate.totalBets.neutral / totalPool.value) * 100 : 0;
});

const formatTimeRemaining = (endTime) => {
  const now = new Date();
  const end = new Date(endTime);
  const diff = end - now;
  
  if (diff <= 0) {
    return 'Ended';
  }
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  
  if (days > 0) {
    return `${days}d ${hours}h remaining`;
  } else if (hours > 0) {
    return `${hours}h remaining`;
  } else {
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    return `${minutes}m remaining`;
  }
};

const getStatusColor = (status) => {
  switch (status) {
    case 'active':
      return 'bg-green-100 text-green-800';
    case 'resolved':
      return 'bg-blue-100 text-blue-800';
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const getPositionColor = (position) => {
  switch (position) {
    case 'agree':
      return 'text-green-600 font-medium';
    case 'disagree':
      return 'text-red-600 font-medium';
    case 'neutral':
      return 'text-yellow-600 font-medium';
    default:
      return 'text-gray-600 font-medium';
  }
};
</script>

<style scoped>
/* Add any specific styles for the debate card */
</style> 