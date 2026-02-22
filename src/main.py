import os
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Add it to .env")

client = OpenAI(api_key=api_key)

SCHEMA_DESCRIPTION = """
Return ONLY valid JSON and match this schema exactly:
{
  "feature": "string",
  "positive_test_cases": [
    {
      "id": "TC001",
      "title": "string",
      "priority": "P0|P1|P2",
      "type": "functional|security|usability|performance",
      "preconditions": ["string"],
      "test_data": {"key": "value"},
      "steps": ["string"],
      "expected_result": "string",
      "automation_candidate": true
    }
  ],
  "negative_test_cases": [ ... same objects ... ],
  "edge_cases": [ ... same objects ... ]
}
"""

def generate_test_cases(feature_description: str) -> dict:
    system_msg = "You are a senior QA engineer. Output ONLY valid JSON. No markdown, no extra text."

    user_msg = f"""
Feature:
{feature_description}

Return JSON exactly in this format:
{{
  "positive_test_cases": [
    {{"id":"TC001","title":"...","steps":["..."],"expected_result":"...","priority":"P0|P1|P2","automation_candidate":true}}
  ],
  "negative_test_cases": [
    {{"id":"TC101","title":"...","steps":["..."],"expected_result":"...","priority":"P0|P1|P2","automation_candidate":true}}
  ],
  "edge_cases": [
    {{"id":"TC201","title":"...","steps":["..."],"expected_result":"...","priority":"P0|P1|P2","automation_candidate":false}}
  ]
}}

Rules:
- Create 5 positive, 5 negative, 5 edge cases.
- Ensure coverage for: valid login, invalid creds, empty fields, lockout after 5 attempts, remember-me.
- IDs must be unique.
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(resp.choices[0].message.content)

def save_json(data: dict, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="AI Test Case Generator (LLM)")
    parser.add_argument("--feature", type=str, help="Feature description text")
    parser.add_argument("--feature-file", type=str, help="Path to a text file containing the feature description")
    parser.add_argument("--out", type=str, default="testcases.json", help="Output JSON file name (default: testcases.json)")
    args = parser.parse_args()

    feature = None
    if args.feature:
        feature = args.feature.strip()
    elif args.feature_file:
        with open(args.feature_file, "r", encoding="utf-8") as f:
            feature = f.read().strip()
    else:
        feature = input("Enter feature description: ").strip()

    if not feature:
        raise ValueError("Feature description is empty.")

    print("\n=== Generating test cases... ===\n")
    result = generate_test_cases(feature)

    result["feature"] = feature
    result["generated_at"] = datetime.utcnow().isoformat() + "Z"

    save_json(result, args.out)

    print(f"✅ Done. Saved to: {args.out}\n")
    print(json.dumps(result, indent=2))

    with open("../testcases.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("\n✅ Saved to testcases.json")

if __name__ == "__main__":
    main()