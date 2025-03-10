import os
from openai import OpenAI

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
from PIL import Image
import base64
from tqdm import tqdm


simple_stretch_prompt = """The input will be a picture with a human and an action history you generated. Please help me analyze the human's action.

To improve efficiency, I will send an image every 2 seconds. You must analyze the current image by considering previous images. If the action is the same as before, return same(). If the action changes, return the new action. If you realize the previous analysis was incorrect, correct it using correct(previous_action, new_action). If you cannot determine the action, return noaction().

You must make reasonable guesses based on the context.

    Pay close attention to the human's hands to detect whether they are holding an object.
    If the human is now holding an object but was not before, they must have performed a pickup() action earlier.
    If the human had just opened an articulated object (e.g., fridge, cabinet) and is now interacting with it again, it is likely a close() action rather than another open() action.
    If the human was holding an object earlier and there is no detected place() action, assume they are still holding the object.
    If you cannot determine what the human is holding in the current image, refer to the last known object they picked up. If they previously picked up an apple and no place() action occurred, assume they are still holding the apple.

Respond using these actions:

    open(articulated_object) # The human is opening an articulated object (e.g., fridge, cabinet, microwave, door).
    close(articulated_object) # The human is closing an articulated object.
    pickup(object_name, location_name) # The human is picking up an object from a specific location.
    place(object_name, location_name) # The human is placing an object onto a receptacle or surface.
    say(text) # Describe the action in natural language.
    same() # The human continues doing the same action.
    correct(previous_action, new_action) # The previous action was incorrect; specify the wrong action and the corrected one.
    noaction() # If no valid action is detected, return noaction().

All arguments must be explicit. Do not use pronouns like "it" or vague descriptions.

Examples:

input: "An image that shows a human opening the refrigerator." output: say("This human is opening the refrigerator.") open(refrigerator) end()

input: "A new image where the human is still opening the refrigerator." output: same() end()

input: "A new image shows the human picking up an apple from the refrigerator." output: say("This human is picking up an apple from the refrigerator.") pickup(apple, refrigerator) end()

input: "A new image shows the human with empty hands. Now they are holding something, but the object is unidentifiable." Previous history: pickup(apple, refrigerator) output: say("This human is holding an apple. They must have picked it up earlier.") same() end()

input: "A new image shows the human placing an object on the table." Previous history: pickup(apple, refrigerator) output: say("This human is placing an apple on the table.") place(apple, table) end()

input: "A new image shows that the human was actually opening a microwave, not a refrigerator." output: correct(open(refrigerator), open(microwave)) say("This human is actually opening the microwave.") open(microwave) end()

input: "A new image shows the human standing still." output: say("This human is doing nothing.") noaction() end()

input: "An image where no human is visible." output: say("There is no human.") noaction() end()

input: "A previous image showed the human opening the fridge. Now they are reaching inside." output: same() end()

input: "A previous image showed the human opening the fridge. Now they are closing it." output: say("This human is closing the refrigerator.") close(refrigerator) end()

input: "A previous image showed the human with empty hands. Now they are holding a bottle." output: say("This human is holding a bottle, they must have picked it up earlier.") pickup(bottle, refrigerator) end()

Starting dialogue now.

input: """


prompt = simple_stretch_prompt


FRAME_DIR = "frames_rgb"
FRAME_INTERVAL = 1


image_files = sorted(
    [f for f in os.listdir(FRAME_DIR) if f.endswith(".png")],  
    key=lambda x: int(x.split("_")[-1].split(".")[0])  
)
print(len(image_files),image_files[0])
selected_images = image_files[::FRAME_INTERVAL]  
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
test = ["frame_0500.png"]
# for img_name in tqdm(selected_images, desc="Processing Images"):
#     img_path = os.path.join(FRAME_DIR, img_name)
#     base64_image = encode_image(img_path)


# for img_name in test:#tqdm(selected_images, desc="Processing Images"):
#     img_path = os.path.join(FRAME_DIR, img_name)

history = []

for p in range(0, len(image_files),30):
    img_path = os.path.join(FRAME_DIR, image_files[p])
    base64_image = encode_image(img_path)
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "text", "text": "history:" + " ".join(history)},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},  
                }
            ]
        }
    ],
    max_tokens=400
)


    generated_text = response.choices[0].message.content
    history.append(generated_text)
    # print(response)

    print(f"Image: {img_path}")
    print(f"Response: {generated_text}\n")
