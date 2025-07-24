<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-75 overflow-y-auto h-full w-full flex items-center justify-center z-50">
    <div class="relative p-6 border w-full max-w-md shadow-lg rounded-md bg-white">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-medium leading-6 text-gray-900">Place Your Bet</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <span class="sr-only">Close</span>
          ✕
        </button>
      </div>

      <!-- Debate Info -->
      <div class="mb-6 p-4 bg-gray-50 rounded-lg">
        <p class="text-sm font-medium text-gray-900 mb-2">Debate:</p>
        <p class="text-sm text-gray-600">{{ debate.assertion }}</p>
      </div>

      <!-- Position Selection -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Your Position
        </label>
        <div class="grid grid-cols-3 gap-2">
          <button
            @click="selectedPosition = 'agree'"
            :class="[
              'p-3 rounded-lg border-2 transition-colors',
              selectedPosition === 'agree'
                ? 'border-green-500 bg-green-50 text-green-800'
                : 'border-gray-300 hover:border-green-300'
            ]"
          >
            <div class="text-center">
              <div class="text-lg">✅</div>
              <div class="text-sm font-medium">AGREE</div>
            </div>
          </button>
          <button
            @click="selectedPosition = 'disagree'"
            :class="[
              'p-3 rounded-lg border-2 transition-colors',
              selectedPosition === 'disagree'
                ? 'border-red-500 bg-red-50 text-red-800'
                : 'border-gray-300 hover:border-red-300'
            ]"
          >
            <div class="text-center">
              <div class="text-lg">❌</div>
              <div class="text-sm font-medium">DISAGREE</div>
            </div>
          </button>
          <button
            @click="selectedPosition = 'neutral'"
            :class="[
              'p-3 rounded-lg border-2 transition-colors',
              selectedPosition === 'neutral'
                ? 'border-yellow-500 bg-yellow-50 text-yellow-800'
                : 'border-gray-300 hover:border-yellow-300'
            ]"
          >
            <div class="text-center">
              <div class="text-lg">⚖️</div>
              <div class="text-sm font-medium">NEUTRAL</div>
            </div>
          </button>
        </div>
      </div>

      <!-- Bet Amount -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Bet Amount (tokens)
        </label>
        <input
          v-model.number="betAmount"
          type="number"
          min="1"
          :max="maxBet"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          placeholder="Enter amount"
        />
        <div class="mt-1 flex justify-between text-xs text-gray-500">
          <span>Minimum: 1 token</span>
          <span>Available: {{ maxBet }} tokens</span>
        </div>
      </div>

      <!-- Quick Amount Buttons -->
      <div class="mb-4">
        <div class="flex space-x-2">
          <button
            v-for="amount in quickAmounts"
            :key="amount"
            @click="betAmount = amount"
            class="flex-1 py-1 px-2 text-xs border border-gray-300 rounded hover:bg-gray-50"
          >
            {{ amount }}
          </button>
        </div>
      </div>

      <!-- Argument (Optional) -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Supporting Argument (Optional)
        </label>
        <textarea
          v-model="argument"
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          placeholder="Explain your reasoning... (This will be visible to other users and considered by the LLM jury)"
        ></textarea>
        <div class="mt-1 text-xs text-gray-500">
          {{ argument.length }}/500 characters
        </div>
      </div>

      <!-- Bet Summary -->
      <div v-if="selectedPosition && betAmount" class="mb-4 p-3 bg-blue-50 rounded-lg">
        <div class="text-sm">
          <div class="flex justify-between">
            <span>Position:</span>
            <span :class="getPositionColor(selectedPosition)" class="font-medium">
              {{ selectedPosition.toUpperCase() }}
            </span>
          </div>
          <div class="flex justify-between">
            <span>Amount:</span>
            <span class="font-medium">{{ betAmount }} tokens</span>
          </div>
          <div class="flex justify-between">
            <span>Potential Return:</span>
            <span class="font-medium text-green-600">{{ potentialReturn }} tokens</span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-2">
        <button
          @click="$emit('close')"
          class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
        >
          Cancel
        </button>
        <button
          @click="placeBet"
          :disabled="!canPlaceBet || placingBet"
          :class="[
            'flex-1 font-bold py-2 px-4 rounded',
            canPlaceBet && !placingBet
              ? 'bg-blue-500 hover:bg-blue-700 text-white'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          ]"
        >
          {{ placingBet ? 'Placing Bet...' : 'Place Bet' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  debate: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close', 'bet-placed']);

// Form state
const selectedPosition = ref('');
const betAmount = ref(10);
const argument = ref('');
const placingBet = ref(false);

// Mock user token balance - in real app this would come from props or store
const maxBet = ref(1000);

const quickAmounts = computed(() => {
  const amounts = [10, 25, 50, 100];
  return amounts.filter(amount => amount <= maxBet.value);
});

const canPlaceBet = computed(() => {
  return selectedPosition.value && 
         betAmount.value && 
         betAmount.value >= 1 && 
         betAmount.value <= maxBet.value &&
         argument.value.length <= 500;
});

const potentialReturn = computed(() => {
  if (!selectedPosition.value || !betAmount.value) return 0;
  
  // Simple calculation - in real app would be more sophisticated
  const totalPool = props.debate.totalBets.agree + props.debate.totalBets.disagree + props.debate.totalBets.neutral;
  const currentPositionTotal = props.debate.totalBets[selectedPosition.value];
  const otherPositionsTotal = totalPool - currentPositionTotal;
  
  if (otherPositionsTotal === 0) return betAmount.value;
  
  // Calculate potential return based on pool distribution
  const winningShare = betAmount.value / (currentPositionTotal + betAmount.value);
  const totalPrize = totalPool + betAmount.value;
  
  return Math.floor(totalPrize * winningShare);
});

const getPositionColor = (position) => {
  switch (position) {
    case 'agree':
      return 'text-green-600';
    case 'disagree':
      return 'text-red-600';
    case 'neutral':
      return 'text-yellow-600';
    default:
      return 'text-gray-600';
  }
};

const placeBet = async () => {
  if (!canPlaceBet.value) return;
  
  placingBet.value = true;
  
  try {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Emit the bet data
    emit('bet-placed', {
      debateId: props.debate.id,
      position: selectedPosition.value,
      amount: betAmount.value,
      argument: argument.value.trim() || null
    });
    
    // Close the modal
    emit('close');
  } catch (error) {
    console.error('Error placing bet:', error);
  } finally {
    placingBet.value = false;
  }
};
</script>

<style scoped>
/* Add any specific styles for the bet form */
</style> 