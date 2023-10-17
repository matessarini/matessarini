{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "# Santander Dev Week 2023 (ETL com Python)"
      ],
      "metadata": {
        "id": "BPJQsTCULaC-"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Contexto:** Você é um cientista de dados no Santander e recebeu a tarefa de envolver seus clientes de maneira mais personalizada. Seu objetivo é usar o poder da IA Generativa para criar mensagens de marketing personalizadas que serão entregues a cada cliente.\n",
        "\n",
        "**Condições do Problema:**\n",
        "\n",
        "1. Você recebeu uma planilha simples, em formato CSV ('SDW2023.csv'), com uma lista de IDs de usuário do banco:\n",
        "  ```\n",
        "  UserID\n",
        "  1\n",
        "  2\n",
        "  3\n",
        "  4\n",
        "  5\n",
        "  ```\n",
        "2. Seu trabalho é consumir o endpoint `GET https://sdw-2023-prd.up.railway.app/users/{id}` (API da Santander Dev Week 2023) para obter os dados de cada cliente.\n",
        "3. Depois de obter os dados dos clientes, você vai usar a API do ChatGPT (OpenAI) para gerar uma mensagem de marketing personalizada para cada cliente. Essa mensagem deve enfatizar a importância dos investimentos.\n",
        "4. Uma vez que a mensagem para cada cliente esteja pronta, você vai enviar essas informações de volta para a API, atualizando a lista de \"news\" de cada usuário usando o endpoint `PUT https://sdw-2023-prd.up.railway.app/users/{id}`.\n",
        "\n"
      ],
      "metadata": {
        "id": "k5fA5OrXt1a3"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Utilize sua própria URL se quiser ;)\n",
        "# Repositório da API: https://github.com/digitalinnovationone/santander-dev-week-2023-api\n",
        "sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'"
      ],
      "metadata": {
        "id": "FKqLC_CWoYqR"
      },
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## **E**xtract\n",
        "\n",
        "Extraia a lista de IDs de usuário a partir do arquivo CSV. Para cada ID, faça uma requisição GET para obter os dados do usuário correspondente."
      ],
      "metadata": {
        "id": "9dfI-o7gLRq9"
      }
    },
    {
      "cell_type": "code",
      "execution_count": 18,
      "metadata": {
        "id": "NYydpX_GLRCB",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "a5200c84-1cf0-439f-9a02-66caccdb64c0"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "[2805, 2806, 2807]\n"
          ]
        }
      ],
      "source": [
        "import pandas as pd\n",
        "\n",
        "df = pd.read_csv('SDW2023.csv')\n",
        "user_ids = df['UserID'].tolist()\n",
        "print(user_ids)"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import requests\n",
        "import json\n",
        "\n",
        "def get_user(id):\n",
        "  response = requests.get(f'{sdw2023_api_url}/users/{id}')\n",
        "  return response.json() if response.status_code == 200 else None\n",
        "\n",
        "users = [user for id in user_ids if (user := get_user(id)) is not None]\n",
        "print(json.dumps(users, indent=2))"
      ],
      "metadata": {
        "id": "F5XOuCZGSTGw",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "8348e33d-3ed1-43bc-e5ef-2bed6f22929c"
      },
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "[\n",
            "  {\n",
            "    \"id\": 2805,\n",
            "    \"name\": \"EDMILSON001\",\n",
            "    \"account\": {\n",
            "      \"id\": 2966,\n",
            "      \"number\": \"1000-001\",\n",
            "      \"agency\": \"0001\",\n",
            "      \"balance\": 0.0,\n",
            "      \"limit\": 1000.0\n",
            "    },\n",
            "    \"card\": {\n",
            "      \"id\": 2724,\n",
            "      \"number\": \"1234 1234 1234 0001\",\n",
            "      \"limit\": 2000.0\n",
            "    },\n",
            "    \"features\": [],\n",
            "    \"news\": [\n",
            "      {\n",
            "        \"id\": 5765,\n",
            "        \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
            "        \"description\": \"Ol\\u00e1 Edmilson! Investir \\u00e9 essencial para multiplicar seu dinheiro e garantir seu futuro financeiro.\"\n",
            "      },\n",
            "      {\n",
            "        \"id\": 5768,\n",
            "        \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
            "        \"description\": \"Ol\\u00e1 EDMILSON001, investir assegura seu futuro financeiro. Comece agora, seu amanh\\u00e3 agradece!\"\n",
            "      },\n",
            "      {\n",
            "        \"id\": 5771,\n",
            "        \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
            "        \"description\": \"Ol\\u00e1 EDMILSON001, invista agora para garantir um futuro pr\\u00f3spero! Seu dinheiro pode trabalhar para voc\\u00ea.\"\n",
            "      }\n",
            "    ]\n",
            "  },\n",
            "  {\n",
            "    \"id\": 2806,\n",
            "    \"name\": \"EDMILSON002\",\n",
            "    \"account\": {\n",
            "      \"id\": 2967,\n",
            "      \"number\": \"1000-002\",\n",
            "      \"agency\": \"0001\",\n",
            "      \"balance\": 0.0,\n",
            "      \"limit\": 1000.0\n",
            "    },\n",
            "    \"card\": {\n",
            "      \"id\": 2725,\n",
            "      \"number\": \"1234 1234 1234 0002\",\n",
            "      \"limit\": 2000.0\n",
            "    },\n",
            "    \"features\": [],\n",
            "    \"news\": [\n",
            "      {\n",
            "        \"id\": 5766,\n",
            "        \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
            "        \"description\": \"Ol\\u00e1 EDMILSON002, investir \\u00e9 o caminho chave para construir um futuro seguro e pr\\u00f3spero. Vamos come\\u00e7ar?\"\n",
            "      },\n",
            "      {\n",
            "        \"id\": 5769,\n",
            "        \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
            "        \"description\": \"Ol\\u00e1, EDMILSON002! Investir \\u00e9 vital para ampliar rendimentos. Fa\\u00e7a seu dinheiro trabalhar para voc\\u00ea!\"\n",
            "      },\n",
            "      {\n",
            "        \"id\": 5772,\n",
            "        \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
            "        \"description\": \"Oi Edmilson002! A chave para crescimento financeiro s\\u00e3o os investimentos. Vamos come\\u00e7ar?\"\n",
            "      }\n",
            "    ]\n",
            "  },\n",
            "  {\n",
            "    \"id\": 2807,\n",
            "    \"name\": \"EDMILSON003\",\n",
            "    \"account\": {\n",
            "      \"id\": 2968,\n",
            "      \"number\": \"1000-003\",\n",
            "      \"agency\": \"0001\",\n",
            "      \"balance\": 0.0,\n",
            "      \"limit\": 1000.0\n",
            "    },\n",
            "    \"card\": {\n",
            "      \"id\": 2726,\n",
            "      \"number\": \"1234 1234 1234 0003\",\n",
            "      \"limit\": 2000.0\n",
            "    },\n",
            "    \"features\": [],\n",
            "    \"news\": [\n",
            "      {\n",
            "        \"id\": 5767,\n",
            "        \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
            "        \"description\": \"Ol\\u00e1 EDMILSON003! Garanta seu futuro. Fa\\u00e7a hoje seus investimentos e alavanque sua prosperidade!\"\n",
            "      },\n",
            "      {\n",
            "        \"id\": 5770,\n",
            "        \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
            "        \"description\": \"Ol\\u00e1 Edmilson003! Seu futuro financeiro merece investimentos inteligentes hoje. Invista para prosperar!\"\n",
            "      },\n",
            "      {\n",
            "        \"id\": 5773,\n",
            "        \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
            "        \"description\": \"Ol\\u00e1, EDMILSON003! Investir \\u00e9 a chave para crescer seu patrim\\u00f4nio e garantir seu futuro financeiro.\"\n",
            "      }\n",
            "    ]\n",
            "  }\n",
            "]\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## **T**ransform\n",
        "\n",
        "Utilize a API do OpenAI GPT-4 para gerar uma mensagem de marketing personalizada para cada usuário."
      ],
      "metadata": {
        "id": "cWoqInB4TF1x"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install openai"
      ],
      "metadata": {
        "id": "O--PCAObTQkK",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "ac2b0422-085d-4fc6-bf8c-cf6c3dd8f706"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: openai in /usr/local/lib/python3.10/dist-packages (0.28.0)\n",
            "Requirement already satisfied: requests>=2.20 in /usr/local/lib/python3.10/dist-packages (from openai) (2.31.0)\n",
            "Requirement already satisfied: tqdm in /usr/local/lib/python3.10/dist-packages (from openai) (4.66.1)\n",
            "Requirement already satisfied: aiohttp in /usr/local/lib/python3.10/dist-packages (from openai) (3.8.5)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/dist-packages (from requests>=2.20->openai) (3.2.0)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests>=2.20->openai) (3.4)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests>=2.20->openai) (2.0.4)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests>=2.20->openai) (2023.7.22)\n",
            "Requirement already satisfied: attrs>=17.3.0 in /usr/local/lib/python3.10/dist-packages (from aiohttp->openai) (23.1.0)\n",
            "Requirement already satisfied: multidict<7.0,>=4.5 in /usr/local/lib/python3.10/dist-packages (from aiohttp->openai) (6.0.4)\n",
            "Requirement already satisfied: async-timeout<5.0,>=4.0.0a3 in /usr/local/lib/python3.10/dist-packages (from aiohttp->openai) (4.0.3)\n",
            "Requirement already satisfied: yarl<2.0,>=1.0 in /usr/local/lib/python3.10/dist-packages (from aiohttp->openai) (1.9.2)\n",
            "Requirement already satisfied: frozenlist>=1.1.1 in /usr/local/lib/python3.10/dist-packages (from aiohttp->openai) (1.4.0)\n",
            "Requirement already satisfied: aiosignal>=1.1.2 in /usr/local/lib/python3.10/dist-packages (from aiohttp->openai) (1.3.1)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Documentação Oficial da API OpenAI: https://platform.openai.com/docs/api-reference/introduction\n",
        "# Informações sobre o Período Gratuito: https://help.openai.com/en/articles/4936830\n",
        "\n",
        "# Para gerar uma API Key:\n",
        "# 1. Crie uma conta na OpenAI\n",
        "# 2. Acesse a seção \"API Keys\"\n",
        "# 3. Clique em \"Create API Key\"\n",
        "# Link direto: https://platform.openai.com/account/api-keys\n",
        "\n",
        "# Substitua o texto TODO por sua API Key da OpenAI, ela será salva como uma variável de ambiente.\n",
        "openai_api_key = 'TODO'"
      ],
      "metadata": {
        "id": "sUB1doiDTX3y"
      },
      "execution_count": 5,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import openai\n",
        "\n",
        "openai.api_key = openai_api_key\n",
        "\n",
        "def generate_ai_news(user):\n",
        "  completion = openai.ChatCompletion.create(\n",
        "    model=\"gpt-4\",\n",
        "    messages=[\n",
        "      {\n",
        "          \"role\": \"system\",\n",
        "          \"content\": \"Você é um especialista em marketing bancário.\"\n",
        "      },\n",
        "      {\n",
        "          \"role\": \"user\",\n",
        "          \"content\": f\"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)\"\n",
        "      }\n",
        "    ]\n",
        "  )\n",
        "  return completion.choices[0].message.content.strip('\\\"')\n",
        "\n",
        "for user in users:\n",
        "  news = generate_ai_news(user)\n",
        "  print(news)\n",
        "  user['news'].append({\n",
        "      \"icon\": \"https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg\",\n",
        "      \"description\": news\n",
        "  })"
      ],
      "metadata": {
        "id": "n1w78kNxTrZY",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "d986a0de-d81b-49c0-f777-0e5f9ed4849b"
      },
      "execution_count": 16,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Olá Mariana, invista agora para garantir um futuro próspero! Seu dinheiro pode trabalhar para você.\n",
            "Oi Bruno! A chave para crescimento financeiro são os investimentos. Vamos começar?\n",
            "Olá, Giulia! Investir é a chave para crescer seu patrimônio e garantir seu futuro financeiro.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## **L**oad\n",
        "\n",
        "Atualize a lista de \"news\" de cada usuário na API com a nova mensagem gerada."
      ],
      "metadata": {
        "id": "kNuP0SDUZMBY"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "def update_user(user):\n",
        "  response = requests.put(f\"{sdw2023_api_url}/users/{user['id']}\", json=user)\n",
        "  return True if response.status_code == 200 else False\n",
        "\n",
        "for user in users:\n",
        "  success = update_user(user)\n",
        "  print(f\"User {user['name']} updated? {success}!\")"
      ],
      "metadata": {
        "id": "YefWfYBoZMN2",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "51c56e49-5da8-4534-ee5c-bc74649763d0"
      },
      "execution_count": 17,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "User Mariana updated? True!\n",
            "User Bruno updated? True!\n",
            "User Giulia updated? True!\n"
          ]
        }
      ]
    }
  ]
}
