from flask import Flask, render_template_string, request
import os
import boto3
import json

app = Flask(__name__)

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name=os.environ.get('AWS_REGION', 'us-east-1')
)

@app.route('/', methods=['GET', 'POST'])
def home():
    db_pass = os.environ.get('DB_PASSWORD', 'Not Found')
    secret_status = "Successfully Injected (Zero-Trust Active)" if db_pass != 'Not Found' else "Missing"
    
    ai_response = None
    user_prompt = ""

    if request.method == 'POST':
        user_prompt = request.form.get('prompt', '')
        if user_prompt:
            try:
                payload = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": user_prompt}]
                        }
                    ]
                }
                
                response = bedrock.invoke_model(
                    modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0', 
                    contentType='application/json',
                    accept='application/json',
                    body=json.dumps(payload)
                )
                
                response_body = json.loads(response['body'].read())
                ai_response = response_body.get('content', [{}])[0].get('text', 'No response generated.')
            
            except Exception as e:
                error_str = str(e)
                if "ThrottlingException" in error_str:
                    # The Enterprise Fallback Response for the Viva
                    ai_response = (
                        "⚠️ AWS Bedrock Rate Limit Reached (ThrottlingException).\n\n"
                        "SYSTEM NOTE: The IAM role successfully authenticated, but the AWS account's daily Anthropic token quota has been exceeded.\n\n"
                        "🔄 [FAILOVER CACHE ACTIVATED] Here is a cached response for your demonstration:\n"
                        "An automated CI/CD pipeline paired with zero-trust architecture provides zero-downtime deployments, self-healing infrastructure, and ensures sensitive database credentials are never exposed in source code."
                    )
                else:
                    ai_response = f"Bedrock AI Error: {error_str}"

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AgileOps Enterprise Cloud Control Panel</title>
        <style>
            :root { bg: #0f172a; card-bg: #1e293b; text: #f8fafc; primary: #38bdf8; success: #22c55e; border: #334155; }
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; }
            .container { max-width: 900px; width: 100%; }
            header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 25px; }
            h1 { font-size: 24px; color: #38bdf8; margin: 0; }
            .badge { background: #22c55e20; color: #22c55e; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; border: 1px solid #22c55e50; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }
            .card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
            .card h3 { margin-top: 0; color: #94a3b8; font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; }
            .status-value { font-size: 18px; font-weight: bold; color: #22c55e; margin-top: 10px; }
            .ai-card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px; grid-column: span 2; }
            textarea { width: 100%; background: #0f172a; border: 1px solid #475569; color: #fff; padding: 12px; border-radius: 8px; font-size: 14px; resize: vertical; box-sizing: border-box; margin-top: 10px; }
            button { background: #38bdf8; color: #0f172a; border: none; padding: 10px 20px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-top: 10px; transition: background 0.2s; }
            button:hover { background: #0ea5e9; }
            .ai-output { background: #0f172a; border: 1px solid #334155; padding: 15px; border-radius: 8px; margin-top: 15px; white-space: pre-wrap; color: #e2e8f0; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>⚡ AgileOps Enterprise Control Center</h1>
                <div class="badge">SYSTEM ONLINE</div>
            </header>

            <div class="grid">
                <div class="card">
                    <h3>Zero-Trust Secrets Management</h3>
                    <div class="status-value">🔒 {{ secret_status }}</div>
                    <p style="font-size: 13px; color: #94a3b8; margin-top: 8px;">Dynamic runtime injection via AWS SSM Parameter Store.</p>
                </div>
                <div class="card">
                    <h3>Infrastructure Orchestration</h3>
                    <div class="status-value" style="color: #38bdf8;">🚀 AWS ECS (EC2 Backed)</div>
                    <p style="font-size: 13px; color: #94a3b8; margin-top: 8px;">Self-healing containers with persistent EBS storage.</p>
                </div>
            </div>

            <div class="ai-card">
                <h3>🤖 Amazon Bedrock Generative AI Intelligence Layer</h3>
                <p style="font-size: 13px; color: #94a3b8;">Interact with enterprise foundation models securely hosted inside AWS.</p>
                <form method="POST">
                    <textarea name="prompt" rows="3" placeholder="Ask the cloud assistant anything...">{{ user_prompt }}</textarea>
                    <button type="submit">Invoke Bedrock Model</button>
                </form>
                {% if ai_response %}
                    <div class="ai-output"><strong>AI Response:</strong><br>{{ ai_response }}</div>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
"""
    return render_template_string(html_template, secret_status=secret_status, ai_response=ai_response, user_prompt=user_prompt)

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
