<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <!-- Header -->
    <header class="bg-slate-800 border-b border-slate-700 px-6 py-4">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <div class="flex items-center space-x-6">
          <h1 class="text-xl font-bold text-white">🎯 DebateBets</h1>
          <div class="hidden md:flex space-x-6 text-sm text-slate-300">
            <span class="text-emerald-400 font-medium">Trending</span>
            <span>Politics</span>
            <span>Tech</span>
            <span>Economy</span>
            <span>Culture</span>
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
          <div v-if="userAddress" class="text-right">
            <div class="text-sm text-slate-400">Balance</div>
            <div class="font-mono font-bold text-emerald-400">${{ userTokens.toLocaleString() }}</div>
          </div>
          <button
            v-if="!userAddress"
            @click="createUserAccount"
            class="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg font-medium transition-all duration-200"
          >
            Connect
          </button>
          <button
            v-else
            @click="openCreateModal"
            class="bg-emerald-500 hover:bg-emerald-600 px-4 py-2 rounded-lg font-medium transition-all duration-200"
          >
            Create Market
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto p-6">
      <!-- Markets Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="debate in debates"
          :key="debate.id"
          class="bg-slate-800 hover:bg-slate-750 border border-slate-700 rounded-xl p-5 transition-all duration-200 cursor-pointer transform hover:scale-[1.02]"
          @click="openDebateDetails(debate)"
        >
          <!-- Header with icon and agreement percentage -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-slate-700 rounded-full flex items-center justify-center text-sm">
                {{ getDebateIcon(debate.category) }}
              </div>
              <div class="flex-1">
                <h3 class="text-sm font-medium text-white leading-tight">
                  {{ debate.assertion }}
                </h3>
              </div>
            </div>
            <div class="text-right ml-3">
              <div class="text-2xl font-bold text-emerald-400">
                {{ getAgreePercentage(debate) }}%
              </div>
              <div class="text-xs text-slate-400">agree</div>
            </div>
          </div>

          <!-- Live Countdown -->
          <div class="mb-4 text-center">
            <div class="text-lg font-mono text-yellow-400">
              {{ getLiveCountdown(debate.endTime) }}
            </div>
            <div class="text-xs text-slate-400">remaining</div>
          </div>

          <!-- Betting Buttons - 3 options -->
          <div class="grid grid-cols-3 gap-2 mb-4">
            <button
              @click.stop="quickBet(debate, 'agree')"
              :disabled="!userAddress"
              class="bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-medium py-2 px-2 rounded-lg transition-all duration-200 text-xs flex items-center justify-center space-x-1"
            >
              <span>I Agree</span>
            </button>
            <button
              @click.stop="quickBet(debate, 'neutral')"
              :disabled="!userAddress"
              class="bg-yellow-600 hover:bg-yellow-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-medium py-2 px-2 rounded-lg transition-all duration-200 text-xs flex items-center justify-center space-x-1"
            >
              <span>Neutral</span>
            </button>
            <button
              @click.stop="quickBet(debate, 'disagree')"
              :disabled="!userAddress"
              class="bg-red-600 hover:bg-red-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-medium py-2 px-2 rounded-lg transition-all duration-200 text-xs flex items-center justify-center space-x-1"
            >
              <span>I Disagree</span>
            </button>
          </div>

          <!-- Market Info -->
          <div class="flex items-center justify-between text-xs text-slate-400">
            <span>${{ getTotalVolume(debate).toLocaleString() }} Vol.</span>
            <div class="flex items-center space-x-2">
              <span>{{ debate.totalArguments }} arguments</span>
              <div class="w-1 h-1 bg-slate-500 rounded-full"></div>
              <span>{{ debate.totalBets }} bets</span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Detailed Debate Modal -->
    <div
      v-if="showDetailModal"
      class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      @click="showDetailModal = false"
    >
      <div
        class="bg-slate-800 border border-slate-700 rounded-xl p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto"
        @click.stop
      >
        <div class="flex justify-between items-start mb-6">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <div class="w-10 h-10 bg-slate-700 rounded-full flex items-center justify-center">
                {{ getDebateIcon(selectedDebate?.category) }}
              </div>
              <h2 class="text-xl font-bold text-white">{{ selectedDebate?.assertion }}</h2>
            </div>
            <div class="text-lg font-mono text-yellow-400 mb-2">
              {{ getLiveCountdown(selectedDebate?.endTime) }} remaining
            </div>
          </div>
          <button
            @click="showDetailModal = false"
            class="text-slate-400 hover:text-white transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Statistics -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Betting Distribution -->
            <div class="bg-slate-900 rounded-lg p-4">
              <h3 class="text-lg font-semibold mb-4">Betting Distribution</h3>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <div class="w-3 h-3 bg-emerald-500 rounded-full"></div>
                    <span>I Agree</span>
                  </div>
                  <div class="flex items-center space-x-4">
                    <span class="font-mono">${{ selectedDebate?.agreeShares || 0 }}</span>
                    <span class="text-emerald-400 font-bold">{{ getAgreePercentage(selectedDebate) }}%</span>
                  </div>
                </div>
                <div class="w-full bg-slate-700 rounded-full h-2">
                  <div
                    class="bg-emerald-500 h-2 rounded-full transition-all duration-500"
                    :style="{ width: getAgreePercentage(selectedDebate) + '%' }"
                  ></div>
                </div>

                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                    <span>I Disagree</span>
                  </div>
                  <div class="flex items-center space-x-4">
                    <span class="font-mono">${{ selectedDebate?.disagreeShares || 0 }}</span>
                    <span class="text-red-400 font-bold">{{ getDisagreePercentage(selectedDebate) }}%</span>
                  </div>
                </div>
                <div class="w-full bg-slate-700 rounded-full h-2">
                  <div
                    class="bg-red-500 h-2 rounded-full transition-all duration-500"
                    :style="{ width: getDisagreePercentage(selectedDebate) + '%' }"
                  ></div>
                </div>

                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <span>Neutral</span>
                  </div>
                  <div class="flex items-center space-x-4">
                    <span class="font-mono">${{ selectedDebate?.neutralShares || 0 }}</span>
                    <span class="text-yellow-400 font-bold">{{ getNeutralPercentage(selectedDebate) }}%</span>
                  </div>
                </div>
                <div class="w-full bg-slate-700 rounded-full h-2">
                  <div
                    class="bg-yellow-500 h-2 rounded-full transition-all duration-500"
                    :style="{ width: getNeutralPercentage(selectedDebate) + '%' }"
                  ></div>
                </div>
              </div>
            </div>

            <!-- Recent Arguments -->
            <div class="bg-slate-900 rounded-lg p-4">
              <h3 class="text-lg font-semibold mb-4">Recent Arguments</h3>
              <div class="space-y-3 max-h-60 overflow-y-auto">
                <div
                  v-for="argument in mockArguments.slice(0, 5)"
                  :key="argument.id"
                  class="border border-slate-700 rounded-lg p-3"
                >
                  <div class="flex items-start justify-between mb-2">
                    <div class="flex items-center space-x-2">
                      <div :class="getPositionColor(argument.position)" class="px-2 py-1 rounded text-xs font-medium">
                        {{ argument.position.toUpperCase() }}
                      </div>
                      <span class="text-sm text-slate-400">{{ argument.author.slice(0, 8) }}...</span>
                    </div>
                    <span class="text-xs text-slate-500">{{ formatTimeAgo(argument.timestamp) }}</span>
                  </div>
                  <p class="text-sm text-slate-300">{{ argument.content }}</p>
                  <div class="mt-2 text-xs text-slate-400">
                    Bet: ${{ argument.betAmount }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="space-y-4">
            <div class="bg-slate-900 rounded-lg p-4">
              <h3 class="text-lg font-semibold mb-4">Place Your Bet</h3>
              <div class="space-y-3">
                <button
                  @click="quickBet(selectedDebate, 'agree')"
                  class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-3 rounded-lg transition-all duration-200"
                >
                  I Agree ({{ getAgreePercentage(selectedDebate) }}%)
                </button>
                <button
                  @click="quickBet(selectedDebate, 'neutral')"
                  class="w-full bg-yellow-600 hover:bg-yellow-500 text-white font-medium py-3 rounded-lg transition-all duration-200"
                >
                  Neutral ({{ getNeutralPercentage(selectedDebate) }}%)
                </button>
                <button
                  @click="quickBet(selectedDebate, 'disagree')"
                  class="w-full bg-red-600 hover:bg-red-500 text-white font-medium py-3 rounded-lg transition-all duration-200"
                >
                  I Disagree ({{ getDisagreePercentage(selectedDebate) }}%)
                </button>
              </div>
            </div>

            <!-- Market Stats -->
            <div class="bg-slate-900 rounded-lg p-4">
              <h3 class="text-lg font-semibold mb-4">Market Stats</h3>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-slate-400">Total Volume</span>
                  <span class="font-mono">${{ getTotalVolume(selectedDebate).toLocaleString() }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">Total Bets</span>
                  <span class="font-mono">{{ selectedDebate?.totalBets || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">Arguments</span>
                  <span class="font-mono">{{ selectedDebate?.totalArguments || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">Created by</span>
                  <span class="font-mono text-xs">{{ selectedDebate?.creator?.slice(0, 8) }}...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Market Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      @click="showCreateModal = false"
    >
      <div
        class="bg-slate-800 border border-slate-700 rounded-xl p-6 w-full max-w-md"
        @click.stop
      >
        <h3 class="text-lg font-bold mb-4">Create New Market</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-2">Question</label>
            <textarea
              v-model="newAssertion"
              class="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-white placeholder-slate-400 focus:border-blue-500 focus:outline-none transition-colors"
              placeholder="Will X happen by Y date?"
              rows="3"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-2">Duration (hours)</label>
            <select
              v-model="duration"
              class="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-white focus:border-blue-500 focus:outline-none transition-colors"
            >
              <option value="2">2 hours</option>
              <option value="6">6 hours</option>
              <option value="12">12 hours</option>
              <option value="24">24 hours</option>
            </select>
          </div>
          <div class="flex space-x-3 pt-2">
            <button
              @click="showCreateModal = false"
              class="flex-1 bg-slate-700 hover:bg-slate-600 text-white py-2 rounded-lg transition-all duration-200"
            >
              Cancel
            </button>
            <button
              @click="createMarket"
              :disabled="creating"
              class="flex-1 bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-white py-2 rounded-lg transition-all duration-200"
            >
              {{ creating ? 'Creating...' : 'Create Market' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Bet Modal -->
    <div
      v-if="showBetModal"
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      @click="showBetModal = false"
    >
      <div
        class="bg-slate-800 border border-slate-700 rounded-xl p-6 w-full max-w-md"
        @click.stop
      >
        <h3 class="text-lg font-bold mb-4">Place Your Bet</h3>
        <div class="space-y-4">
          <div class="bg-slate-900 rounded-lg p-4">
            <div class="text-sm text-slate-400 mb-1">Market</div>
            <div class="text-sm font-medium">{{ selectedDebate?.assertion }}</div>
          </div>
          
          <div>
            <div class="text-sm text-slate-400 mb-2">Your Position</div>
            <div :class="getPositionTextColor(selectedPosition)" class="text-lg font-bold">
              {{ getPositionText(selectedPosition) }}
            </div>
          </div>

          <div>
            <div class="text-sm text-slate-400 mb-2">Bet Amount</div>
            <input
              v-model.number="betAmount"
              type="number"
              min="1"
              :max="userTokens"
              class="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-white font-mono text-lg focus:border-blue-500 focus:outline-none transition-colors"
              placeholder="0"
            />
            <div class="flex space-x-2 mt-2">
              <button
                v-for="amount in [10, 25, 100, 500]"
                :key="amount"
                @click="betAmount = amount"
                class="flex-1 bg-slate-700 hover:bg-slate-600 py-1 px-2 rounded text-sm transition-all duration-200"
              >
                ${{ amount }}
              </button>
            </div>
          </div>

          <!-- Argument Input for Agree/Disagree -->
          <div v-if="selectedPosition !== 'neutral'" class="space-y-2">
            <div class="text-sm text-slate-400">Supporting Argument (Optional)</div>
            <textarea
              v-model="betArgument"
              class="w-full bg-slate-900 border border-slate-600 rounded-lg p-3 text-white placeholder-slate-400 focus:border-blue-500 focus:outline-none transition-colors resize-none"
              placeholder="Share your reasoning for this position..."
              rows="3"
              maxlength="500"
            ></textarea>
            <div class="text-xs text-slate-500 text-right">
              {{ betArgument.length }}/500 characters
            </div>
          </div>

          <div class="bg-slate-900 rounded-lg p-4">
            <div class="flex justify-between text-sm mb-2">
              <span class="text-slate-400">Potential Return</span>
              <span class="font-mono font-bold text-emerald-400">
                ${{ Math.floor(betAmount * getPayout(selectedDebate, selectedPosition)) }}
              </span>
            </div>
            <div class="flex justify-between text-xs text-slate-500">
              <span>Current Odds</span>
              <span>{{ (getPayout(selectedDebate, selectedPosition)).toFixed(2) }}x</span>
            </div>
          </div>

          <div class="flex space-x-3">
            <button
              @click="showBetModal = false"
              class="flex-1 bg-slate-700 hover:bg-slate-600 text-white py-2 rounded-lg transition-all duration-200"
            >
              Cancel
            </button>
            <button
              @click="confirmBet"
              :disabled="!betAmount || betAmount > userTokens"
              class="flex-1 bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-white py-2 rounded-lg transition-all duration-200"
            >
              Place Bet
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";

const userAccount = ref(null);
const userTokens = ref(0);
const userAddress = computed(() => userAccount.value?.address);

const debates = ref([]);
const showCreateModal = ref(false);
const showBetModal = ref(false);
const showDetailModal = ref(false);
const selectedDebate = ref(null);
const selectedPosition = ref('');
const betAmount = ref(25);
const betArgument = ref('');

// Form data
const newAssertion = ref("");
const duration = ref("6");
const creating = ref(false);

// Live countdown
const currentTime = ref(new Date());
let countdownInterval = null;

// Mock arguments data
const mockArguments = ref([
  {
    id: '1',
    position: 'agree',
    author: '0x1234567890abcdef',
    content: 'The rapid advancement in transformer architectures and compute scaling suggests we\'re closer than many think.',
    betAmount: 150,
    timestamp: new Date(Date.now() - 1000 * 60 * 30) // 30 min ago
  },
  {
    id: '2', 
    position: 'disagree',
    author: '0x9876543210fedcba',
    content: 'Current AI lacks true understanding and reasoning. We need breakthrough in consciousness research first.',
    betAmount: 200,
    timestamp: new Date(Date.now() - 1000 * 60 * 45) // 45 min ago
  },
  {
    id: '3',
    position: 'agree',
    author: '0xabcdef1234567890',
    content: 'OpenAI and Google are making unprecedented progress. AGI is inevitable within this decade.',
    betAmount: 75,
    timestamp: new Date(Date.now() - 1000 * 60 * 60) // 1 hour ago
  }
]);

// Methods
const createUserAccount = async () => {
  userAccount.value = {
    address: '0x' + Math.random().toString(16).substr(2, 40)
  };
  userTokens.value = 1000;
};

const openCreateModal = () => {
  showCreateModal.value = true;
};

const createMarket = async () => {
  if (newAssertion.value.trim()) {
    creating.value = true;
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const endTime = new Date();
    endTime.setHours(endTime.getHours() + parseInt(duration.value));
    
    const newMarket = {
      id: String(debates.value.length + 1),
      assertion: newAssertion.value,
      category: 'general',
      creator: userAddress.value,
      endTime: endTime.toISOString(),
      agreeShares: Math.floor(Math.random() * 500) + 100,
      disagreeShares: Math.floor(Math.random() * 500) + 100,
      neutralShares: Math.floor(Math.random() * 200) + 50,
      volume: Math.floor(Math.random() * 20000) + 5000,
      totalBets: Math.floor(Math.random() * 50) + 10,
      totalArguments: Math.floor(Math.random() * 20) + 5,
      status: 'active'
    };
    
    debates.value.unshift(newMarket);
    
    newAssertion.value = "";
    duration.value = "6";
    showCreateModal.value = false;
    creating.value = false;
  }
};

const quickBet = (debate, position) => {
  selectedDebate.value = debate;
  selectedPosition.value = position;
  betArgument.value = '';
  showBetModal.value = true;
};

const openDebateDetails = (debate) => {
  selectedDebate.value = debate;
  showDetailModal.value = true;
};

const confirmBet = async () => {
  if (selectedDebate.value && betAmount.value && betAmount.value <= userTokens.value) {
    const debate = selectedDebate.value;
    
    // Update market data
    const shareKey = selectedPosition.value + 'Shares';
    debate[shareKey] += betAmount.value;
    debate.volume += betAmount.value;
    debate.totalBets += 1;
    
    // If user provided an argument, increase argument count
    if (betArgument.value.trim() && selectedPosition.value !== 'neutral') {
      debate.totalArguments += 1;
      
      // Add to mock arguments
      mockArguments.value.unshift({
        id: String(mockArguments.value.length + 1),
        position: selectedPosition.value,
        author: userAddress.value,
        content: betArgument.value.trim(),
        betAmount: betAmount.value,
        timestamp: new Date()
      });
    }
    
    // Update user tokens
    userTokens.value -= betAmount.value;
    
    showBetModal.value = false;
    betAmount.value = 25;
    betArgument.value = '';
  }
};

// Live countdown functionality
const startCountdown = () => {
  countdownInterval = setInterval(() => {
    currentTime.value = new Date();
  }, 1000);
};

const getLiveCountdown = (endTime) => {
  if (!endTime) return 'N/A';
  
  const now = currentTime.value;
  const end = new Date(endTime);
  const diff = end - now;
  
  if (diff <= 0) return 'ENDED';
  
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);
  
  if (hours > 0) {
    return `${hours}h ${minutes}m ${seconds}s`;
  } else if (minutes > 0) {
    return `${minutes}m ${seconds}s`;
  } else {
    return `${seconds}s`;
  }
};

// Percentage calculations
const getAgreePercentage = (debate) => {
  if (!debate) return 0;
  const total = debate.agreeShares + debate.disagreeShares + debate.neutralShares;
  return Math.round((debate.agreeShares / total) * 100);
};

const getDisagreePercentage = (debate) => {
  if (!debate) return 0;
  const total = debate.agreeShares + debate.disagreeShares + debate.neutralShares;
  return Math.round((debate.disagreeShares / total) * 100);
};

const getNeutralPercentage = (debate) => {
  if (!debate) return 0;
  const total = debate.agreeShares + debate.disagreeShares + debate.neutralShares;
  return Math.round((debate.neutralShares / total) * 100);
};

const getTotalVolume = (debate) => {
  return debate?.volume || 0;
};

const getPayout = (debate, position) => {
  if (!debate) return 1;
  
  const total = debate.agreeShares + debate.disagreeShares + debate.neutralShares;
  const positionShares = debate[position + 'Shares'];
  const otherShares = total - positionShares;
  
  if (positionShares === 0) return 3.0;
  return Math.max(1.1, Math.min(10.0, total / positionShares));
};

const getPositionColor = (position) => {
  const colors = {
    agree: 'bg-emerald-900 text-emerald-300',
    disagree: 'bg-red-900 text-red-300',
    neutral: 'bg-yellow-900 text-yellow-300'
  };
  return colors[position] || 'bg-slate-700 text-slate-300';
};

const getPositionTextColor = (position) => {
  const colors = {
    agree: 'text-emerald-400',
    disagree: 'text-red-400',
    neutral: 'text-yellow-400'
  };
  return colors[position] || 'text-slate-400';
};

const getPositionText = (position) => {
  const texts = {
    agree: 'I AGREE',
    disagree: 'I DISAGREE',
    neutral: 'NEUTRAL'
  };
  return texts[position] || '';
};

const getDebateIcon = (category) => {
  const icons = {
    politics: '🏛️',
    tech: '💻',
    economy: '📈',
    culture: '🎭',
    general: '💭'
  };
  return icons[category] || '💭';
};

const formatTimeAgo = (timestamp) => {
  const now = new Date();
  const diff = now - new Date(timestamp);
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(diff / (1000 * 60 * 60));
  
  if (hours > 0) return `${hours}h ago`;
  if (minutes > 0) return `${minutes}m ago`;
  return 'Just now';
};

// Initialize with mock data (shorter times)
const loadDebates = () => {
  const now = new Date();
  
  debates.value = [
    {
      id: '1',
      assertion: 'AI will achieve AGI before 2030',
      category: 'tech',
      creator: '0x1234567890abcdef12345678',
      endTime: new Date(now.getTime() + 4 * 60 * 60 * 1000).toISOString(), // 4 hours
      agreeShares: 680,
      disagreeShares: 1320,
      neutralShares: 200,
      volume: 45200,
      totalBets: 156,
      totalArguments: 23,
      status: 'active'
    },
    {
      id: '2',
      assertion: 'Bitcoin will reach $500,000 by end of 2025',
      category: 'economy',
      creator: '0x9876543210fedcba87654321',
      endTime: new Date(now.getTime() + 8 * 60 * 60 * 1000).toISOString(), // 8 hours
      agreeShares: 1200,
      disagreeShares: 800,
      neutralShares: 300,
      volume: 78300,
      totalBets: 89,
      totalArguments: 31,
      status: 'active'
    },
    {
      id: '3',
      assertion: 'Remote work will be dominant by 2030',
      category: 'culture',
      creator: '0xabcdef1234567890abcdef12',
      endTime: new Date(now.getTime() + 2 * 60 * 60 * 1000).toISOString(), // 2 hours
      agreeShares: 1500,
      disagreeShares: 500,
      neutralShares: 100,
      volume: 32100,
      totalBets: 67,
      totalArguments: 12,
      status: 'active'
    },
    {
      id: '4',
      assertion: 'SpaceX will land humans on Mars by 2028',
      category: 'tech',
      creator: '0xfedcba0987654321fedcba09',
      endTime: new Date(now.getTime() + 12 * 60 * 60 * 1000).toISOString(), // 12 hours
      agreeShares: 400,
      disagreeShares: 1600,
      neutralShares: 300,
      volume: 25800,
      totalBets: 43,
      totalArguments: 18,
      status: 'active'
    }
  ];
};

onMounted(() => {
  loadDebates();
  startCountdown();
});

onUnmounted(() => {
  if (countdownInterval) {
    clearInterval(countdownInterval);
  }
});
</script>

<style scoped>
.bg-slate-750 {
  background-color: rgb(55 65 81 / 0.8);
}

/* Smooth scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgb(51 65 85);
}

::-webkit-scrollbar-thumb {
  background: rgb(100 116 139);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgb(148 163 184);
}

/* Animation for cards */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.grid > div {
  animation: slideIn 0.5s ease-out;
}
</style> 