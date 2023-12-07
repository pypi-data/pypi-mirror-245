# Agent Wallet Python SDK

The Agent Wallet Python SDK is a powerful tool designed to simplify the integration of your AI agent with the AgentWallet platform. This SDK allows you to easily manage your agent's account, perform transactions, and access wallet information programmatically.

## Key Features

- **Simple Account Management:** Create and manage your agent's account with ease.
- **Wallet Operations:** Retrieve wallet information, check balances, and perform fund transfers.
- **Seamless Integration:** Designed to work effortlessly with AgentWallet's API platform.
- **Secure Authentication:** Utilizes API keys for secure interactions with your agent's account.

## Getting Started

1. **Installation:**

  To start using the Agent Wallet SDK, check out the [Agent Wallet SDK GitHub repository](https://github.com/llmOS/agent-wallet-sdk) and install it using `pip`:

  ```bash
  git clone git@github.com:llmOS/agent-wallet-sdk.git
  cd agent-wallet-sdk
  pip install -e .
  ```

2. **Setting Up Your Account:**

  Import the Account class from the SDK and initialize it with your API key:

  ```python
  from agentwallet import Account

  account = Account.from_key("your-api-key")
  ```

3. **Managing Wallets:**

  Fetch wallet information and manage transactions:
  
  ```python
  # Fetch all wallets associated with the account
  wallets = account.get_wallets()
  print(f"Wallets: {wallets}")

  # Access a specific wallet
  wallet = account.get_wallet(wallets[0].wallet_uid)
  print(f"Wallet: {wallet}")

  # Perform a fund transfer
  transfer_ok = wallet.transfer("recipient@email.com", amount)
  print(f"Transfer successful: {transfer_ok}")

  # Check the new balance
  balance = wallet.balance()
  print(f"New balance: ${balance / 100:.2f}")
  ```

## Examples
  For more details, visit [Agent Wallet SDK GitHub repository](https://github.com/llmOS/agent-wallet-sdk). Here, you can find the source code and examples to help you integrate the SKD with your AI agent seamlessly.
