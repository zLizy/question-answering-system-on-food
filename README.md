# question-answering-system-on-food

## Steps
1. Install dependencies
   
```shell
cd question-answering-system-on-food
pip install -r requirements.txt
```

Add your perplexity API key in `.env`.

2. Run the dashboard

```python dashboard.py```

3. Access the dashboard through [https://127.0.1.0:8050/](http://127.0.0.1:8050/)
![Dashboard](img/ui.png)

## Solution
This demo uses LLMs to process user request on the target dataset and return python script.
Results are returned and desplayed after executing the python script. 

### UI
- Python
- Library: Dash, Pandas
### Back-end
- Python
- API
   * OpenAI - gpt-4o
   * Perplexity - llama-3.1-sonar-large-128k-online
