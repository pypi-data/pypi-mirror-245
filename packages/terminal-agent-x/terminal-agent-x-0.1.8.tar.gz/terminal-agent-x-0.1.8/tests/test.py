# curl https://api.openai.com/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $OPENAI_API_KEY" \
#   -d '{
#     "model": "gpt-4-vision-preview",
#     "messages": [
#       {
#         "role": "user",
#         "content": [
#           {
#             "type": "text",
#             "text": "What’s in this image?"
#           },
#           {
#             "type": "image_url",
#             "image_url": {
#               "url": "URL"
#             }
#           }
#         ]
#       }
#     ],
#     "max_tokens": 300
#   }'



def ask_gpt4_vision(prompt, image_url):
