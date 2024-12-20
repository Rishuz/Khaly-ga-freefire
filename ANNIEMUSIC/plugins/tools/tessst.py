import requests
from pyrogram import Client, filters


# Handler to capture the command and vehicle number
@bot.on_message(filters.command("vehicleinfo") & filters.text)
def fetch_vehicle_info(client, message):
    # Extract vehicle number from the message
    vehicle_number = " ".join(message.command[1:]).strip()
    if not vehicle_number:
        message.reply_text("❌ Please provide a valid vehicle number. Example: /vehicleinfo MH12AB1234")
        return

    # Encode the vehicle number
    encoded_vehicle_number = requests.utils.quote(vehicle_number)

    # API Endpoint
    api_url = f"https://botmaker.serv00.net/vehicle-info.php?number={encoded_vehicle_number}"

    try:
        # Send HTTP GET request
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Check the status of the API response
        if data.get("status") == "success":
            vehicle_data = data.get("data", {})
            # Format the message
            message_text = f"🚗 *Vehicle Details* 🚗\n\n"
            message_text += f"🔢 *Vehicle Number*: `{vehicle_data.get('VEHICLE_NUM', 'N/A')}`\n"
            message_text += f"🏢 *Brand*: `{vehicle_data.get('BRAND', 'N/A')}`\n"
            message_text += f"🚙 *Model*: `{vehicle_data.get('VEHICLE_MODEL', 'N/A')}`\n"
            message_text += f"👤 *Owner*: `{vehicle_data.get('NAME', 'N/A')}`\n"
            message_text += f"🛡️ *Role*: `{vehicle_data.get('ROLE', 'N/A')}`\n"
            message_text += f"🏦 *Insurance By*: `{vehicle_data.get('INSURANCE_BY', 'N/A')}`\n"
            message_text += f"📅 *Insurance Expiry*: `{vehicle_data.get('insurance_Expiry_Date', 'N/A')}`\n"
            message_text += f"⏳ *Days Left*: `{vehicle_data.get('DAYS_LEFT', 'N/A')}`\n"
            message_text += f"👥 *Owner Number*: `{vehicle_data.get('OWNER_NUM', 'N/A')}`\n"
            message_text += f"🏗️ *Commercial*: `{vehicle_data.get('isCommercial', 'N/A')}`\n"
            message_text += f"🗓️ *Registration Date*: `{vehicle_data.get('REG_DATE', 'N/A')}`\n"
            message_text += f"🎂 *Vehicle Age*: `{vehicle_data.get('AGE', 'N/A')}`\n"
            message_text += f"📍 *Pincode*: `{vehicle_data.get('PINCODE', 'N/A')}`\n"
            message_text += f"🚘 *Probable Vehicle Type*: `{vehicle_data.get('PROBABLE_VEHICLE_TYPE', 'N/A')}`\n\n"
            
            # Vehicle image link
            image_url = data.get("image", None)
            if image_url:
                message_text += f"🖼️ *Vehicle Image*: [Click here]({image_url})\n\n"
            else:
                message_text += "🖼️ *Vehicle Image*: `Image not available`\n\n"

            # Send the formatted message
            message.reply_text(message_text, parse_mode="Markdown")

        else:
            # If API status is not success
            message.reply_text("❌ Failed to fetch vehicle information. Please try again later.")

    except Exception as e:
        # Handle any errors during API call
        message.reply_text(f"❌ An error occurred while fetching data: {str(e)}")
