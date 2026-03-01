# EWS-PME (Streamlit)

## Rodar local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Cloud
1. Suba este repo no GitHub.
2. No Streamlit Cloud, crie um novo app.
3. Selecione o repositorio e o arquivo `app.py`.
4. Aguarde o build e acesso.

## Estrutura esperada
- `app.py` (entrada)
- `pages/` (telas)
- `core/` (logica)
- `assets/` (imagens)
- `requirements.txt` (dependencias)
- `.streamlit/config.toml` (tema)
