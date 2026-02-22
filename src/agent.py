import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import requests

RAG_API_URL = "http://127.0.0.1:8000/generate-testcases-rag"
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def planner(feature: str) -> dict:
    prompt = f"""
You are a QA architect.
Given the feature, produce:
1) key requirements
2) risks
3) coverage checklist

Return JSON:
{{
  "requirements": ["..."],
  "risks": ["..."],
  "checklist": ["..."]
}}

Feature:
{feature}
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{"role":"system","content":"Return JSON only."},
                  {"role":"user","content":prompt}],
        response_format={"type":"json_object"}
    )
    return json.loads(r.choices[0].message.content)

def generator(feature: str, context_bundle: dict) -> dict:
    """
    Uses your local RAG API (Swagger endpoint) to generate test cases grounded in PDF.
    Then optionally merges checklist guidance by asking model to refine the output.
    """
    # 1) Call RAG API
    resp = requests.post(RAG_API_URL, json={"feature": feature}, timeout=120)
    resp.raise_for_status()
    rag_tests = resp.json()

    # 2) (Optional but recommended) Refine using checklist
    refine_prompt = f"""
You are a senior QA engineer.
You are given test cases generated using document context (RAG).
Now refine them using the checklist to ensure nothing is missed.

Checklist:
{json.dumps(context_bundle["checklist"], indent=2)}

Current Test Cases:
{json.dumps(rag_tests, indent=2)}

Return improved JSON in the SAME structure:
positive_test_cases, negative_test_cases, edge_cases.
Each test case should include: id, title, steps, expected_result, priority.
Output JSON only.
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Return JSON only."},
            {"role": "user", "content": refine_prompt}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(r.choices[0].message.content)

def reviewer(feature: str, plan: dict, tests: dict) -> dict:
    prompt = f"""
You are a QA lead reviewing generated test cases.
Check for:
- duplicates
- missing checklist coverage
- vague steps / expected results
- wrong priorities (P0 should cover critical flows)

Checklist:
{json.dumps(plan["checklist"], indent=2)}

Current Test Cases:
{json.dumps(tests, indent=2)}

Return improved JSON in the SAME structure, fixing issues.
Output JSON only.
"""
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{"role":"system","content":"Return JSON only."},
                  {"role":"user","content":prompt}],
        response_format={"type":"json_object"}
    )
    return json.loads(r.choices[0].message.content)
def automation_generator(feature: str, final_tests: dict) -> dict:
    """
    Generates Playwright Python skeleton code for P0 test cases.
    """
    prompt = f"""
You are an automation architect.
Generate Playwright (Python) test skeletons for ONLY P0 test cases.

Feature:
{feature}

Test cases JSON:
{json.dumps(final_tests, indent=2)}

Rules:
- Output JSON only in this format:
{{
  "framework": "playwright-python",
  "files": [
    {{
      "path": "tests/test_login.py",
      "content": "python code as a string"
    }}
  ]
}}
- Use pytest style.
- Use placeholder selectors like: page.locator("data-test=login-email")
- Include comments where real selectors/URLs are needed.
"""

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Return JSON only."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(r.choices[0].message.content)

def run_agent(feature: str) -> dict:
    plan = planner(feature)
    tests = generator(feature, plan)
    final_tests = reviewer(feature, plan, tests)
    automation = automation_generator(feature, final_tests)

    return {
        "feature": feature,
        "plan": plan,
        "final_test_cases": final_tests,
        "automation_bundle": automation
    }

if __name__ == "__main__":
    feature = input("Enter feature: ").strip()
    result = run_agent(feature)
    print(json.dumps(result, indent=2))

    with open("../agent_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("\n✅ Saved to agent_output.json")
    # Write generated automation files
    bundle = result.get("automation_bundle", {})
    files = bundle.get("files", [])

    for fobj in files:
        path = fobj["path"]
        content = fobj["content"]

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"\n✅ Wrote {len(files)} automation file(s)")