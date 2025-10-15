
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

def load_model(model_name="t5-base"):

    print(f"Loading {model_name} model...")
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    print(f"Model loaded on {device}")
    return tokenizer, model, device

def summarize_text(text, tokenizer, model, device, max_length=150, min_length=30):

   
    input_text = "summarize: " + text
    

    inputs = tokenizer.encode(
        input_text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    ).to(device)
    
    summary_ids = model.generate(
        inputs,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def main():
    """Main function to run the summarization demo"""
    
  
    tokenizer, model, device = load_model("t5-small")
    

    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to 
    the natural intelligence displayed by humans and animals. Leading AI textbooks define 
    the field as the study of "intelligent agents": any device that perceives its environment 
    and takes actions that maximize its chance of successfully achieving its goals. 
    Colloquially, the term "artificial intelligence" is often used to describe machines 
    that mimic "cognitive" functions that humans associate with the human mind, such as 
    "learning" and "problem solving". As machines become increasingly capable, tasks 
    considered to require "intelligence" are often removed from the definition of AI, 
    a phenomenon known as the AI effect. A quip in Tesler's Theorem says "AI is whatever 
    hasn't been done yet." For instance, optical character recognition is frequently 
    excluded from things considered to be AI, having become a routine technology.
    """
    
    print("\n" + "="*70)
    print("T5 SUMMARIZATION DEMO")
    print("="*70)
    
    print("\n📄 Original Text:")
    print("-" * 70)
    print(sample_text.strip())
    
    print("\n⚙️  Generating summary...")
    summary = summarize_text(sample_text, tokenizer, model, device)
    
    print("\n📝 Summary:")
    print("-" * 70)
    print(summary)
    print("="*70)

    print("\n\n🔄 Interactive Mode (type 'quit' to exit)")
    print("-" * 70)
    
    while True:
        user_input = input("\nEnter text to summarize (or 'quit'): ")
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if len(user_input.strip()) < 50:
            print("⚠️  Please enter a longer text (at least 50 characters)")
            continue
        
        print("\n⚙️  Generating summary...")
        summary = summarize_text(user_input, tokenizer, model, device)
        print("\n📝 Summary:")
        print(summary)
        print("-" * 70)

if __name__ == "__main__":
    main()