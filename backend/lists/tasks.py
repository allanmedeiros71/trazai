from celery import shared_task
import os
import requests
from django.conf import settings
from lists.models import Item, ProductCache, Category

@shared_task
def categorize_item_task(item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return f"Item {item_id} not found."

    product_name = item.name.strip().lower()

    # Check Cache First
    try:
        cached_product = ProductCache.objects.get(product_name=product_name)
        item.category = cached_product.category
        item.save()
        return f"Item {item_id} categorized as {cached_product.category.name} from cache."
    except ProductCache.DoesNotExist:
        pass

    # Call AI API (using OpenAI as an example if OPENAI_API_KEY is present in settings)
    # Since we are using Gemini/OpenAI, we'll implement a basic structure using requests.
    api_key = os.environ.get('OPENAI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("Warning: No API key found for categorization. Returning.")
        return "No API key found."

    valid_categories = list(Category.objects.values_list('name', flat=True))
    if not valid_categories:
        valid_categories = ["Outros"] # Fallback if db is completely empty
    categories_str = ", ".join(valid_categories)

    # Dummy categorization logic to be replaced with actual API call
    # Here you'd use requests.post to OpenAI/Gemini API to get the category name.
    # For now, we'll try to find a category that matches vaguely or put in a default.
    predicted_category_name = "Outros" # Default
    
    if os.environ.get('OPENAI_API_KEY'):
        # Example OpenAI Call
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system", 
                    "content": f"Você é um assistente que categoriza itens de supermercado. Responda APENAS com UMA das seguintes categorias: {categories_str}. Não adicione pontuação ou explicações."
                },
                {"role": "user", "content": f"Categorize o seguinte item: {product_name}"}
            ]
        }
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                predicted_category_name = result['choices'][0]['message']['content'].strip()
        except requests.RequestException:
            pass
    elif os.environ.get('GEMINI_API_KEY'):
        # Gemini API Call
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        prompt = (
            f"Você é um assistente especialista em categorizar itens de supermercado. "
            f"Classifique o item '{product_name}' escolhendo EXATAMENTE UMA das seguintes categorias: "
            f"{categories_str}. "
            f"Sua resposta deve conter apenas o nome da categoria escolhida, sem pontuação, sem aspas e sem texto adicional."
        )
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    predicted_category_name = result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                print(f"Gemini Error: {response.text}")
        except requests.RequestException as e:
            print(f"Request Exception: {e}")

    # Normalize response
    predicted_category_name = predicted_category_name.replace('"', '').replace("'", '').strip()
    
    # Try to match broadly with valid categories in case model adds prefixes
    matched_category = "Outros"
    for cat in valid_categories:
        if cat.lower() in predicted_category_name.lower():
            matched_category = cat
            break
            
    # Get or create the category
    category, created = Category.objects.get_or_create(name=matched_category)

    # Save to Cache
    ProductCache.objects.create(product_name=product_name, category=category)

    # Update Item
    item.category = category
    item.save()

    return f"Item {item_id} categorized as {category.name} via AI."
