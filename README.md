# Crypto & Currency Chatbot - API Integration

A chatbot that pulls real-time cryptocurrency prices and currency exchange rates using OpenAI function calling. Built with Streamlit for an interactive web interface.


## Requirements

Install the dependencies:

```
pip install openai requests streamlit
```

You will also need an OpenAI API key. Get one at https://platform.openai.com/api-keys


## How to Run

1. Open `crypto_chatbot.py` and replace the placeholder with your OpenAI API key:

```python
OPENAI_API_KEY = "your-openai-api-key-here"
```

2. Run the app:

```
streamlit run crypto_chatbot.py
```


## How It Works

The chatbot uses OpenAI's function calling feature to decide when and how to query the APIs.

1. **User Input** - The user asks a question like "What's the price of Ethereum?"
2. **Tool Selection** - The LLM reads the tool descriptions and picks `get_crypto_price`.
3. **API Call** - The function makes an HTTP request to the CoinGecko API.
4. **Response Parsing** - The JSON response is parsed and formatted.
5. **Final Answer** - The LLM generates a natural language response for the user.



The chatbot can convert between crypto and any fiat currency by chaining both APIs.

## Sample Queries

The chatbot can handle requests like:

1. "What's the price of Bitcoin?"
2. "Convert 1.5 ETH to NGN"
3. "How much Bitcoin can I get for 500000 NGN?"
4. "Show me the top cryptocurrencies"
5. "Convert 100 USD to EUR"
6. "What's the exchange rate from NGN to GBP?"

## APIs Used

Both APIs are free and require no API key.

- **CoinGecko API** (Cryptocurrency data)

  Full docs: https://www.coingecko.com/en/api/documentation

- **Currency Exchange API** (Fiat currency data)

  Supports 150+ currencies including USD, EUR, GBP, NGN, JPY, CNY.

  Source: https://github.com/fawazahmed0/exchange-api


