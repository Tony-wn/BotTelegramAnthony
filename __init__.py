import logging
import requests
import json
import os
import azure.functions as func

#Cargar variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

