import os
import requests
import json
from mcp.server.fastmcp import FastMCP


# Configuration
CONTACTS_FILE = os.path.join(os.path.dirname(__file__), "contacts.json")

# Create MCP server
mcp = FastMCP("WhatsApp Server")

@mcp.tool()
def send_message(phone_number, message):
    """
    Sends a message via WhatsApp using the Waha API

    Args:
        phone_number: Phone number of the recipient
        message: Content of the message to be sent

    Returns:
        str: Operation result

    Raises:
        Exception: If the message cannot be sent
    """
    try:
        url = "http://localhost:3000/api/sendText"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "chatId": f"{phone_number}@c.us",
            "text": message,
            "session": "default"
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"Response: {response.status_code} - {response.text}")

        if response.status_code in [200, 201]:
            return "Success sending message!"
        return "Error: Bad Request. Please check the phone number and message format."

    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return f"Error sending message: {str(e)}"

def load_contacts():
    """
    Loads contacts from JSON file

    Returns:
        dict: Dictionary of contacts with names as keys and phone numbers as values

    Raises:
        Exception: If the contacts file cannot be read or is not found
    """
    try:
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Loaded contacts: {data}")
                return data.get("contacts", {})
        else:
            print(f"Contacts file not found: {CONTACTS_FILE}")
            return {}
    except Exception as e:
        print(f"Error loading contacts: {str(e)}")
        return {}

@mcp.tool()
def send_message_by_name(name: str, message: str):
    """
    Sends a text message via WhatsApp to a contact by name
    
    Args:
        name: Name of the contact registered in the system
        message: Content of the message to be sent

    Returns:
        str: Operation result
    """
    contacts = load_contacts()
    if name in contacts:
        return send_message(contacts[name], message)
    return f"Contact '{name}' not found. Please check the name and try again."

if __name__ == "__main__":
    print("MCP Waha Server started. Waiting for commands...")
    mcp.run()
