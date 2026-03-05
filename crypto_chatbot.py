import json
import requests
import streamlit as st
from openai import OpenAI

# Replace with your OpenAI API key
OPENAI_API_KEY = "your-openai-api-key-here"

# API base URLs (both free, no keys needed)
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
CURRENCY_BASE = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"


# Function to get current price of a cryptocurrency
def get_crypto_price(coin):
    coin = coin.lower().strip()
    url = f"{COINGECKO_BASE}/simple/price?ids={coin}&vs_currencies=usd,eur,gbp&include_24hr_change=true"
    response = requests.get(url)
    data = response.json()
    
    if not data or coin not in data:
        return f"Couldn't find price for '{coin}'. Try bitcoin, ethereum, solana, etc."
    
    info = data[coin]
    return (
        f"{coin.title()} Price:\n"
        f"- USD: ${info['usd']:,.2f}\n"
        f"- EUR: €{info['eur']:,.2f}\n"
        f"- GBP: £{info['gbp']:,.2f}\n"
        f"- 24h Change: {info.get('usd_24h_change', 0):.2f}%"
    )


# Function to get top cryptocurrencies by market cap
def get_top_cryptos():
    url = f"{COINGECKO_BASE}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
    response = requests.get(url)
    data = response.json()
    
    if not data:
        return "Couldn't fetch top cryptocurrencies."
    
    results = []
    for i, coin in enumerate(data, 1):
        change = coin.get('price_change_percentage_24h', 0) or 0
        results.append(f"{i}. {coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']:,.2f} ({change:+.2f}%)")
    
    return "Top 10 Cryptocurrencies:\n" + "\n".join(results)


# Function to get trending cryptocurrencies
def get_trending_cryptos():
    url = f"{COINGECKO_BASE}/search/trending"
    response = requests.get(url)
    data = response.json()
    
    if not data or "coins" not in data:
        return "Couldn't fetch trending cryptocurrencies."
    
    results = []
    for item in data["coins"][:7]:
        coin = item["item"]
        results.append(f"- {coin['name']} ({coin['symbol']})")
    
    return "Trending Cryptocurrencies:\n" + "\n".join(results)


# Function to convert currency
def convert_currency(amount, from_currency, to_currency):
    from_curr = from_currency.lower().strip()
    to_curr = to_currency.lower().strip()
    
    url = f"{CURRENCY_BASE}/{from_curr}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Couldn't find currency '{from_currency.upper()}'."
    
    data = response.json()
    rates = data.get(from_curr, {})
    
    if to_curr not in rates:
        return f"Couldn't find currency '{to_currency.upper()}'."
    
    rate = rates[to_curr]
    converted = amount * rate
    
    return (
        f"Currency Conversion:\n"
        f"- {amount:,.2f} {from_currency.upper()} = {converted:,.2f} {to_currency.upper()}\n"
        f"- Rate: 1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}"
    )


# Function to get exchange rate between two currencies
def get_exchange_rate(from_currency, to_currency):
    from_curr = from_currency.lower().strip()
    to_curr = to_currency.lower().strip()
    
    url = f"{CURRENCY_BASE}/{from_curr}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Couldn't find currency '{from_currency.upper()}'."
    
    data = response.json()
    rates = data.get(from_curr, {})
    
    if to_curr not in rates:
        return f"Couldn't find currency '{to_currency.upper()}'."
    
    rate = rates[to_curr]
    return f"Exchange Rate: 1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}"


