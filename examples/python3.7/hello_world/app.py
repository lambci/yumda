import os

def lambda_handler(event, context):
    os.chdir("/tmp")
    
    os.system("git clone --depth 1 https://github.com/lambci/yumda")

    os.system("gm convert ./yumda/examples/sam_squirrel.jpg -negate -contrast -resize 100x100 thumbnail.jpg")

    # Normally we'd perhaps upload to S3, etc... but here we just convert to ASCII:
    
    os.system("jp2a --width=69 thumbnail.jpg")
