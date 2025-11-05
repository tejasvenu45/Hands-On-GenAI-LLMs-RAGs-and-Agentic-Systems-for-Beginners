from transformers import pipeline
from statistics import mean


sentiment_analyzer = pipeline("sentiment-analysis")


def analyze_sentiment(paragraph: str):
    """Analyze sentiment of a paragraph."""
    result = sentiment_analyzer(paragraph)[0]
    label = result["label"].lower()

    if "pos" in label:
        sentiment = "positive"
    elif "neg" in label:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {"text": paragraph, "sentiment": sentiment, "confidence": result["score"]}


def hr_action_based_on_sentiment(employee_name: str, salary: float, sentiment_result: dict):
    """Decide HR action based on sentiment."""
    sentiment = sentiment_result["sentiment"]
    confidence = sentiment_result["confidence"]

    if sentiment == "positive":
        new_salary = round(salary * 1.10, 2)
        action = f"Positive feedback ({confidence:.2f}). Salary increased by 10% to ₹{new_salary}."
    elif sentiment == "neutral":
        new_salary = salary
        action = f"Neutral feedback ({confidence:.2f}). Salary remains ₹{new_salary}."
    else:
        new_salary = salary
        action = f"Negative feedback ({confidence:.2f}). Employee '{employee_name}' is under review. Salary remains ₹{new_salary}."

    return new_salary, action


def ai_feedback_agent():
    print("=== Employee Feedback AI Agent ===")
    print("Manage multiple employees (press 'q' to quit anytime)\n")

    employees = {}

    while True:
        employee_name = input("Enter employee name (or 'q' to finish): ").strip()
        if employee_name.lower() == "q":
            break

        try:
            salary = float(input(f"Enter current salary for {employee_name} (₹): "))
        except ValueError:
            print("Invalid salary. Please enter a numeric value.")
            continue

        feedback_records = []
        warnings = 0
        salary_after_reviews = salary

        print(f"\n--- Enter feedbacks for {employee_name} ---")
        while True:
            paragraph = input("Feedback (or 'done' to finish this employee): ")
            if paragraph.lower() == "done":
                break

            sentiment_result = analyze_sentiment(paragraph)
            salary_after_reviews, decision = hr_action_based_on_sentiment(
                employee_name, salary_after_reviews, sentiment_result
            )
            print("Decision:", decision)

       
            feedback_records.append({
                "sentiment": sentiment_result["sentiment"],
                "confidence": sentiment_result["confidence"]
            })

            if sentiment_result["sentiment"] == "negative":
                warnings += 1

        employees[employee_name] = {
            "initial_salary": salary,
            "final_salary": salary_after_reviews,
            "feedbacks": feedback_records,
            "warnings": warnings
        }

        print(f"Finished recording feedback for {employee_name}.\n")

    # Generate HR Summary Report
    if not employees:
        print("\nNo employee records entered.")
        return

    print("\n=== HR Summary Report ===")
    for name, data in employees.items():
        sentiments = [f["sentiment"] for f in data["feedbacks"]]
        confidences = [f["confidence"] for f in data["feedbacks"]]
        avg_conf = round(mean(confidences), 2) if confidences else 0

        print(f"\nEmployee: {name}")
        print(f"Initial Salary: ₹{data['initial_salary']}")
        print(f"Final Salary: ₹{data['final_salary']}")
        print(f"Total Feedbacks: {len(data['feedbacks'])}")
        print(f"Positive: {sentiments.count('positive')}")
        print(f"Neutral: {sentiments.count('neutral')}")
        print(f"Negative: {sentiments.count('negative')}")
        print(f"Warnings Issued: {data['warnings']}")
        print(f"Average Confidence: {avg_conf}")
        print("-" * 40)

    print("\nSession complete. All employee feedbacks processed.")


if __name__ == "__main__":
    ai_feedback_agent()
