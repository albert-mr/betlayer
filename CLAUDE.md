# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a GenLayer intelligent contract project implementing a football betting dApp. The project consists of:
- A Python smart contract (`contracts/football_bets.py`) that runs on GenLayer network
- A Vue.js frontend application (`app/`) for user interaction
- Integration tests for contract functionality

## Common Commands

### Contract Development
- Deploy contract: `genlayer deploy` (runs `deploy/deployScript.ts`)
- Switch networks: `genlayer network` (choose studionet, localnet, or tesnet-*)
- Run contract tests: `gltest` (requires Python virtual environment with `requirements.txt`)

### Frontend Development
```bash
cd app
npm install
npm run dev     # Start development server (usually http://localhost:5173)
npm run build   # Build for production
npm run preview # Preview production build
```

### Testing
- Contract tests: `gltest` (from project root, requires Python virtual environment)
- Individual test files can be run with pytest-style patterns
- Frontend has no specific test commands configured

## Architecture

### Smart Contract (`contracts/football_bets.py`)
- Built using GenLayer framework with `genlayer` imports
- Main contract class: `FootballBets`
- Uses web scraping via `gl.get_webpage()` and AI via `gl.exec_prompt()` for match result resolution
- Storage: `TreeMap[Address, TreeMap[str, Bet]]` for bets, `TreeMap[Address, u256]` for points
- Key methods:
  - `create_bet()`: Creates new football match bets
  - `resolve_bet()`: Resolves bets using BBC Sport data
  - `get_bets()`, `get_points()`, `get_player_points()`: Query methods

### Frontend (`app/src/`)
- Vue 3 + Vite + Tailwind CSS
- Single main component: `BetsScreen.vue`
- GenLayer integration via `genlayer-js` SDK in `services/genlayer.js`
- Uses `studionet` chain configuration
- Account management with localStorage persistence

### Configuration
- Frontend environment: Copy `app/.env.example` to `app/.env` and set:
  - `VITE_CONTRACT_ADDRESS`: Deployed contract address
  - `VITE_STUDIO_URL`: GenLayer Studio backend URL
- Contract config: `config/genlayer_config.py` reads from environment variables

### Key Dependencies
- Contract: `genlayer` framework for intelligent contracts
- Frontend: `genlayer-js` SDK, Vue 3, Vite, Tailwind CSS, Lucide Vue Next icons
- Testing: `genlayer-test` framework with `gltest` command
- Python deps: requests, python-dotenv, eth-account, eth-utils

## Deployment Workflow
1. Ensure GenLayer Studio is running (local or hosted at studio.genlayer.com)
2. Select network with `genlayer network`
3. Deploy with `genlayer deploy`
4. Copy contract address to `app/.env`
5. Start frontend with `cd app && npm run dev`

## Testing Notes
- Contract tests use fixture-based approach with `load_fixture(deploy_contract)`
- Tests cover win/draw/loss scenarios with real match data resolution
- Long-running operations use `wait_interval=10000` and `wait_retries=15` for AI processing
- Test files: `test_footbal_bet.py` (main tests), `test_debate_bets.py` (additional scenarios)
- Tests require GenLayer Studio to be running and accessible

## Development Notes
- Contract uses AI via `gl.exec_prompt()` for match result interpretation from web data
- Web scraping via `gl.get_webpage()` fetches live match data from resolution URLs
- Storage pattern: nested TreeMaps for player bets and points tracking
- Deployment script at `deploy/deployScript.ts` handles contract deployment with proper error handling