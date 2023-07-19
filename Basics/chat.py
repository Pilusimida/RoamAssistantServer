import openai
import os
# 设置OpenAI API密钥
openai.api_key = os.getenv("OPENAI_KEY")

data = {
    "Transportation": {
        "Flight": "You can book flight ticket from Shanghai to Singapore in here [https://www.kayak.sg/flights/SHA-SIN/2023-08-11/2023-08-18?sort=bestflight_a]",
        "Train": "No train from Shanghai to Singapore."
    },
    "TravelPlan": [
        {
            "index": 0,
            "Morning": "Start your day with a visit to the iconic Merlion Park, where you can see the famous Merlion statue, a mythical creature with the head of a lion and the body of a fish. Enjoy panoramic views of the city skyline and Marina Bay from this picturesque location.",
            "Lunch Recommendation": "You can have lunch in 'Jypsy at One Fullerton' [https://www.pscafe.com/jypsy-one-fullerton] near Merlion Park",
            "Afternoon": "Head to the Supertree Grove at Gardens by the Bay, a futuristic park with towering tree-like structures. Explore the various gardens and attractions, such as the Flower Dome and Cloud Forest, and admire the stunning views of the city from the OCBC Skyway.",
            "Dinner Recommendation": "You can have dinner at 'Marina Bay BBQ Steamboat Buffet' [https://www.facebook.com/marinabaysteamboat/] inside Garden by the Bay",
            "Evening": "Take a leisurely stroll along the Singapore River and enjoy the vibrant atmosphere of Clarke Quay. Indulge in a delicious dinner at one of the riverside restaurants and take a river cruise to see the cityscape illuminated at night.",
            "Bedtime": "You can find amazing hotels here [https://www.kayak.sg/hotels/Singapore/2023-07-12/2023-07-16?sort=rank_a]"
        }
    ],
    "Additional Information": {
        "Emergency Number": "The emergency number in Singapore is 995. This number should be dialed in case of a medical emergency or when an ambulance is needed. When you call 995, you will be connected to the Singapore Civil Defence Force (SCDF) Emergency Medical Services, and they will dispatch an ambulance to your location.",
        "Police Number": "For other emergencies such as police assistance or fire-related emergencies, you can dial 999",
        "Weather Condition": "Summer in Singapore is characterized by occasional rain showers and thunderstorms. These rain showers can be heavy and brief, providing temporary relief from the heat. It's advisable to carry an umbrella or raincoat when exploring the city during the summer season."
    }
}

# 与ChatGPT进行对话
def chat_with_gpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # choose model
        messages=messages
    )

    # 获取ChatGPT的回复
    reply = response.choices[0].message.content
    return reply


messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user",
     "content": "I need help in planning my trip.Here's the situation: I need to create a travel assistant app to help users plan their trips. In the message part, I want to instruct ChatGPT on how to understand the requirements of the prompt. For example, I need to specify the departure location, destination, travel budget, and duration of the trip. Apart from that, I would like the app to focus on attractions and accommodations, providing recommended links for attractions and accommodation options. Additionally, I would like users to have the option to choose different modes of transportation between different locations (consider utilizing the Google Maps API for map visualization). Then, the app should generate a detailed travel itinerary and provide the total budget. For some attractions, it would be great if I could retrieve visitor reviews using the Owl website's API"},
    {"role": "system", "content": "Sure! I can assist you with that."},
    {"role": "user",
     "content": "There are some attractions in Singapore, you should choose part of them to make the plan considering the distances between each pair of attractions:" +
                "Marina Bay Sands, Gardens by the Bay, Universal Studios Singapore, Sentosa Island, Merlion Park, Singapore Flyer, Orchard Road, Chinatown, Little India, Clarke Quay, Raffles Hotel, National Museum of Singapore, Singapore Botanic Gardens, Sri Mariamman Temple, Jurong Bird Park, Singapore Zoo, ArtScience Museum, Asian Civilisations Museum, Fort Canning Park, Haw Par Villa, East Coast Park"},
    {"role": "system",
     "content": "Sure! I will choose part of the attractions from this set if the user's travel destination is Singapore"},
    {"role": "user",
     "content": "Please help me make a travel plan from Shanghai to Singapore for 1 day, budget is not taken into consideration. And return me the plane with json form"},
    {"role": "system",
     "content": "Sure, below is travel plan:" + str(data)},
    {"role": "user",
     "content": "In the later travel plan, please follow the format of "+str(data)},
    {"role": "system",
     "content": "Sure, I will follow the format in the later travel plan."}
]

if __name__ == "__main__":
    # 提示用户输入并与ChatGPT对话
    while True:

        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        user_message = {"role": "user", "content": user_input}
        messages.append(user_message)

        response = chat_with_gpt(messages)

        print("ChatGPT:", response)
        gpt_message = {"role": "system", "content": response}
        messages.append(gpt_message)
