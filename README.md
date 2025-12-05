# 🔍 Text-to-SQL Data Query Assistant-- Pathan Afnan Khan

A powerful application that converts natural language queries into SQL queries and visualizes results automatically using AI.
(also check the screenshot folder for sample output ).
## 🎯 Features

* **Natural Language Processing** : Ask questions in plain English
* **Automatic SQL Generation** : Converts queries to valid SQLite statements
* **Smart Visualization** : AI decides when and what chart to display
* **Interactive UI** : Built with Streamlit for seamless experience
* **Support for Multiple Charts** : Bar, Line, and Pie charts

## 🏗️ Architecture

The application uses:

* **LangChain** : For building the agentic workflow
* **Claude (Anthropic)** : For natural language understanding and SQL generation
* **Streamlit** : For the user interface
* **Plotly** : For interactive visualizations
* **SQLite** : For database operations

## 📋 Prerequisites

* Python 3.8 or higher
* Anthropic API key
* Chinook SQLite database

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd text-to-sql-assistant
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt

and also 
pip install langchain==0.3.11 langchain-core==0.3.24 langchain-community==0.3.11 langchain-openai==0.2.3 --upgrade

```

### Step 4: Setup Database

1. Download the Chinook database from: https://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip
2. Extract the zip file
3. Place `chinook.db` in the `data/` folder

### Step 5: Configure Environment Variables

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Add your Anthropic API key to `.env`:

```
Open AI API key =your_actual_api_key_here
```

Get your API key from: https://console.anthropic.com/

### Step 6: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Database Schema

The Chinook database includes the following tables:

* **customers** : Customer information
* **employees** : Employee details
* **invoices** : Sales invoices
* **invoice_items** : Invoice line items
* **tracks** : Music tracks
* **albums** : Album information
* **artists** : Artist details
* **genres** : Music genres
* **media_types** : Media type categories
* **playlists** : Playlist information

## 💡 Example Queries

Try these natural language queries:

1. "How many customers are in each country?"
2. "Show me the top 10 best-selling tracks"
3. "What is the total sales by genre?"
4. "List all employees with their titles"
5. "Which customers spent the most?"
6. "Show revenue trends over time"
7. "What are the most popular media types?"
8. "Compare album sales by artist"

## 🎨 How It Works

1. **User Input** : User enters a question in natural language
2. **Schema Analysis** : System analyzes the database schema
3. **SQL Generation** : Claude AI converts the question to SQL
4. **Query Execution** : SQL query is executed on the database
5. **Data Display** : Results are shown in a table
6. **Smart Visualization** : AI determines if a chart is needed and generates appropriate visualization

## 🔧 Project Structure

```
text-to-sql-assistant/
├── app.py                 # Main Streamlit application
├── data/
│   └── chinook.db        # SQLite database
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (not in git)
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🚢 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repository
4. Add your `ANTHROPIC_API_KEY` in the Secrets section
5. Deploy!

### Deploy to Other Platforms

The app can be deployed to:

* Heroku
* AWS
* Google Cloud
* Azure

Make sure to set environment variables on your deployment platform.

## 🛠️ Configuration

### Environment Variables

* Open_AI_ API_KEY: Your OpenAI API key (required)
* `STREAMLIT_SERVER_PORT`: Port to run the server (optional, default: 8501)
* `STREAMLIT_SERVER_ADDRESS`: Server address (optional, default: localhost)

### Customization

You can customize:

* Chart colors and themes in the plotting functions
* SQL query generation prompts for better results
* UI styling in the CSS section
* Number of results displayed

## 🐛 Troubleshooting

### Common Issues

 **Issue** : "Database file not found"

* **Solution** : Ensure `chinook.db` is in the `data/` folder

 **Issue** : "API key error"

* **Solution** : Check your `.env` file has the correct API key

 **Issue** : "Module not found"

* **Solution** : Run `pip install -r requirements.txt`

 **Issue** : Charts not displaying

* **Solution** : Check if your query returns numeric data suitable for visualization

## 📈 Performance Tips

* Use specific queries to reduce result size
* Add LIMIT clauses for large datasets
* Keep questions focused and clear
* Use proper column and table names for better results

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 👏 Acknowledgments

* OpenAI for LLM
* SQLite Tutorial for the Chinook database
* Streamlit for the amazing framework
* LangChain for the agent framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

 **Note** : This is a demonstration project for educational purposes. Always validate SQL queries and implement proper security measures in production environments.
