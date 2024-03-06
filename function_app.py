import azure.functions as func
import azure.durable_functions as df
from PIL import Image

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

#resize function
@myApp.activity_trigger(input_name="image")
def resize_image(input_image_path: str,size=(1024, 768)):
    try:
        with Image.open(input_image_path) as image:
            resized_image = image.resize(size)
            resized_image.save(input_image_path)
            print("Image has been Resized")
            return True
    except Exception as e:
        print("Error:", e)
        print("Resize Failed")
        return False
    
    
#greyscale function
@myApp.activity_trigger(input_name="image")
def grayscale_image(input_image_path,):
    try:
        with Image.open(input_image_path) as image:
            grayscale_image = image.convert("L")
            grayscale_image.save(input_image_path)
            print("Image has been Greyscaled")
            return True
    except Exception as e:
        print("Error:", e)
        print("Greyscale Failed")
        return False


# water mark function
@myApp.activity_trigger(input_name="image")
def watermark_image(input_image_path, text="VethusonAmit"):
    try:
        with Image.open(input_image_path) as image:
            draw = ImageDraw.Draw(image)
            width, height = image.size
            font_size = width/10 
            font = ImageFont.load_default(size=font_size)
            text_width = draw.textlength(text, font=font)  
            text_height = font_size * text.count('\n')
            position = ((width - text_width) // 2, (height - text_height) // 2)
            draw.text(position, text, fill="white", font=font)
            image.save(input_image_path)
            print("Watermark successful")
            return True
    except Exception as e:
        print("Error:", e)
        print("Watermark failed")
        return False



# trigger
@app.blob_trigger(arg_name="myblob", path="image",
                               connection="AzureWebJobsStorage") 
def main(myblob: func.InputStream):
   df.start_new("image_processing", None, blob.read())


# Orchestrator
@myApp.orchestration_trigger(context_name="context")
def image_processing(context):
    imageImport = context.input()
    image = yield context.call_activity("resize_image", )
    image = yield context.call_activity("hello", "Tokyo")
    image = yield context.call_activity("hello", "London")

    return [result1, result2, result3]






