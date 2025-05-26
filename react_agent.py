import marimo

__generated_with = "0.13.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # React Agent with Tools

    Questo notebook esplora l'implementazione di un React Agent che può utilizzare diversi tools per completare task complessi.

    Il pattern **ReAct (Reasoning + Acting)** combina reasoning in linguaggio naturale e azioni specifiche in modo interleaved.
    """
    )
    return


@app.cell
def _():
    from datetime import datetime
    import os
    from langchain_core.tools import tool
    from langgraph.prebuilt import create_react_agent

    return create_react_agent, datetime, os, tool


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Tools""")
    return


@app.cell
def _(datetime, tool):
    @tool
    def get_weather_info(city: str) -> str:
        """
        Tool per ottenere informazioni meteo.
        Args:
            city: Nome della città
        Returns:
            str: Informazioni meteo
        """
        # Simulazione API meteo
        mock_weather = {
            "catania": "Soleggiato, 22°C, umidità 65%",
            "milano": "Nuvoloso, 18°C, umidità 80%", 
            "napoli": "Piovoso, 20°C, umidità 90%",
            "torino": "Sereno, 16°C, umidità 55%"
        }
        weather = mock_weather.get(city.lower(), f"Dati meteo non disponibili per {city}")
        return f"Meteo per {city}: {weather}"

    @tool
    def add_numbers(a: float, b: float) -> str:
        """
        Tool per sommare due numeri.
        Args:
            a: Primo numero
            b: Secondo numero
        Returns:
            str: Risultato della somma
        """
        result = a + b
        return f"Somma di {a} + {b} = {result}"

    @tool
    def multiply_numbers(a: float, b: float) -> str:
        """
        Tool per moltiplicare due numeri.
        Args:
            a: Primo numero
            b: Secondo numero
        Returns:
            str: Risultato della moltiplicazione
        """
        result = a * b
        return f"Moltiplicazione di {a} × {b} = {result}"

    @tool
    def subtract_numbers(a: float, b: float) -> str:
        """
        Tool per sottrarre due numeri.
        Args:
            a: Primo numero
            b: Secondo numero
        Returns:
            str: Risultato della sottrazione
        """
        result = a - b
        return f"Sottrazione di {a} - {b} = {result}"

    @tool
    def divide_numbers(a: float, b: float) -> str:
        """
        Tool per dividere due numeri.
        Args:
            a: Dividendo
            b: Divisore
        Returns:
            str: Risultato della divisione
        """
        if b == 0:
            return "Errore: Divisione per zero non possibile"
        result = a / b
        return f"Divisione di {a} ÷ {b} = {result}"

    @tool
    def calculate_power(base: float, exponent: float) -> str:
        """
        Tool per calcolare potenze.
        Args:
            base: Base della potenza
            exponent: Esponente
        Returns:
            str: Risultato della potenza
        """
        result = base ** exponent
        return f"Potenza di {base}^{exponent} = {result}"

    @tool
    def get_current_time() -> str:
        """
        Tool per ottenere l'ora corrente.
        Returns:
            str: Ora corrente
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"Ora corrente: {current_time}"

    available_tools = [
        get_weather_info, 
        add_numbers, 
        multiply_numbers, 
        subtract_numbers, 
        divide_numbers, 
        calculate_power,
        get_current_time
    ]
    return (available_tools,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### React agent Implementation""")
    return


@app.cell
def _(os):
    import getpass

    if not os.environ.get("MISTRAL_API_KEY"):
        os.environ["MISTRAL_API_KEY"] = getpass.getpass()
    return


@app.cell
def _():
    from langchain_mistralai import ChatMistralAI

    def mistral_chat_model(temperature=0.2, model="mistral-large-latest"):
        return ChatMistralAI(
            model=model,
            temperature=temperature,
            )
    return (mistral_chat_model,)


@app.cell
def _():
    SYS_PROMPT = "sei un agente esperto multifunzione"
    return (SYS_PROMPT,)


@app.cell
def _(SYS_PROMPT, available_tools, create_react_agent, mistral_chat_model):
    agent = create_react_agent(
                model=mistral_chat_model(),
                tools=available_tools,
                name="agent_multiuse",
                prompt=SYS_PROMPT,
                debug="false"
            )

    return (agent,)


@app.cell
def _(agent):
    agent.invoke(
        {"messages": [{"role": "user", "content": "qual'è il meteo di catania? e dimmi che ore sono"}]}
    )
    return


@app.cell
def _(agent):
    agent.invoke(
        {"messages": [{"role": "user", "content": "Dimmi il meteo di Catania e Milano, poi calcola la differenza tra le temperature."}]}
    )
    return


if __name__ == "__main__":
    app.run()
