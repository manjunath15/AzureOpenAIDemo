import requests
import json

# Replace with your Azure OpenAI endpoint and API key, https://mjopenai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview
endpoint = "https://mjopenai.openai.azure.com"
api_key = "****"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Define the request payload
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are a fashion expert at a fashion organization. Your task is to recommend between five to ten complementary product categories that align with the input product, based on the intended gender. For instance, if the product is a men's casual shirt, your recommendations should include products related to men's fashion. The input product will be provided with its title and attributes in JSON format, enclosed between \"==========\" and \"==========\", along with an image of the product. **IMPORTANT Instruction mentioned in BOLD Please prioritize those Instruction** **Recommend \"Saree Shapewear\" as complementary category only if the product_category of the input product enclosed between \"==========\" and \"==========\" is one of the following: Embellished Sarees, Solid/Plain Sarees, Printed Saree, Handloom Sarees, Pre-Draped Saree, or Embroidered Sarees. If the product_category of the input product enclosed between \"==========\" and \"==========\"  is any other value, do not recommend \"Saree Shapewear\" as complementary category.For example if the input product_category is Kurta, Printed, Dupattas, Mini dresses etc. do not suggest a complementary category as Saree Shapewear.** ========== {     \"color\": \"Yellow\",     \"occasion_value\": \"Casual\",     \"neckline_type\": \"Sweetheart\",     \"pattern\": \"Floral\",     \"gender\": \"Women\",     \"apparel_closure_type\": \"Pull On\",     \"material\": \"Polyester\",     \"fit\": \"Fitted\",     \"sleeve_length_type\": \"Three Fourth Sleeves\",     \"product_category\": \"Tops\",     \"type_of_wear\": \"Westernwear\",     \"title\": \"Twenty Dresses by Nykaa Fashion Yellow Floral Print Sweetheart Neck Fit And Flare Top\" } ========== Based on the product title, product attributes, and image, generate complementary category recommendations by analyzing all the provided information. The complementary category recommendations should only be selected from the below category dictionary enclosed between \"**********\" and \"**********\", where the keys represent the categories, and the values are their corresponding serial codes. This dictionary consists of 78 categories, with each category listed as a key and its respective serial code as the value. ********** {'Anklets': 'A001', 'Backpacks': 'B001', 'Ballerina': 'B002', 'Bangle Bracelets And Cuffs': 'B003', 'Batuas And Potlis': 'B004', 'Beanie': 'B005', 'Belt Bags': 'B006', 'Belts': 'B007', 'Body Chains': 'B008', 'Body Shapers': 'B009', 'Body Tape': 'B010', 'Bra-Underwear Sets': 'B011', 'Bralette': 'B012', 'Casual Boots': 'C001', 'Charms': 'C002', 'Clutches': 'C003', 'Demi / Balconette': 'D001', 'Earrings': 'E001', 'Espadrilles': 'E002', 'Eyeglass Frames': 'E003', 'Fashion Rakhis': 'F001', 'Flats': 'F002', 'Flipflops': 'F003', 'Full': 'F004', 'Hair Bands': 'H001', 'Hair Clips & Pins': 'H002', 'Hair Ties & Scrunchies': 'H003', 'Handbags': 'H004', 'Handbags Accessories': 'H005', 'Heels': 'H006', 'Jewellery Sets': 'J001', 'Kolhapuris': 'K001', 'Laptop Bags': 'L001', 'Lingerie Accessories': 'L002', 'Loafers': 'L003', 'Luggage And Travel Bag': 'L004', 'Maang Tikkas': 'M001', 'Mangalsutra': 'M002', 'Masks': 'M003', 'Minimizer': 'M004', 'Mufflers': 'M005', 'Mules': 'M006', 'Multiway': 'M007', 'Naths And Nose Rings': 'N001', 'Necklaces And Pendants': 'N002', 'Pajamas': 'P001', 'Palazzo': 'P002', 'Panty Packs': 'P003', 'Passport Holder': 'P004', 'Pendants': 'P005', 'Plunge': 'P006', 'Printed': 'P007', 'Rakhi Gift Sets': 'R001', 'Rings': 'R002', 'Sandals': 'S001', 'Saree Shapewear': 'S002', 'Satchels': 'S003', 'Sets': 'S004', 'Sliders': 'S005', 'Sling And Cross Bags': 'S006', 'Slips & Camisoles': 'S007', 'Sneakers': 'S008', 'Socks': 'S009', 'Solid': 'S010', 'Sports Shoes': 'S011', 'Stitched Blouse': 'S012', 'Stoles': 'S013', 'Strapless': 'S014', 'Swim Cover-Up': 'S015', 'Toe Rings': 'T001', 'Tote Bags': 'T002', 'Tube Bra': 'T003', 'Vanity Bags And Pouches': 'V001', 'Wallets And Card Cases': 'W001', 'Watches': 'W002', 'Wedges': 'W003', 'Winterwear': 'W004', 'Women Sunglasses': 'W005'} ********** Recommend complementary categories based on the input clothing style. For example, if the input is a topwear in a western style, suggest complementary categories that align with a western look. If the input is traditional clothing, recommend complementary categories in traditional styles. Prioritize relevant categories only and do not recommend items like stoles and scarfes. For swimwear-related inputs, recommend complementary categories such as straw hats, flip-flops, swim covers, etc. If the input image is of a clothing item, recommend at least one complementary footwear category from the categories, which are enclosed between '**********' and '**********' in a dictionary as keys. Ensure that the recommendation complements the input product. Ensure that the suggested footwear category matches the occasion and culture of the input clothing. For example, traditional clothing should be paired with traditional footwear. Additionally, recommend sports-related categories only if the anchor product enclosed between \"==========\" and \"==========\" is related to the sports category. If the anchor product is not related to sports category than do not recommend sports-related categories. Identify the color of the input product from the attributes, specifically under the key 'color'. If the 'color' attribute is not available, analyze the input image to determine the product's color. Suggest complementary colors that will pair well with the identified color based on complementary color theory. Avoid limiting the recommendations to just black, blue, or beige, and instead choose from a wide range of colors. Provide a reason for suggesting the complementary colors, making sure to include the identified color as part of the explanation. When suggesting complementary categories for an anchor product category, deprioritize the Watches and only recommend it if no other suitable complementary categories are available. Watches should be treated as a last-resort recommendation, to be suggested only when there are no other complementary options left to suggest.Consider this rule only when the complementary category contains Watches. When recommending Bags from the categories enclosed between \"**********\" and \"**********\", ensure that a diverse range of Bags is suggested, selecting options that complement the anchor product well. Make sure to recommend sports-related categories, such as shoes and accessories, only when the input product is also from the sports category. If the input product is not sports-related, do not recommend sports-related categories. Additionally, when recommending Watches for Sportswear, only suggest Sports Watches or Smart Watches, and exclude all other types of Watches. Do not recommend Pajamas with the Sportswear category since Pajamas is considered as sleepwear. Your output should consist only serial codes of the complementary category from the above dictionary enclosed between \"**********\" and \"**********\". Also give your reason for recommending the particular complementary category.Make sure that the complementary category alligned with the reason given by you. Your output should be in JSON format. Let's say the input product information provided to you is Saree then following are the output. Adheer your output to the below format. [{     \"complementary_category_serial_code\" : \"S012\",     \"reason\": \"A stitched blouse is a great complement for a saree because it offers convenience, saving time by eliminating the need for tailoring compared to unstitched blouse pieces. It provides a ready-to-wear option with a perfect fit, enhancing the overall saree look. Stitched blouses are available in various sizes, designs, and patterns, allowing customers to easily find a blouse that matches or contrasts with their saree. Additionally, they cater to the growing demand for quick, hassle-free fashion solutions, making them ideal for modern shoppers looking for both style and practicality.\"     }, {     \"complementary_category_serial_code\" : \"S002\",     \"reason\" : \"Yes, saree shapewear is indeed considered a complementary category to sarees. Saree shapewear is designed to provide a smooth silhouette under the saree, enhancing the drape and overall appearance. It replaces the traditional petticoat (underskirt) and is meant to provide better comfort and support, especially around the waist and hips. Offering saree shapewear alongside sarees in an e-commerce platform could help improve the customer experience by suggesting items that enhance the overall fit and styling of the saree.\" }, {     \"complementary_category_serial_code\" : \"B008\",     \"reason\" : \"In Body Chains, kamarbandh is a great complementary recommendation for a saree because it enhances the traditional and elegant appeal of the outfit by adding a touch of ornamentation around the waist. It accentuates the saree's drape and defines the waistline, creating a more structured and graceful silhouette. Kamarbandhs come in various designs, from minimalistic to heavily embellished, making them versatile for both casual and festive occasions. Additionally, they serve as a fashion statement, helping elevate the saree from everyday wear to a more festive or formal look. This accessory adds both functionality and style, making it a valuable addition to saree ensembles.\" }, {     \"complementary_category_serial_code\" : \"A001\",     \"reason\" : \"An ethnic anklet is a perfect complementary accessory for a saree because it adds a touch of traditional elegance that enhances the overall aesthetic of the outfit. Sarees, often worn during cultural and festive occasions, showcase the ankles, making anklets a visible and striking addition. The intricate designs of ethnic anklets complement the rich patterns and textures of sarees, creating a harmonious and culturally resonant ensemble that elevates the wearer's grace and style.\" }, {   \"complementary_category_serial_code\" : \"E001\",   \"reason\": \"Ethnic earrings are an ideal complementary accessory for a saree because they frame the face and enhance the traditional elegance of the outfit. Sarees, with their intricate drapes and rich designs, call for accessories that can match their opulence, and ethnic earrings do just that. Whether they're elaborate jhumkas, chandbalis, or danglers, these earrings draw attention to the face and add a touch of cultural sophistication. This not only completes the look but also elevates the saree’s overall appeal, making the wearer stand out with a timeless and graceful style.\"   }, {     \"complementary_category_serial_code\" : \"C003\",     \"reason\": \"A Rajasthani-style Royal Clutch Silk Batwa Bag Combo is a perfect match for a saree, blending traditional craftsmanship with elegance. The rich silk fabric and intricate Rajasthani designs echo the opulence of a saree, creating a cohesive and culturally resonant look. These ethnic potli bags not only add a pop of color and texture but also offer a practical yet stylish way to carry essentials. The detailed embroidery and regal aesthetics of the batwa beautifully complement the grace and sophistication of a saree, making it an ideal accessory for festive and formal occasions.\" }, {     \"complementary_category_serial_code\" : \"B004\",     \"reason\": \"Batuas and potlis complement sarees beautifully due to their shared cultural roots, elegant design, and festive appeal. Both accessories often feature intricate embroidery and rich fabrics like silk or brocade, aligning with the saree's traditional aesthetic. Their small, compact size provides balance to the flowing drape of sarees, adding grace without overwhelming the look. Additionally, batuas and potlis come in versatile colors and textures, allowing for easy coordination or contrast. Perfect for weddings, festivals, and traditional events, these accessories enhance the saree ensemble with a sophisticated, timeless touch.\" }]"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "{'active_sports_subcatgeory': None, 'activity': None, 'back': None, 'blouse_type': None, 'cardigans_sweater_type': None, 'color': array(['Black'], dtype=object), 'compression_control': None, 'coverage': None, 'distress': None, 'dress_material_subcategory': None, 'dresses_type': None, 'dupattas_subcategory': None, 'ethnic_dresses_subcategory': None, 'fade': None, 'fit': array(['Regular'], dtype=object), 'gender': array(['Women'], dtype=object), 'impact': None, 'jackets_and_coats_subcategory': None, 'jumpsuits_type': None, 'kurti_kurta_tunics_type': None, 'leg_style': None, 'lehengas_type': None, 'lingerie_collection': None, 'material': array(['Polyester'], dtype=object), 'neckline_type': array(['Ruffled Neck'], dtype=object), 'occasion_value': array(['Casual'], dtype=object), 'padding': None, 'pants_jeans_shorts_type': None, 'pattern': array(['Character'], dtype=object), 'pocket_description': None, 'pockets': None, 'product_category': array(['Crop Tops'], dtype=object), 'profile_recommendation': None, 'reversible': None, 'rise_style': None, 'salwar_suits_sets_type': None, 'sarees_type': None, 'seam': None, 'sets_subcategory': None, 'shirts_tops_and_crop_tops_type': array(['Crop Tops'], dtype=object), 'skirts_type': None, 'sleeve_length_type': array(['Full Sleeves'], dtype=object), 'straps': None, 'stretchable': None, 'style': None, 'support': None, 'target_area': None, 'title': array(['The Souled Store Official Disney Mowgli & Friends Women Cropped Top'],       dtype=object), 'type_of_jeans': None, 'type_of_wear': array(['Westernwear'], dtype=object), 'type_of_work': None, 'wiring': None}"
        }
      ]
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 800,
  "n": 1,
    "stop": None,
    "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "generate_style_details",
      "schema": {
        "type": "object",
        "properties": {
          "generate_style_details": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "complementary_category_serial_code": {
                  "type": "string"
                },
                "reason": {
                  "type": "string"
                }
              },
              "required": [
                "complementary_category_serial_code",
                "reason"
              ]
            }
          }
        }
      }
    }
    }
}   

# Make the request to the Azure OpenAI API
response = requests.post(
    f"{endpoint}/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
    headers=headers,
    json=payload
)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)

