import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)

        except IOError:
            print(f"Unable to open {image_path}")

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return None
    
    return response.content

async def generate_images(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            with open(fr"Data\{prompt.replace(' ', '_')}{i+1}.jpg", "wb") as f:
                f.write(image_bytes)
        else:
            print(f"Failed to generate image {i+1}")

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

if __name__ == "__main__":
    while True:

        try:
            with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
                Data: str = f.read()

            Prompt, Status = Data.split(",")

            if Status == "True":
                print("Generating Images...")
                ImageStatus = GenerateImages(prompt=Prompt)

                with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                    f.write("False,False")
                    break
            
            else:
                sleep(1)

        except Exception as e:
            print(f"Error: {e}")
            sleep(1)