<template>
  <div class="space-y-6">
    <!-- Debate Info -->
    <div class="bg-gray-50 p-4 rounded-lg">
      <h4 class="font-medium text-gray-900 mb-2">{{ debate.assertion }}</h4>
      <div class="text-sm text-gray-600">
        Total Arguments: {{ totalArguments }} | Total Pool: {{ totalPool }} tokens
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="border-b border-gray-200">
      <nav class="-mb-px flex space-x-8">
        <button
          @click="activeFilter = 'all'"
          :class="[
            'py-2 px-1 border-b-2 font-medium text-sm',
            activeFilter === 'all'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          All Arguments ({{ totalArguments }})
        </button>
        <button
          @click="activeFilter = 'agree'"
          :class="[
            'py-2 px-1 border-b-2 font-medium text-sm',
            activeFilter === 'agree'
              ? 'border-green-500 text-green-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          Agree ({{ agreeArguments.length }})
        </button>
        <button
          @click="activeFilter = 'disagree'"
          :class="[
            'py-2 px-1 border-b-2 font-medium text-sm',
            activeFilter === 'disagree'
              ? 'border-red-500 text-red-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          Disagree ({{ disagreeArguments.length }})
        </button>
        <button
          @click="activeFilter = 'neutral'"
          :class="[
            'py-2 px-1 border-b-2 font-medium text-sm',
            activeFilter === 'neutral'
              ? 'border-yellow-500 text-yellow-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          Neutral ({{ neutralArguments.length }})
        </button>
      </nav>
    </div>

    <!-- Sort Options -->
    <div class="flex justify-between items-center">
      <div class="text-sm text-gray-600">
        Showing {{ filteredArguments.length }} arguments
      </div>
      <div class="flex items-center space-x-2">
        <label class="text-sm text-gray-600">Sort by:</label>
        <select 
          v-model="sortBy"
          class="text-sm border border-gray-300 rounded px-2 py-1"
        >
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
          <option value="amount">Highest Bet</option>
          <option value="likes">Most Liked</option>
        </select>
      </div>
    </div>

    <!-- Arguments List -->
    <div class="space-y-4">
      <div v-if="filteredArguments.length === 0" class="text-center py-8 text-gray-500">
        <div class="text-lg mb-2">📝</div>
        <div>No arguments yet for this position</div>
        <div class="text-sm">Be the first to share your thoughts!</div>
      </div>
      
      <div
        v-for="argument in filteredArguments"
        :key="argument.id"
        class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
      >
        <!-- Argument Header -->
        <div class="flex justify-between items-start mb-3">
          <div class="flex items-center space-x-3">
            <Address :address="argument.author" />
            <span :class="getPositionBadgeClass(argument.position)" 
                  class="px-2 py-1 rounded-full text-xs font-medium">
              {{ argument.position.toUpperCase() }}
            </span>
            <span class="text-xs text-gray-500">
              {{ formatTimeAgo(argument.timestamp) }}
            </span>
          </div>
          <div class="text-right">
            <div class="text-sm font-medium text-gray-900">
              {{ argument.betAmount }} tokens
            </div>
            <div class="text-xs text-gray-500">
              bet amount
            </div>
          </div>
        </div>

        <!-- Argument Content -->
        <div class="mb-3">
          <p class="text-gray-800 leading-relaxed">{{ argument.content }}</p>
        </div>

        <!-- Argument Footer -->
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-4">
            <button
              @click="likeArgument(argument.id)"
              :class="[
                'flex items-center space-x-1 text-sm',
                argument.isLikedByUser 
                  ? 'text-blue-600' 
                  : 'text-gray-500 hover:text-blue-600'
              ]"
            >
              <span>👍</span>
              <span>{{ argument.likes }}</span>
            </button>
            
            <button
              @click="reportArgument(argument.id)"
              class="flex items-center space-x-1 text-sm text-gray-500 hover:text-red-600"
            >
              <span>🚩</span>
              <span>Report</span>
            </button>
          </div>
          
          <div class="text-xs text-gray-500">
            ID: {{ argument.id.slice(0, 8) }}...
          </div>
        </div>
      </div>
    </div>

    <!-- Load More Button -->
    <div v-if="hasMoreArguments" class="text-center">
      <button
        @click="loadMoreArguments"
        class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded"
      >
        Load More Arguments
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Address from './Address.vue';

