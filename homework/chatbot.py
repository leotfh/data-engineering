from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import ollama

class MySQLChatbot:
    def __init__(self, user: str, password: str, host: str, port: str, database: str, model: str = "llama3.2:3b"):
        self.db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        self.engine: Engine = create_engine(self.db_uri)
        self.model = model
        self.chat_history = []

    def get_schema(self) -> str:
        """Fetch basic schema info from the MySQL database."""
        schema = ""
        with self.engine.connect() as conn:
            tables = conn.execute(text("SHOW TABLES")).fetchall()
            for (table_name,) in tables:
                schema += f"\nTable: {table_name}\n"
                columns = conn.execute(text(f"DESCRIBE {table_name}")).fetchall()
                for col in columns:
                    schema += f"  - {col[0]} ({col[1]})\n"
        return schema.strip()

    def build_sql_prompt(self, question: str) -> str:
        """Builds the prompt to send to the LLM."""
        schema = self.get_schema()

        prompt = f"""
            You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
            Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.

            <SCHEMA>{schema}</SCHEMA>

            For example:
                Question: which 3 artists have the most tracks?
                SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
                Question: Name 10 artists
                SQL Query: SELECT Name FROM Artist LIMIT 10;

            IMPORTANT:
                - Output only the final SQL query.
                - Do NOT include explanations or internal reasoning.
                - Do NOT use Markdown or wrap with backticks.

            Your turn:

            Question: {question}
            SQL Query:
        """
        return prompt.strip()

    def ask(self, question: str) -> str:
        """Handles a full question/answer cycle including SQL execution."""
        prompt = self.build_sql_prompt(question)
        response = ollama.chat(model=self.model, messages=[
            {"role": "user", "content": prompt}
        ])
        
        # Preprocess LLM response (you might want to strip <think> etc.)
        full_response = response['message']['content'].strip()
        sql_query = full_response
        if "<think>" in full_response:
            sql_query = full_response.split("</think>")[-1].strip()
        sql_result = None
        try:
            with self.engine.connect() as conn:
                sql_result = conn.execute(text(sql_query)).fetchall()
        except Exception as e:
            error_message = f"[Error running SQL query]: {e}"
            self.chat_history.append((question, error_message))
            return error_message

        # Proceed to natural language formatting
        template = """
        You are a expert data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, question, sql query, and sql response, write a natural language response.
        You prefer short and concise answers, and heavily dislike filler words.
        Do not include any SQL code in your response.
        DO NOT INCLUDE EXPLANATIONS OR INTERNAL REASONING.
        DO NOT USE MARKDOWN OR WRAP WITH BACKTICKS.
        DO NOT DECODE THE TIMESTAMP.
        DO NOT INCLUDE <think> 

        Correct Examples:
            Maximum radiation level is: 660.3214012475306
            The maximum state_pv level was 10395.5498747675. It occurred on timestamp.

        <SCHEMA>{schema}</SCHEMA>
        SQL Query: <SQL>{query}</SQL>
        User question: {question}
        SQL Response: {result}
        """

        formatted_result = ollama.chat(model=self.model, messages=[
            {"role": "user", "content": template.format(
                schema=self.get_schema(),
                query=sql_query,
                question=question,
                result=str(sql_result),
            )}
        ])['message']['content'].strip()

        self.chat_history.append((question, formatted_result))
        return formatted_result

    def check_db_connection(self) -> bool:
        """Check if the database connection is valid."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