# Function to convert crypto to fiat currency
def crypto_to_fiat(crypto_amount, coin, to_currency):
    coin = coin.lower().strip()
    to_curr = to_currency.lower().strip()
    
    # Get crypto price in USD
    url = f"{COINGECKO_BASE}/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    
    if not data or coin not in data:
        return f"Couldn't find crypto '{coin}'. Try bitcoin, ethereum, solana, etc."
    
    crypto_price_usd = data[coin]["usd"]
    usd_value = crypto_amount * crypto_price_usd
    
    if to_curr == "usd":
        return (
            f"Conversion: {crypto_amount} {coin.upper()} to USD\n"
            f"- {coin.upper()} price: ${crypto_price_usd:,.2f}\n"
            f"- Value: ${usd_value:,.2f} USD"
        )
    
    # Get USD to target currency rate
    rate_url = f"{CURRENCY_BASE}/usd.json"
    rate_response = requests.get(rate_url)
    
    if rate_response.status_code != 200:
        return "Couldn't fetch exchange rates."
    
    rate_data = rate_response.json()
    rates = rate_data.get("usd", {})
    
    if to_curr not in rates:
        return f"Couldn't find currency '{to_currency.upper()}'."
    
    usd_to_fiat_rate = rates[to_curr]
    fiat_value = usd_value * usd_to_fiat_rate
    
    return (
        f"Conversion: {crypto_amount} {coin.upper()} to {to_currency.upper()}\n"
        f"- {coin.upper()} price: ${crypto_price_usd:,.2f} USD\n"
        f"- Value in USD: ${usd_value:,.2f}\n"
        f"- Value in {to_currency.upper()}: {fiat_value:,.2f}"
    )


# Function to convert fiat currency to crypto
def fiat_to_crypto(fiat_amount, from_currency, coin):
    coin = coin.lower().strip()
    from_curr = from_currency.lower().strip()
    
    # Get crypto price in USD
    url = f"{COINGECKO_BASE}/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    
    if not data or coin not in data:
        return f"Couldn't find crypto '{coin}'. Try bitcoin, ethereum, solana, etc."
    
    crypto_price_usd = data[coin]["usd"]
    
    if from_curr == "usd":
        crypto_amount = fiat_amount / crypto_price_usd
        return (
            f"Conversion: ${fiat_amount:,.2f} USD to {coin.upper()}\n"
            f"- {coin.upper()} price: ${crypto_price_usd:,.2f}\n"
            f"- You get: {crypto_amount:.6f} {coin.upper()}"
        )
    
    # Get source currency to USD rate
    rate_url = f"{CURRENCY_BASE}/{from_curr}.json"
    rate_response = requests.get(rate_url)
    
    if rate_response.status_code != 200:
        return f"Couldn't find currency '{from_currency.upper()}'."
    
    rate_data = rate_response.json()
    rates = rate_data.get(from_curr, {})
    
    if "usd" not in rates:
        return "Couldn't convert to USD."
    
    fiat_to_usd_rate = rates["usd"]
    usd_value = fiat_amount * fiat_to_usd_rate
    crypto_amount = usd_value / crypto_price_usd
    
    return (
        f"Conversion: {fiat_amount:,.2f} {from_currency.upper()} to {coin.upper()}\n"
        f"- {from_currency.upper()} in USD: ${usd_value:,.2f}\n"
        f"- {coin.upper()} price: ${crypto_price_usd:,.2f}\n"
        f"- You get: {crypto_amount:.6f} {coin.upper()}"
    )



