import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

class DebateBets {
  contractAddress;
  client;

  constructor(contractAddress, account = null, studioUrl = null) {
    this.contractAddress = contractAddress;
    const config = {
      chain: studionet,
      ...(account ? { account } : {}),
      ...(studioUrl ? { endpoint: studioUrl } : {}),
    };
    this.client = createClient(config);
  }

  updateAccount(account) {
    this.client = createClient({ chain: studionet, account });
  }

  async getDebates() {
    try {
      const debates = await this.client.readContract({
        address: this.contractAddress,
        functionName: "get_debates",
        args: [],
      });
      
      return Array.from(debates.entries()).map(([id, debateData]) => {
        const debateObj = Array.from(debateData.entries()).reduce((obj, [key, value]) => {
          obj[key] = value;
          return obj;
        }, {});

        return {
          id,
          ...debateObj,
        };
      });
    } catch (error) {
      console.error("Error fetching debates:", error);
      throw error;
    }
  }

  async createDebate(assertion, endTime) {
    try {
      const txHash = await this.client.writeContract({
        address: this.contractAddress,
        functionName: "create_debate",
        args: [assertion, endTime],
      });
      
      const receipt = await this.client.waitForTransactionReceipt({
        hash: txHash,
        status: "FINALIZED",
        interval: 10000,
      });
      
      return receipt;
    } catch (error) {
      console.error("Error creating debate:", error);
      throw error;
    }
  }

  async placeBet(debateId, position, amount, argument = null) {
    try {
      const txHash = await this.client.writeContract({
        address: this.contractAddress,
        functionName: "place_bet",
        args: [debateId, position, amount, argument],
      });
      
      const receipt = await this.client.waitForTransactionReceipt({
        hash: txHash,
        status: "FINALIZED",
        interval: 10000,
      });
      
      return receipt;
    } catch (error) {
      console.error("Error placing bet:", error);
      throw error;
    }
  }

  async getArguments(debateId) {
    try {
      const argumentsData = await this.client.readContract({
        address: this.contractAddress,
        functionName: "get_arguments",
        args: [debateId],
      });
      
      return Array.from(argumentsData.entries()).map(([id, argumentData]) => {
        const argumentObj = Array.from(argumentData.entries()).reduce((obj, [key, value]) => {
          obj[key] = value;
          return obj;
        }, {});

        return {
          id,
          ...argumentObj,
        };
      });
    } catch (error) {
      console.error("Error fetching arguments:", error);
      throw error;
    }
  }

  async getUserTokens(address) {
    if (!address) {
      return 0;
    }
    
    try {
      const tokens = await this.client.readContract({
        address: this.contractAddress,
        functionName: "get_user_tokens",
        args: [address],
      });
      return tokens;
    } catch (error) {
      console.error("Error fetching user tokens:", error);
      throw error;
    }
  }

  async getUserBets(address) {
    if (!address) {
      return [];
    }
    
    try {
      const bets = await this.client.readContract({
        address: this.contractAddress,
        functionName: "get_user_bets",
        args: [address],
      });
      
      return Array.from(bets.entries()).map(([id, betData]) => {
        const betObj = Array.from(betData.entries()).reduce((obj, [key, value]) => {
          obj[key] = value;
          return obj;
        }, {});

        return {
          id,
          ...betObj,
        };
      });
    } catch (error) {
      console.error("Error fetching user bets:", error);
      throw error;
    }
  }

  async getLeaderboard() {
    try {
      const leaderboard = await this.client.readContract({
        address: this.contractAddress,
        functionName: "get_leaderboard",
        args: [],
      });
      
      return Array.from(leaderboard.entries())
        .map(([address, tokens]) => ({
          address,
          tokens: Number(tokens),
        }))
        .sort((a, b) => b.tokens - a.tokens);
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
      throw error;
    }
  }

  async resolveDebate(debateId) {
    try {
      const txHash = await this.client.writeContract({
        address: this.contractAddress,
        functionName: "resolve_debate",
        args: [debateId],
      });
      
      const receipt = await this.client.waitForTransactionReceipt({
        hash: txHash,
        status: "FINALIZED",
        interval: 10000,
        retries: 20,
      });
      
      return receipt;
    } catch (error) {
      console.error("Error resolving debate:", error);
      throw error;
    }
  }

  async getDebateDetails(debateId) {
    try {
      const details = await this.client.readContract({
        address: this.contractAddress,
        functionName: "get_debate_details",
        args: [debateId],
      });
      
      const detailsObj = Array.from(details.entries()).reduce((obj, [key, value]) => {
        obj[key] = value;
        return obj;
      }, {});

      return detailsObj;
    } catch (error) {
      console.error("Error fetching debate details:", error);
      throw error;
    }
  }

  async likeArgument(argumentId) {
    try {
      const txHash = await this.client.writeContract({
        address: this.contractAddress,
        functionName: "like_argument",
        args: [argumentId],
      });
      
      const receipt = await this.client.waitForTransactionReceipt({
        hash: txHash,
        status: "FINALIZED",
        interval: 10000,
      });
      
      return receipt;
    } catch (error) {
      console.error("Error liking argument:", error);
      throw error;
    }
  }

  async reportArgument(argumentId, reason) {
    try {
      const txHash = await this.client.writeContract({
        address: this.contractAddress,
        functionName: "report_argument",
        args: [argumentId, reason],
      });
      
      const receipt = await this.client.waitForTransactionReceipt({
        hash: txHash,
        status: "FINALIZED",
        interval: 10000,
      });
      
      return receipt;
    } catch (error) {
      console.error("Error reporting argument:", error);
      throw error;
    }
  }
}

export default DebateBets; 