const props = defineProps({
  debate: {
    type: Object,
    required: true
  }
});

// State
const activeFilter = ref('all');
const sortBy = ref('newest');
const argumentsList = ref([]);
const hasMoreArguments = ref(false);

// Mock data - in real app this would come from API
const mockArguments = [
  {
    id: 'arg_1',
    author: '0x1234...5678',
    position: 'agree',
    content: 'Climate change is indeed the most pressing issue because it affects every aspect of human life, from food security to economic stability. The scientific consensus is overwhelming, and we\'re already seeing the effects worldwide.',
    betAmount: 50,
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
    likes: 12,
    isLikedByUser: false
  },
  {
    id: 'arg_2',
    author: '0x9876...5432',
    position: 'disagree',
    content: 'While climate change is important, I believe poverty and inequality are more pressing. Millions die from preventable diseases and lack of basic necessities every day. We need to prioritize immediate human suffering.',
    betAmount: 75,
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
    likes: 8,
    isLikedByUser: true
  },
  {
    id: 'arg_3',
    author: '0xabcd...efgh',
    position: 'neutral',
    content: 'Both climate change and social issues are interconnected. We can\'t solve one without addressing the other. A holistic approach that tackles environmental and social challenges simultaneously would be most effective.',
    betAmount: 30,
    timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000), // 6 hours ago
    likes: 15,
    isLikedByUser: false
  },
  {
    id: 'arg_4',
    author: '0xdef0...1234',
    position: 'agree',
    content: 'The IPCC reports clearly show we have less than a decade to prevent catastrophic warming. No other issue has such an urgent timeline with such far-reaching consequences for all of humanity.',
    betAmount: 100,
    timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000), // 8 hours ago
    likes: 20,
    isLikedByUser: false
  }
];

// Computed properties
const agreeArguments = computed(() => 
  argumentsList.value.filter(arg => arg.position === 'agree')
);

const disagreeArguments = computed(() => 
  argumentsList.value.filter(arg => arg.position === 'disagree')
);

const neutralArguments = computed(() => 
  argumentsList.value.filter(arg => arg.position === 'neutral')
);

const totalArguments = computed(() => argumentsList.value.length);

const totalPool = computed(() => 
  argumentsList.value.reduce((sum, arg) => sum + arg.betAmount, 0)
);

const filteredArguments = computed(() => {
  let filtered = argumentsList.value;
  
  // Filter by position
  if (activeFilter.value !== 'all') {
    filtered = filtered.filter(arg => arg.position === activeFilter.value);
  }
  
  // Sort arguments
  return filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'newest':
        return new Date(b.timestamp) - new Date(a.timestamp);
      case 'oldest':
        return new Date(a.timestamp) - new Date(b.timestamp);
      case 'amount':
        return b.betAmount - a.betAmount;
      case 'likes':
        return b.likes - a.likes;
      default:
        return 0;
    }
  });
});

// Methods
const getPositionBadgeClass = (position) => {
  switch (position) {
    case 'agree':
      return 'bg-green-100 text-green-800';
    case 'disagree':
      return 'bg-red-100 text-red-800';
    case 'neutral':
      return 'bg-yellow-100 text-yellow-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const formatTimeAgo = (timestamp) => {
  const now = new Date();
  const diff = now - new Date(timestamp);
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  
  if (days > 0) {
    return `${days}d ago`;
  } else if (hours > 0) {
    return `${hours}h ago`;
  } else if (minutes > 0) {
    return `${minutes}m ago`;
  } else {
    return 'Just now';
  }
};

const likeArgument = async (argumentId) => {
  const argument = argumentsList.value.find(arg => arg.id === argumentId);
  if (argument) {
    if (argument.isLikedByUser) {
      argument.likes--;
      argument.isLikedByUser = false;
    } else {
      argument.likes++;
      argument.isLikedByUser = true;
    }
  }
};

const reportArgument = (argumentId) => {
  // Handle reporting logic
  console.log('Reporting argument:', argumentId);
  // In real app, would show report modal or send to API
};

const loadMoreArguments = () => {
  // Load more arguments logic
  console.log('Loading more arguments...');
  hasMoreArguments.value = false; // For demo, hide after first click
};

// Initialize
onMounted(() => {
  argumentsList.value = mockArguments;
  hasMoreArguments.value = false; // For demo, no pagination
});
</script>

<style scoped>
/* Add any specific styles for the arguments list */
</style> 