# Tool Definitions for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_crypto_price",
            "description": "Get current price of a cryptocurrency in USD, EUR, GBP. Use when user asks about crypto prices.",
            "parameters": {
                "type": "object",
                "properties": {
                    "coin": {"type": "string", "description": "Cryptocurrency name like bitcoin, ethereum, solana"}
                },
                "required": ["coin"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_cryptos",
            "description": "Get top 10 cryptocurrencies by market cap. Use when user asks about top or biggest cryptos.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_trending_cryptos",
            "description": "Get trending cryptocurrencies right now. Use when user asks what's hot or trending.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert fiat currency to another fiat currency. Use for USD to EUR, NGN to GBP, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount to convert"},
                    "from_currency": {"type": "string", "description": "Source currency code like USD, EUR, NGN"},
                    "to_currency": {"type": "string", "description": "Target currency code like USD, EUR, NGN"}
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get exchange rate between two fiat currencies. Use when user just wants the rate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_currency": {"type": "string", "description": "Source currency code"},
                    "to_currency": {"type": "string", "description": "Target currency code"}
                },
                "required": ["from_currency", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crypto_to_fiat",
            "description": "Convert cryptocurrency to any fiat currency. Use when user wants to convert BTC/ETH/etc to NGN/USD/EUR/etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "crypto_amount": {"type": "number", "description": "Amount of cryptocurrency"},
                    "coin": {"type": "string", "description": "Cryptocurrency name like bitcoin, ethereum, solana"},
                    "to_currency": {"type": "string", "description": "Target fiat currency code like NGN, USD, EUR"}
                },
                "required": ["crypto_amount", "coin", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fiat_to_crypto",
            "description": "Convert fiat currency to cryptocurrency. Use when user wants to know how much BTC/ETH they can get for their NGN/USD/EUR.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fiat_amount": {"type": "number", "description": "Amount of fiat currency"},
                    "from_currency": {"type": "string", "description": "Source fiat currency code like NGN, USD, EUR"},
                    "coin": {"type": "string", "description": "Target cryptocurrency like bitcoin, ethereum, solana"}
                },
                "required": ["fiat_amount", "from_currency", "coin"]
            }
        }
    }
]

# Map names to functions
available_functions = {
    "get_crypto_price": get_crypto_price,
    "get_top_cryptos": get_top_cryptos,
    "get_trending_cryptos": get_trending_cryptos,
    "convert_currency": convert_currency,
    "get_exchange_rate": get_exchange_rate,
    "crypto_to_fiat": crypto_to_fiat,
    "fiat_to_crypto": fiat_to_crypto
}


# Function to handle chat interactions 
def chat(user_message, client, messages):  
    messages.append({"role": "user", "content": user_message})
    
    # Call OpenAI with tools
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    reply = response.choices[0].message
    
    # Check if a function was called
    if reply.tool_calls:
        messages.append(reply)
        
        for tool_call in reply.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
           
            # Run the function
            if func_name in available_functions:
                if func_args:
                    result = available_functions[func_name](**func_args)
                else:
                    result = available_functions[func_name]()
            else:
                result = "Function not found."
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        # Get final response
        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        answer = final.choices[0].message.content
        messages.append({"role": "assistant", "content": answer})
        return answer
    
    else:
        content = reply.content
        messages.append({"role": "assistant", "content": content})
        return content


# Streamlit UI
st.title("Crypto & Currency Chatbot")

st.write("I can help you with real-time data on cryptocurrency prices and currency conversions!")
st.write("Try asking things like:")
st.write("- What's the price of Bitcoin?")
st.write("- Convert 1.5 ETH to NGN")
st.write("- How much Bitcoin can I get for 500000 NGN?")
st.write("- Convert 100 USD to EUR")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": "You are a helpful financial assistant. Use the available tools to help users with crypto prices and currency conversions."
    }]

if "history" not in st.session_state:
    st.session_state.history = []

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# User input
user_input = st.text_input("Enter your question:")

if user_input:
    try:
        response = chat(user_input, client, st.session_state.messages)
        
        # Save to display history
        st.session_state.history.append(f"You: {user_input}")
        st.session_state.history.append(f"Assistant: {response}")
        
        st.subheader("Answer")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")

# View conversation history
with st.expander("Conversation History"):
    if st.session_state.history:
        for entry in st.session_state.history:
            st.write(entry)
    else:
        st.info("No conversation yet.")

# Clear history button
if st.button("Clear History"):
    st.session_state.messages = [{
        "role": "system",
        "content": "You are a helpful financial assistant. Use the available tools to help users with crypto prices and currency conversions."
    }]
    st.session_state.history = []
    st.rerun()